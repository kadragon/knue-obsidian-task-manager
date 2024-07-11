from tkinter import ttk, messagebox
from src.widgets import create_widgets
from src.utils import validate_inputs, generate_content, get_final_save_path, show_success_message, clear_inputs, search_person, conv_call


class TodoApp:
    def __init__(self, root):
        """
        TodoApp 초기화
        """
        self.root = root
        self.root.title("업무노트 작성기")
        self.root.geometry("600x800")
        self.selected_person = None
        self.persons = None

        self.style = ttk.Style()
        self.style.theme_use('clam')

        create_widgets(self)

    def save_to_file(self):
        """
        입력된 데이터를 파일로 저장
        """
        if not validate_inputs(self):
            return

        content = generate_content(self)
        file_path = get_final_save_path(self)

        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            show_success_message(file_path)
            clear_inputs(self)
        except Exception as e:
            messagebox.showerror("오류", f"파일 저장 중 오류가 발생했습니다: {str(e)}")

    def select_person_from_list(self, event):
        """
        리스트에서 선택된 사람 정보 업데이트
        """
        selected_index = self.listbox.curselection()
        if not selected_index:
            return

        self.selected_person = self.persons['data'][selected_index[0]]
        self.update_selected_person_label()

    def update_selected_person_label(self):
        """
        선택된 사람 정보 라벨 업데이트
        """
        if self.selected_person:
            person_info = (f"선택된 대상자: {self.selected_person['username']} "
                           f"({self.selected_person['buseo_nm']}, {self.selected_person['jikwi']})")
            self.selected_person_label.config(text=person_info)
        else:
            self.selected_person_label.config(text="선택된 대상자: 없음")

    def focus_next_widget(self, event):
        """
        탭 키를 눌렀을 때 다음 위젯으로 포커스 이동
        """
        event.widget.tk_focusNext().focus()
        return "break"

    def search_person(self, event=None):
        """
        사용자 검색 기능
        """
        search_person(self, event)
