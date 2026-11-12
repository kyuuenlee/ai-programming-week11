# 同一 대화에서 명세를 기준으로 작성한 초안. 코드 비공개 독립 실험이 아님.
import pytest
from load_scores import load_scores

def test_valid_and_duplicate(tmp_path):
    f=tmp_path/'b.csv'; f.write_text('name,score\n가,80\n가,90\n',encoding='utf-8')
    assert load_scores(f)==([('가',80),('가',90)],[])

def test_blank_and_comma(tmp_path):
    f=tmp_path/'b.csv'; f.write_text('name,score\n\n"가,나",70\n',encoding='utf-8')
    assert load_scores(f)==([('가,나',70)],[])

def test_header(tmp_path):
    f=tmp_path/'b.csv'; f.write_text('name,score\n',encoding='utf-8')
    assert load_scores(f)==([],[])

def test_missing(tmp_path):
    with pytest.raises(FileNotFoundError): load_scores(tmp_path/'missing.csv')

@pytest.mark.parametrize('score,valid',[(-1,False),(0,True),(1,True),(99,True),(100,True),(101,False)])
def test_boundary(tmp_path,score,valid):
    f=tmp_path/'b.csv'; f.write_text(f'name,score\n가,{score}\n',encoding='utf-8')
    kept,skipped=load_scores(f)
    assert kept==([('가',score)] if valid else [])
    assert len(skipped)==(0 if valid else 1)
    if not valid: assert skipped[0][0]==2 and skipped[0][1]==f'가,{score}' and skipped[0][2]

@pytest.mark.parametrize('row',['가,80,비고',',80','가,','가,결석','가,88.5'])
def test_invalid_records(tmp_path,row):
    f=tmp_path/'b.csv'; f.write_text('name,score\n'+row+'\n',encoding='utf-8')
    kept,skipped=load_scores(f)
    assert kept==[]
    assert len(skipped)==1
    number,original,reason=skipped[0]
    assert number==2 and original==row and reason
