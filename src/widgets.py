import tkinter as tk
from tkinter import ttk
from src.config import CONFIG
from src.utils import get_first_depth_directories, get_second_depth_directories


def create_widgets(app):
    """
    모든 위젯 생성 함수 호출
    """
    main_frame = ttk.Frame(app.root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)

    create_search_frame(app, main_frame)
    create_listbox(app, main_frame)
    create_selected_person_label(app, main_frame)
    create_folder_selection_frame(app, main_frame)
    create_input_fields(app, main_frame)
    create_save_button(app, main_frame)


def create_search_frame(app, parent):
    """
    검색 프레임 생성
    """
    search_frame = ttk.Frame(parent)
    search_frame.pack(fill=tk.X, pady=(0, 20))

    ttk.Label(search_frame, text="사용자 검색",
              font=CONFIG['font']).pack(side=tk.LEFT)
    app.entry_search = ttk.Entry(search_frame, font=CONFIG['font'])
    app.entry_search.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(10, 0))
    app.entry_search.bind("<Return>", app.search_person)
    app.search_button = ttk.Button(
        search_frame, text="검색", command=app.search_person)
    app.search_button.pack(side=tk.LEFT, padx=(10, 0))


def create_folder_selection_frame(app, parent):
    """
    폴더 선택 프레임 생성
    """
    folder_frame = ttk.Frame(parent)
    folder_frame.pack(fill=tk.X, pady=(0, 20))

    ttk.Label(folder_frame, text="첫 번째 폴더",
              font=CONFIG['font']).pack(side=tk.LEFT)
    app.first_folder_combobox = ttk.Combobox(
        folder_frame, font=CONFIG['font'], state='readonly', width=20)
    app.first_folder_combobox.pack(side=tk.LEFT, padx=(10, 20))
    app.first_folder_combobox.bind(
        "<<ComboboxSelected>>", lambda event: update_second_folder_combobox(app))

    ttk.Label(folder_frame, text="두 번째 폴더",
              font=CONFIG['font']).pack(side=tk.LEFT)
    app.second_folder_combobox = ttk.Combobox(
        folder_frame, font=CONFIG['font'], width=20)
    app.second_folder_combobox.pack(side=tk.LEFT, padx=(10, 0))

    obsidian_dir = CONFIG['OBSIDIAN_DIR']
    first_depth_dirs = get_first_depth_directories(obsidian_dir)
    app.first_folder_combobox['values'] = first_depth_dirs


def update_second_folder_combobox(app):
    """
    첫 번째 폴더 선택에 따라 두 번째 폴더 콤보박스 업데이트
    """
    selected_first_dir = app.first_folder_combobox.get()
    second_depth_dirs = get_second_depth_directories(
        CONFIG['OBSIDIAN_DIR'], selected_first_dir)
    app.second_folder_combobox['values'] = second_depth_dirs
    app.second_folder_combobox.set('')  # Clear previous selection


def create_listbox(app, parent):
    """
    리스트박스 생성
    """
    list_frame = ttk.Frame(parent)
    list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

    app.listbox = tk.Listbox(list_frame, height=5, font=CONFIG['font'])
    app.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    app.listbox.bind('<<ListboxSelect>>', app.select_person_from_list)

    scrollbar = ttk.Scrollbar(
        list_frame, orient=tk.VERTICAL, command=app.listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    app.listbox.config(yscrollcommand=scrollbar.set)


def create_selected_person_label(app, parent):
    """
    선택된 사람 정보 라벨 생성
    """
    app.selected_person_label = ttk.Label(
        parent, text="선택된 대상자: 없음", font=CONFIG['font'])
    app.selected_person_label.pack(pady=(0, 20))


def create_input_fields(app, parent):
    """
    입력 필드 생성
    """
    fields = [
        ("할일 제목", "entry_title", ttk.Entry, {"width": 40}),
        ("관련", "entry_related", tk.Text, {"height": 3, "width": 40}),
        ("현황 및 문제점", "entry_issues", tk.Text, {"height": 4, "width": 40}),
        ("해결 방안", "entry_solution", tk.Text, {"height": 4, "width": 40}),
        ("향후 추진 일정", "entry_schedule", tk.Text, {"height": 3, "width": 40})
    ]

    for label_text, attr_name, widget_class, widget_kwargs in fields:
        field_frame = ttk.Frame(parent)
        field_frame.pack(fill=tk.X, pady=(0, 10))

        label = ttk.Label(field_frame, text=label_text,
                          font=CONFIG['font'], width=10, anchor='e')
        label.pack(side=tk.LEFT, padx=(0, 10))

        widget = widget_class(
            field_frame, font=CONFIG['font'], **widget_kwargs)
        widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
        setattr(app, attr_name, widget)

        if isinstance(widget, tk.Text):
            widget.bind("<Tab>", app.focus_next_widget)


def create_save_button(app, parent):
    """
    저장 버튼 생성
    """
    app.save_button = ttk.Button(parent, text="저장", command=app.save_to_file)
    app.save_button.pack(pady=(20, 0))
