import pytest
import os
import tempfile
from src.utils import (
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

    dirs = get_dir_list(temp_directory)
    assert dirs == ["dir1", "dir2", "dir3"]


def test_count_md_files_in_folder(temp_directory):
    os.mkdir(os.path.join(temp_directory, "subdir"))
    create_file(os.path.join(temp_directory, "file1.md"))
    create_file(os.path.join(temp_directory, "file2.txt"))
    create_file(os.path.join(temp_directory, "subdir", "file3.md"))

    count = count_md_files_in_folder(temp_directory)
    assert count == 2


def test_sort_folders_by_md_count(temp_directory):
    os.mkdir(os.path.join(temp_directory, "dir1"))
    os.mkdir(os.path.join(temp_directory, "dir2"))
    create_file(os.path.join(temp_directory, "dir1", "file1.md"))
    create_file(os.path.join(temp_directory, "dir2", "file1.md"))
    create_file(os.path.join(temp_directory, "dir2", "file2.md"))

    sorted_folders = sort_folders_by_md_count(temp_directory)
    assert sorted_folders == ["dir2", "dir1"]


def test_extract_tags_from_file(temp_directory):
    file_path = os.path.join(temp_directory, "test.md")
    content = "This is a test file with #부서태그1 and #부서태그2"
    create_file(file_path, content)

    tags = extract_tags_from_file(file_path)
    assert tags == {"#부서태그1", "#부서태그2"}


def test_extract_tags_from_directory(temp_directory):
    os.mkdir(os.path.join(temp_directory, "subdir"))
    create_file(os.path.join(temp_directory, "file1.md"),
                "Content with #부서태그1")
    create_file(os.path.join(temp_directory, "subdir",
                "file2.md"), "Content with #부서태그2")
    create_file(os.path.join(temp_directory, "file3.txt"),
                "Content with #부서태그3")

    tags = extract_tags_from_directory(temp_directory)
    assert tags == ["#부서태그1", "#부서태그2"]


def test_secure_filename_custom():
    assert secure_filename_custom("test file.md") == "test file.md"
    assert secure_filename_custom("테스트 파일.md") == "테스트 파일.md"
    assert secure_filename_custom("test/file.md") == "testfile.md"
    assert secure_filename_custom(".hidden") == "unnamed"
    assert secure_filename_custom("  spaces  ") == "spaces"