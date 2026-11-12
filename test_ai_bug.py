import pytest
from find_max import find_max


@pytest.mark.parametrize(
    ("scores", "expected"),
    [
        ([7], 7),                       # 원소가 하나
        ([3, 8, 5], 8),                 # 중간 원소가 최댓값
        ([-9, -2, -6], -2),             # 음수 점수
        ([4, 4, 2], 4),                 # 최댓값 중복
        ([1, 3, 9], 9),                 # 마지막 원소가 최댓값
        ([2, 9], 9),                    # 원소가 두 개
    ],
)
def test_find_max_returns_largest_score(scores, expected):
    assert find_max(scores) == expected


def test_find_max_with_empty_list_raises_index_error():
    with pytest.raises(IndexError):
        find_max([])
