from datetime import datetime
from pathlib import Path

import pytest

from lotto.entries import Entry, Entries
from lotto.utilities import FileWriter

DATA_DIR = Path(__file__).resolve().parent.parent / "DATADIR"

@pytest.fixture
def entries_01() -> Entries:
    return Entries(entries=[
        (1, "1 4 2 5", "abc"),
        (2, "1 3 2 10", "abc"),
        (1, "1 2 3 5", "def"),
    ])
    
@pytest.fixture
def entries_02():
    return Entries(entries=[
        (1, "1 2 4 10", "xyz"),
        (2, "15 1 2 10", "xyz")
    ])
    
@pytest.fixture
def file_writer():
    return FileWriter(base_dir=DATA_DIR, game_date=datetime(2025, 4, 22), game_bets={"abc": 15, "def": 5})

@pytest.fixture
def limited_output(entries_01):
    return entries_01

