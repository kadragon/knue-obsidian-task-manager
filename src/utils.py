import os
import tkinter as tk
from tkinter import messagebox
from src.config import CONFIG
from src.api import api_request
from datetime import datetime
import pyperclip


def validate_inputs(app):
    """
    입력 필드 유효성 검사
    """
    if not all([app.entry_title.get().strip(),
                # app.entry_related.get("1.0", tk.END).strip(),
                app.entry_issues.get("1.0", tk.END).strip(),
                app.entry_solution.get("1.0", tk.END).strip(),
                # app.entry_schedule.get("1.0", tk.END).strip(),
                app.selected_person,
                app.first_folder_combobox.get().strip(),
                app.second_folder_combobox.get().strip()]):
        messagebox.showwarning("입력 오류", "현황 및 문제점, 해결 방안, 폴더, 대상자를 입력해주세요.")
        return False
    return True


def generate_content(app):
    """
    입력된 데이터를 기반으로 파일 내용 생성
    """
    todayDate = datetime.now().strftime("%Y-%m-%d")
    person = app.selected_person
    title = app.entry_title.get().strip()
    related = app.entry_related.get('1.0', tk.END).strip()
    issues = app.entry_issues.get('1.0', tk.END).strip()
    solution = app.entry_solution.get('1.0', tk.END).strip()
    schedule = app.entry_schedule.get('1.0', tk.END).strip()

    person_info = (
        f"#부서/{person['buseo_nm']}/{person['jikwi']}_{person['username']} - "
        f"{conv_call(person['gyonae_no'])}"
    )
    folder_info = f"#업무/{app.first_folder_combobox.get()
                         }/{app.second_folder_combobox.get()}"

    related = "\n".join(
        [f"- {x.strip()}" for x in related.split("\n")])

    issues = "\n".join(
        [f"- {x.strip()}" for x in issues.split("\n")])

    solution = "\n".join(
        [f"- [ ] {x.strip()} ➕ {todayDate} 📅 {todayDate}" for x in solution.split("\n")])

    schedule = "\n".join(
        [f"- [ ] {x.strip()} ➕ {todayDate} 📅 {todayDate}" for x in schedule.split("\n")])

    content = f"""
# _{title}

## 🙋‍♂️ 관련
- {person_info}
- {folder_info}
{related}

## 📢 현황 및 문제점
{issues}

## 🛠 해결 방안
{solution}

## 🔔 향후 추진 일정
{schedule}
    """

    return content.strip()


def get_final_save_path(app):
    """
    최종 파일 저장 경로 생성
    """
    base_dir = CONFIG['OBSIDIAN_DIR']
    first_depth_dir = app.first_folder_combobox.get().strip()
    second_depth_dir = app.second_folder_combobox.get().strip()

    if not first_depth_dir or not second_depth_dir:
        messagebox.showwarning("입력 오류", "저장할 폴더를 선택해주세요.")
        return None

    final_dir = os.path.join(base_dir, first_depth_dir, second_depth_dir, datetime.now(
    ).strftime("%Y%m") + "_" + app.entry_title.get().strip())

    if not os.path.exists(final_dir):
        os.makedirs(final_dir)

    pyperclip.copy(final_dir)

    return os.path.join(final_dir, '_' + app.entry_title.get().strip() + '.md')


def show_success_message(file_path):
    """
    파일 저장 성공 메시지 표시
    """
    messagebox.showinfo("성공", f"{file_path}에 파일이 저장되었습니다.")


def clear_inputs(app):
    """
    입력 필드 초기화
    """
    app.entry_title.delete(0, tk.END)
    for widget in [app.entry_related, app.entry_issues, app.entry_solution, app.entry_schedule]:
        widget.delete("1.0", tk.END)
    app.selected_person = None
    app.update_selected_person_label()


def search_person(app, event=None):
    """
    사용자 검색 기능
    """
    search_term = app.entry_search.get().strip()
    if not search_term:
        return

    try:
        app.persons = api_request(search_term)
        app.listbox.delete(0, tk.END)

        if app.persons['cnt'] == 0:
            messagebox.showwarning("검색 결과", "검색된 데이터가 없습니다.")
            return

        for person in app.persons['data']:
            display_text = f"{person['buseo_nm']}\t{person['username']}\t{
                person['gyonae_no']}\t{person['jikwi']} / {person['chrg_busns_nm']}"
            app.listbox.insert(tk.END, display_text)
    except Exception as e:
        messagebox.showerror("오류", f"API 요청 중 오류가 발생했습니다: {str(e)}")


def conv_call(val: str) -> str:
    """
    연락처 번호를 간단한 형태로 변환

    Args:
        val (str): 변환할 연락처 번호

    Returns:
        str: 간단한 형태의 연락처 번호
    """
    return val.split('-')[-1] if val else ""


def get_first_depth_directories(base_dir):
    """
    주어진 디렉토리에서 첫 번째 depth 하위 디렉토리를 반환

    Args:
        base_dir (str): 기본 디렉토리 경로

    Returns:
        list: 첫 번째 depth 하위 디렉토리 이름 리스트
    """
    return sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))])


def get_second_depth_directories(base_dir, first_depth_dir):
    """
    첫 번째 depth 디렉토리에서 두 번째 depth 하위 디렉토리를 반환

    Args:
        base_dir (str): 기본 디렉토리 경로
        first_depth_dir (str): 첫 번째 depth 디렉토리 이름

    Returns:
        list: 두 번째 depth 하위 디렉토리 이름 리스트
    """
    first_depth_path = os.path.join(base_dir, first_depth_dir)
    return sorted([d for d in os.listdir(first_depth_path) if os.path.isdir(os.path.join(first_depth_path, d))])
