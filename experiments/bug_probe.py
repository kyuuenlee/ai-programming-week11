import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from bug3_logic import find_max,count_pass

def test_last_max():
    assert find_max([70,85,60,95]) == 95

def test_cutoff_inclusive():
    assert count_pass([60,60,59]) == 2
