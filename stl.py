from datetime import datetime
import os

import streamlit as st
import pyperclip
from dotenv import load_dotenv

from src.os_utils import extract_tags_from_directory, sort_folders_by_md_count

# Load environment variables
load_dotenv()
OBSIDIAN_DIR = os.getenv('OBSIDIAN_DIR')


def get_today_date_formats():
    """Returns today's date in two formats."""
    todayDate = datetime.now().strftime("%Y-%m-%d")
    todayYM = datetime.now().strftime("%Y%m")
    return todayDate, todayYM


def select_directory(label, directory_path):
    """Select a directory from a dropdown list."""
    dir_list = [''] + sort_folders_by_md_count(directory_path)
    selected_dir = st.selectbox(label, dir_list)
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


def save_todo_file(final_dir, file_name, content):
    """Save the todo content to a file and copy the directory path to clipboard."""
    if not os.path.exists(final_dir):
        os.makedirs(final_dir)

    file_path = os.path.join(final_dir, file_name)

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        st.success('📂 파일이 성공적으로 저장되었습니다!')
        pyperclip.copy(final_dir)

    except Exception as e:
        st.error(f"❌ 파일 저장 중 오류가 발생했습니다: {str(e)}")


def main():
    st.title('Obsidian Task Maker')

    todayDate, todayYM = get_today_date_formats()

    first_class = select_directory('업무분류', OBSIDIAN_DIR)
    if first_class == '':
        return

    second_class = select_directory(
        '세부업무분류', os.path.join(OBSIDIAN_DIR, first_class))
    if second_class == '':
        return

    tags = st.selectbox('관련 태그 선택', [''] + extract_tags_from_directory(
        os.path.join(OBSIDIAN_DIR, first_class, second_class)))

    todo_title = st.text_input('📝 업무 제목을 입력해주세요.')
    if todo_title == '':
        return

    content = generate_todo_content(
        todo_title, first_class, second_class, todayDate, tags)
    todo_content = st.text_area('📝 업무 내용을 입력해주세요.', content, height=400)

    if content == todo_content:
        return

    # Define the final directory path for the todo item
    sanitized_title = todo_title.replace(' ', '_')
    final_dir = os.path.join(OBSIDIAN_DIR, first_class, second_class, f'{
                             todayYM}_{sanitized_title}')

    st.info(f"저장될 경로: {final_dir}")

    if st.button('저장'):
        save_todo_file(final_dir, f'_{todo_title}.md', todo_content)


if __name__ == '__main__':
    main()
