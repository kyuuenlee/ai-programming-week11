from pathlib import Path
import pytest
from load_scores import load_scores
BASE = Path(__file__).parent

def test_정상_파일을_읽는다():
    kept, skipped = load_scores(BASE / "scores.csv")
    assert kept == [("김하나",88),("최,네번",77),("김하나",91),("윤보람",64),("서한별",95)]
    assert len(skipped) == 5

def test_빈_줄은_건너뛴다(tmp_path):
    f = tmp_path / "blank.csv"
    f.write_text("name,score\n\n가,80\n\n", encoding="utf-8")
    assert load_scores(f) == ([("가",80)], [])

def test_이름에_쉼표가_있어도_읽는다(tmp_path):
    f = tmp_path / "comma.csv"
    f.write_text('name,score\n"김,하나",77\n', encoding="utf-8")
    assert load_scores(f) == ([("김,하나",77)], [])

def test_없는_파일이면_오류가_난다(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")

def test_헤더만_있으면_빈_결과():
    assert load_scores(BASE / "empty.csv") == ([], [])

@pytest.mark.parametrize("score,valid", [(-1,False),(0,True),(1,True),(99,True),(100,True),(101,False)])
def test_점수_경계값(tmp_path, score, valid):
    f = tmp_path / "boundary.csv"
    f.write_text(f"name,score\n가,{score}\n", encoding="utf-8")
    kept, skipped = load_scores(f)
    if valid:
        assert (kept, skipped) == ([("가",score)], [])
    else:
        assert kept == []
        assert skipped == [(2,f"가,{score}","점수가 0~100 밖")]

@pytest.mark.parametrize("row,reason", [
    ("가,80,비고","열 개수가 2가 아님"),
    ("가","열 개수가 2가 아님"),
    (",90","이름이 비어 있음"),
    ("가,","점수가 비어 있음"),
    ("가,결석","점수가 정수가 아님"),
    ("가,88.5","점수가 정수가 아님"),
])
def test_잘못된_행의_기록(tmp_path,row,reason):
    f=tmp_path / "invalid.csv"
    f.write_text(f"name,score\n{row}\n",encoding="utf-8")
    assert load_scores(f) == ([],[(2,row,reason)])

def test_동명이인과_공백을_처리한다(tmp_path):
    f=tmp_path / "duplicate.csv"
    f.write_text("name,score\n 가 , 80 \n가,90\n",encoding="utf-8-sig")
    assert load_scores(f) == ([("가",80),("가",90)],[])
