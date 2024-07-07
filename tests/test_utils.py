import pytest
from src.utils import conv_call, get_first_depth_directories


def test_conv_call():
    # 정상적인 전화번호 포맷 테스트
    assert conv_call("123-456-7890") == "7890"
    assert conv_call("02-123-4567") == "4567"

    # 빈 문자열 테스트
    assert conv_call("") == ""

    # None 테스트
    assert conv_call(None) == ""

    # 비정상적인 전화번호 포맷 테스트
    assert conv_call("1234567890") == "1234567890"
    assert conv_call("123-4567890") == "4567890"
    assert conv_call("123-456-") == ""


@pytest.fixture
def setup_test_directories(tmp_path):
    """
    테스트를 위한 디렉토리 구조를 생성하는 pytest fixture
    """
    base_dir = tmp_path / "base"
    base_dir.mkdir()

    # 첫 번째 depth 하위 디렉토리 생성
    (base_dir / "dir1").mkdir()
    (base_dir / "dir2").mkdir()

    # 첫 번째 depth 하위 파일 생성
    (base_dir / "file1.txt").touch()

    # 두 번째 depth 하위 디렉토리 생성
    (base_dir / "dir1" / "subdir1").mkdir()

    return base_dir


def test_get_first_depth_directories(setup_test_directories):
    base_dir = setup_test_directories
    expected_directories = ["dir1", "dir2"]
    result = get_first_depth_directories(base_dir)
    assert sorted(result) == sorted(expected_directories)


if __name__ == "__main__":
    pytest.main()
