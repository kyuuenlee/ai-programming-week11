# 동일 대화에서 생성한 코드 기반 초안. 독립 대화 실험 결과가 아님.
from pathlib import Path
import pytest
from load_scores import load_scores

def test_rows(tmp_path):
    f=tmp_path/'a.csv'
    f.write_text('name,score\n A , 50 \nA,60\n\n"B,C",70\n',encoding='utf-8-sig')
    assert load_scores(f)==([('A',50),('A',60),('B,C',70)],[])

@pytest.mark.parametrize('row,reason',[
    ('A,90,x','열 개수가 2가 아님'),(',90','이름이 비어 있음'),
    ('A,','점수가 비어 있음'),('A,no','점수가 정수가 아님'),
    ('A,-1','점수가 0~100 밖'),('A,101','점수가 0~100 밖')])
def test_skips(tmp_path,row,reason):
    f=tmp_path/'a.csv'
    f.write_text('name,score\n'+row+'\n',encoding='utf-8')
    assert load_scores(f)==([],[(2,row,reason)])

@pytest.mark.parametrize('score',[0,1,99,100])
def test_bounds(tmp_path,score):
    f=tmp_path/'a.csv'
    f.write_text(f'name,score\nA,{score}\n',encoding='utf-8')
    assert load_scores(f)==([('A',score)],[])

def test_header(tmp_path):
    f=tmp_path/'a.csv'; f.write_text('name,score\n',encoding='utf-8')
    assert load_scores(f)==([],[])

def test_missing(tmp_path):
    with pytest.raises(FileNotFoundError): load_scores(tmp_path/'missing.csv')
