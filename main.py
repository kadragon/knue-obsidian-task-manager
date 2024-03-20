import os
from dotenv import load_dotenv
from src.todo import TodoMaker


def load_environment_variables():
    """환경 변수를 로드하는 함수."""
    load_dotenv()
    obsidian_dir = os.getenv("OBSIDIAN_DIR")
    if obsidian_dir is None:
        raise ValueError("OBSIDIAN_DIR 환경 변수가 설정되지 않았습니다.")
    return obsidian_dir


def initialize_todo_maker(obsidian_dir):
    """TodoMaker 인스턴스를 초기화하고 반환하는 함수."""
    return TodoMaker(obsidian_dir)


def main():
    """프로그램의 메인 실행 함수."""
    obsidian_dir = load_environment_variables()

    todo_maker = initialize_todo_maker(obsidian_dir)
    todo_maker.run()


if __name__ == "__main__":
    main()
