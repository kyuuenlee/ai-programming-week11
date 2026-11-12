import pytest

from load_scores import load_scores


@pytest.fixture
def write_csv(tmp_path):
    """각 테스트에서 사용할 CSV 파일을 만든다."""
    def _write(content, *, encoding="utf-8"):
        path = tmp_path / "scores.csv"
        path.write_text(content, encoding=encoding, newline="")
        return path

    return _write


def test_valid_rows_keep_input_order_and_trim_whitespace(write_csv):
    path = write_csv("이름,점수\n  민수  , 75 \n지영,90\n")

    assert load_scores(path) == ([ ("민수", 75), ("지영", 90) ], [])


def test_duplicate_names_are_kept(write_csv):
    path = write_csv("이름,점수\n민수,70\n민수,85\n")

    assert load_scores(path) == ([ ("민수", 70), ("민수", 85) ], [])


@pytest.mark.parametrize("score", [0, 100])
def test_score_range_includes_both_endpoints(write_csv, score):
    path = write_csv(f"이름,점수\n학생,{score}\n")

    assert load_scores(path) == ([ ("학생", score) ], [])


def test_header_only_file_returns_empty_lists(write_csv):
    path = write_csv("이름,점수\n")

    assert load_scores(path) == ([], [])


def test_utf8_bom_is_supported(write_csv):
    path = write_csv("이름,점수\n학생,81\n", encoding="utf-8-sig")

    assert load_scores(path) == ([ ("학생", 81) ], [])


def test_quoted_name_can_contain_comma(write_csv):
    path = write_csv('이름,점수\n"홍길동, 2반",88\n')

    assert load_scores(path) == ([ ("홍길동, 2반", 88) ], [])


def test_blank_lines_are_ignored_without_skip_records(write_csv):
    path = write_csv("이름,점수\n\n학생,80\n\n")

    assert load_scores(path) == ([ ("학생", 80) ], [])


def test_invalid_rows_are_skipped_and_processing_continues(write_csv):
    path = write_csv(
        "이름,점수\n"
        "학생,80\n"
        "열하나만\n"
        "학생,90,추가\n"
        ",70\n"
        "학생,\n"
        "학생,팔십\n"
        "학생,-1\n"
        "학생,101\n"
        "다음학생,100\n"
    )

    kept, skipped = load_scores(path)

    assert kept == [("학생", 80), ("다음학생", 100)]
    assert [line_no for line_no, _, _ in skipped] == [3, 4, 5, 6, 7, 8, 9]
    assert [reason for _, _, reason in skipped] == [
        "열 개수가 2가 아님",
        "열 개수가 2가 아님",
        "이름이 비어 있음",
        "점수가 비어 있음",
        "점수가 정수가 아님",
        "점수가 0~100 밖",
        "점수가 0~100 밖",
    ]


def test_skipped_record_contains_original_line(write_csv):
    original_line = '"홍길동, 2반",101'
    path = write_csv(f"이름,점수\n{original_line}\n")

    kept, skipped = load_scores(path)

    assert kept == []
    assert skipped == [(2, original_line, "점수가 0~100 밖")]


def test_missing_file_raises_file_not_found_error(tmp_path):
    missing_path = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_scores(missing_path)


def test_input_file_is_not_modified(write_csv):
    original = "이름,점수\n학생,75\n학생,잘못된 점수\n"
    path = write_csv(original)
    before = path.read_bytes()

    load_scores(path)

    assert path.read_bytes() == before
