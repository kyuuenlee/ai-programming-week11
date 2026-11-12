"""실행: load_scores.py와 같은 폴더에서 python -m pytest -v"""

import pytest

from load_scores import load_scores


@pytest.fixture
def make_csv(tmp_path):
    """각 테스트 전용 임시 CSV를 생성한다."""
    def write(text, encoding="utf-8"):
        path = tmp_path / "scores.csv"
        path.write_text(text, encoding=encoding)
        return path
    return write


# 정상 입력
def test_valid_scores_preserve_order(make_csv):
    path = make_csv("이름,점수\n민수,75\n지영,90\n")
    assert load_scores(path) == ([("민수", 75), ("지영", 90)], [])


def test_surrounding_whitespace_is_trimmed(make_csv):
    path = make_csv("이름,점수\n  민수  ,  85  \n")
    assert load_scores(path) == ([("민수", 85)], [])


def test_duplicate_names_are_kept(make_csv):
    path = make_csv("이름,점수\n민수,70\n민수,90\n민수,70\n")
    assert load_scores(path) == (
        [("민수", 70), ("민수", 90), ("민수", 70)], []
    )


def test_utf8_bom_and_korean_names(make_csv):
    path = make_csv("이름,점수\n이규은,95\n", encoding="utf-8-sig")
    assert load_scores(path) == ([("이규은", 95)], [])


def test_quoted_name_with_comma(make_csv):
    path = make_csv('이름,점수\n"김,민수",80\n')
    assert load_scores(path) == ([("김,민수", 80)], [])


# 예외: 잘못된 행은 예외를 발생시키지 않고 기록한다.
def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


@pytest.mark.parametrize(
    "row, reason",
    [
        pytest.param("민수", "열 개수가 2가 아님", id="one-column"),
        pytest.param("민수,80,추가", "열 개수가 2가 아님", id="three-columns"),
        pytest.param("민수,", "점수가 비어 있음", id="empty-score"),
        pytest.param("민수,   ", "점수가 비어 있음", id="whitespace-score"),
        pytest.param("민수,abc", "점수가 정수가 아님", id="text-score"),
        pytest.param("민수,80.5", "점수가 정수가 아님", id="decimal-score"),
        pytest.param("민수,80.0", "점수가 정수가 아님", id="decimal-integer"),
        pytest.param(",80", "이름이 비어 있음", id="empty-name"),
        pytest.param("   ,80", "이름이 비어 있음", id="whitespace-name"),
    ],
)
def test_invalid_row_is_logged(make_csv, row, reason):
    path = make_csv(f"이름,점수\n{row}\n")
    assert load_scores(path) == ([], [(2, row, reason)])


def test_mixed_rows_continue_after_errors(make_csv):
    path = make_csv(
        "이름,점수\n민수,75\n\n지영,abc\n,80\n수진,100\n태호,101\n준호,0\n"
    )
    assert load_scores(path) == (
        [("민수", 75), ("수진", 100), ("준호", 0)],
        [
            (4, "지영,abc", "점수가 정수가 아님"),
            (5, ",80", "이름이 비어 있음"),
            (7, "태호,101", "점수가 0~100 밖"),
        ],
    )


# 경계값: 최솟값/최댓값, 바로 안쪽과 바깥쪽을 확인한다.
@pytest.mark.parametrize("score", [0, 1, 99, 100])
def test_scores_within_boundaries(make_csv, score):
    path = make_csv(f"이름,점수\n민수,{score}\n")
    assert load_scores(path) == ([("민수", score)], [])


@pytest.mark.parametrize("score", [-1, 101])
def test_scores_outside_boundaries(make_csv, score):
    path = make_csv(f"이름,점수\n민수,{score}\n")
    assert load_scores(path) == (
        [], [(2, f"민수,{score}", "점수가 0~100 밖")]
    )


@pytest.mark.parametrize(
    "text",
    [
        pytest.param("", id="empty-file"),
        pytest.param("이름,점수\n", id="header-only"),
        pytest.param("이름,점수\n\n\n", id="blank-lines-only"),
    ],
)
def test_no_data_returns_empty_lists(make_csv, text):
    assert load_scores(make_csv(text)) == ([], [])


def test_last_row_without_newline(make_csv):
    assert load_scores(make_csv("이름,점수\n민수,80")) == ([("민수", 80)], [])
