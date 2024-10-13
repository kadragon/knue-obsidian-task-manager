import os
import streamlit as st

from datetime import datetime

from dotenv import load_dotenv

from src.utils import extract_tags_from_directory, sort_folders_by_md_count, secure_filename_custom, save_todo_file
from src.lcop import get_analytic_result
from src.pdf import read_pdf, save_pdf_file
from src.vectorPinecone import VectorDatabasePinecone


# Load environment variables
load_dotenv()

OBSIDIAN_DIR = '/obsidian'


def get_today_date_formats():
    """Returns today's date in two formats."""
    todayDate = datetime.now().strftime("%Y-%m-%d")
    todayYM = datetime.now().strftime("%Y%m")
    return todayDate, todayYM


def select_directory(col, label, directory_path):
    """Select a directory from a dropdown list."""
    dir_list = [''] + sort_folders_by_md_count(directory_path)
    selected_dir = col.selectbox(label, dir_list)
    return selected_dir


def generate_todo_content(todo_title, first_class, second_class, todayDate, tags):
    """Generate the default content for the todo item."""
    return f"""# _{todo_title}

## 🙋‍♂️ 관련
- #업무/{first_class}/{second_class}
- {tags}

## 📢 현황 및 문제점
-

## 🛠 해결 방안
- [ ] 📅 {todayDate}
    """


def reset_session_state():
    """Reset the session state."""
    if 'ai_result' not in st.session_state:
        st.session_state.ai_result = ''
    if 'todo_title_ai' not in st.session_state:
        st.session_state.todo_title_ai = ''


def main():
    vdp = VectorDatabasePinecone()

    st.set_page_config(layout="wide")

    st.title('Obsidian Task Maker')

    # 세션 상태 초기화
    reset_session_state()

    col1, col2 = st.columns(2)

    todayDate, todayYM = get_today_date_formats()

    first_class = select_directory(col1, '업무분류', OBSIDIAN_DIR)
    if first_class == '':
        return

    second_class = select_directory(col1,
                                    '세부업무분류', os.path.join(OBSIDIAN_DIR, first_class))
    if second_class == '':
        return

    tags = col1.selectbox('관련 담당자 선택', [''] + extract_tags_from_directory(
        os.path.join(OBSIDIAN_DIR, first_class, second_class)))

    mail_text = col1.text_area('메일(등) 내용', height=100)

    if mail_text and st.session_state.ai_result == '':
        with st.spinner('입력된 내용을 분석하고 있습니다.'):
            st.session_state.ai_result = get_analytic_result(
                mail_text, f'#업무/{first_class}/{second_class}', tags, is_official_document=False)

            st.session_state.todo_title_ai = st.session_state.ai_result.split("\n")[
                0].replace('# ', '')

    uploaded_file = col1.file_uploader(
        "공문 분석이 필요 할 경우 업로드하세요 (PDF 형식)", type=("pdf"))
    if uploaded_file and st.session_state.ai_result == '':
        with st.spinner('공문을 분석하고 있습니다.'):
            pdf_text = read_pdf(uploaded_file).split("접  수교")[0]
            st.session_state.ai_result = get_analytic_result(
                pdf_text, f'#업무/{first_class}/{second_class}', tags)

            st.session_state.todo_title_ai = st.session_state.ai_result.split("\n")[
                0].replace('# ', '')

            col1.text_area("공문 내용", pdf_text, height=210)

    todo_title = col2.text_input(
        '📝 업무 제목을 입력해주세요.', st.session_state.todo_title_ai)

    # 사용자 입력이 파일명에 사용되기 떄문에 검증하여 안전한 제목 생성
    todo_title = secure_filename_custom(todo_title)

    if todo_title == '':
        return

    if st.session_state.ai_result != '':
        content = st.session_state.ai_result
    else:
        content = generate_todo_content(
            todo_title, first_class, second_class, todayDate, tags)

    todo_content = col2.text_area('📝 업무 내용을 입력해주세요.', content, height=500)

    if col2.button('저장'):
        sanitized_title = todo_title.replace(' ', '_')
        final_dir = os.path.join(OBSIDIAN_DIR, first_class, second_class, f'{
            todayYM}_{sanitized_title}')

        todo_content += "\n\n## 참고\n\n" + \
            vdp.get_reference(todo_content, type='source')

        if save_todo_file(final_dir, f'_{todo_title}.md', todo_content):
            st.toast('파일이 성공적으로 저장되었습니다!', icon='📂')
            col2.info(f"저장 폴더 위치: {final_dir}")

            if uploaded_file:
                save_pdf_file(final_dir, uploaded_file)

            vdp.upsert_recent()
        else:
            st.toast('파일 저장 중 오류가 발생했습니다.', icon='❌')


if __name__ == '__main__':
    main()
