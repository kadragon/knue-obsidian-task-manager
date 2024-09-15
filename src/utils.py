import re
import os
from src.vectorPinecone import VectorDatabasePinecone


def get_dir_list(base_dir):
    return sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))])


def count_md_files_in_folder(folder_path):
    """
    주어진 폴더 내의 모든 하위 폴더를 포함한 .md 파일을 재귀적으로 찾아서 개수를 반환합니다.
    """
    md_count = 0
    for root, _, files in os.walk(folder_path):
        # 모든 하위 폴더의 .md 파일을 포함하여 개수를 셉니다.
        md_count += len([file for file in files if file.endswith('.md')])
    return md_count


def sort_folders_by_md_count(base_path):
    """
    특정 폴더 내의 1차 하위 폴더들을 .md 파일 개수를 기준으로 정렬합니다.
    각 하위 폴더는 내부의 모든 .md 파일을 포함합니다.
    """
    # base_path의 1차 하위 폴더들을 가져옵니다.
    subfolders = [os.path.join(base_path, folder) for folder in os.listdir(base_path)
                  if os.path.isdir(os.path.join(base_path, folder))]

    # 각 하위 폴더의 모든 내부 폴더를 포함한 .md 파일 개수를 계산합니다.
    folder_md_counts = [(folder, count_md_files_in_folder(folder))
                        for folder in subfolders]

    # .md 파일 개수를 기준으로 폴더명을 정렬합니다.
    sorted_folders = sorted(folder_md_counts, key=lambda x: x[1], reverse=True)

    # 정렬된 결과에서 폴더명만 추출하여 반환합니다.
    sorted_folder_names = [os.path.basename(
        folder[0]) for folder in sorted_folders]

    return sorted_folder_names


def extract_tags_from_file(file_path):
    """파일에서 태그를 추출하는 함수"""
    tags = set()  # 중복 태그 방지를 위해 set 사용
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        # 정규 표현식을 사용하여 태그 추출
        found_tags = re.findall(r'#부서\S+', content)
        tags.update(found_tags)
    return tags


def extract_tags_from_directory(directory_path):
    """디렉토리 내 모든 Markdown 파일에서 태그를 추출하는 함수"""
    all_tags = set()  # 전체 태그를 저장할 set
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.md'):  # Markdown 파일만 처리
                file_path = os.path.join(root, file)
                tags = extract_tags_from_file(file_path)
                all_tags.update(tags)
    return sorted(list(all_tags))


def secure_filename_custom(file_name):
    """
    Custom function to sanitize file names while preserving Korean characters and alphanumerics.
    Removes any potentially harmful characters like directory separators.
    """
    # 알파벳, 숫자, 한글, 마침표, 밑줄, 공백을 제외한 모든 문자를 제거
    file_name = re.sub(r'[^a-zA-Z0-9가-힣._\s]', '', file_name)

    # 연속된 공백을 하나의 공백으로 줄임
    file_name = re.sub(r'\s+', ' ', file_name).strip()

    # 만약 파일 이름이 비어 있거나 '.'로 시작하는 경우 'unnamed'로 대체
    if not file_name or file_name.startswith('.'):
        file_name = 'unnamed'

    return file_name


def save_todo_file(final_dir, file_name, content):
    """Save the todo content to a file and copy the directory path to clipboard."""
    if not os.path.exists(final_dir):
        os.makedirs(final_dir)

    file_path = os.path.join(final_dir, file_name)

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        # 벡터 데이터베이스에 저장
        vdp = VectorDatabasePinecone()
        vdp.upsert(file_path)

        return True
    except Exception:
        return False


def save_pdf_file(final_dir, file):
    if not os.path.exists(final_dir):
        os.makedirs(final_dir)

    try:
        with open(os.path.join(final_dir, file.name), 'wb') as f:
            f.write(file.getbuffer())

        return True
    except:
        return False
