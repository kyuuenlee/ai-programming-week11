import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from load_scores import load_scores

def test_intentional_failure():
    kept, _ = load_scores(Path(__file__).resolve().parents[1]/'scores.csv')
    assert len(kept) == 99
