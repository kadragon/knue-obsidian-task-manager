import pytest
import os
import tempfile
from .src.utils import (
    get_dir_list,
    count_md_files_in_folder,
    sort_folders_by_md_count,
    extract_tags_from_file,
    extract_tags_from_directory,
    secure_filename_custom
)


@pytest.fixture
def temp_directory():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname


def create_file(path, content=""):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def test_get_dir_list(temp_directory):
    os.mkdir(os.path.join(temp_directory, "dir1"))
    os.mkdir(os.path.join(temp_directory, "dir2"))
    os.mkdir(os.path.join(temp_directory, "dir3"))
    create_file(os.path.join(temp_directory, "file.txt"))

    result = get_dir_list(temp_directory)
    expected = ["dir1", "dir2", "dir3"]

    if result != expected:
        pytest.fail(f"예상된 폴더 목록: {expected}, 실제 폴더 목록: {result}")


def test_count_md_files_in_folder(temp_directory):
    os.mkdir(os.path.join(temp_directory, "subdir"))
    create_file(os.path.join(temp_directory, "file1.md"))
    create_file(os.path.join(temp_directory, "file2.txt"))
    create_file(os.path.join(temp_directory, "subdir", "file3.md"))

    result = count_md_files_in_folder(temp_directory)
    expected = 2
    if result != expected:
        pytest.fail(f"예상된 태그: {expected}, 실제 태그: {result}")


def test_sort_folders_by_md_count(temp_directory):
    os.mkdir(os.path.join(temp_directory, "dir1"))
    os.mkdir(os.path.join(temp_directory, "dir2"))
    create_file(os.path.join(temp_directory, "dir1", "file1.md"))
    create_file(os.path.join(temp_directory, "dir2", "file1.md"))
    create_file(os.path.join(temp_directory, "dir2", "file2.md"))

    result = sort_folders_by_md_count(temp_directory)
    expected = ["dir2", "dir1"]

    if result != expected:
        pytest.fail(f"예상된 태그: {expected}, 실제 태그: {result}")


def test_extract_tags_from_file(temp_directory):
    file_path = os.path.join(temp_directory, "test.md")
    content = "This is a test file with #부서태그1 and #부서태그2"
    create_file(file_path, content)

    result = extract_tags_from_file(file_path)
    expected = {"#부서태그1", "#부서태그2"}

    if result != expected:
        pytest.fail(f"예상된 태그: {expected}, 실제 태그: {result}")


def test_extract_tags_from_directory(temp_directory):
    os.mkdir(os.path.join(temp_directory, "subdir"))
    create_file(os.path.join(temp_directory, "file1.md"),
                "Content with #부서태그1")
    create_file(os.path.join(temp_directory, "subdir",
                "file2.md"), "Content with #부서태그2")
    create_file(os.path.join(temp_directory, "file3.txt"),
                "Content with #부서태그3")

    result = extract_tags_from_directory(temp_directory)

    expected = ["#부서태그1", "#부서태그2"]

    if result != expected:
        pytest.fail(f"예상된 태그: {expected}, 실제 태그: {result}")


def test_secure_filename_custom():
    test_cases = [
        ("test file.md", "test file.md"),
        ("테스트 파일.md", "테스트 파일.md"),
        ("test/file.md", "testfile.md"),
        (".hidden", "unnamed"),
        ("  spaces  ", "spaces")
    ]

    for input_filename, expected_output in test_cases:
        result = secure_filename_custom(input_filename)
        if result != expected_output:
            pytest.fail(f"입력: {input_filename}, 예상 출력: {
                        expected_output}, 실제 출력: {result}")
