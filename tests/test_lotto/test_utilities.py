from pathlib import Path
from datetime import datetime

import pytest

from lotto.utilities import (
    sync_file_read, 
    parse_read_file, 
    generate_filename, 
    parse_date,
    generate_absolute_filename,
    separator,
    combine_entries,
    FileWriter,
)

DATA_DIR = Path(__file__).resolve().parent.parent / "DATADIR"

def test_sync_file_read():
    filename = DATA_DIR / "2025_04_16_abc.txt"
    filename = str(filename)
    read_file = sync_file_read(filename)
    parsed_input = parse_read_file(read_file)
    
    assert read_file == "1 2 3 5\n5 10 15 20"
    assert len(parsed_input) == 2
    assert parsed_input == ["1 2 3 5", "5 10 15 20"]


@pytest.mark.parametrize("month, day, expected", [
    (4, 9, "2025_04_09_abc.txt"),
    (10, 20, "2025_10_20_abc.txt"),
    (12, 9,"2025_12_09_abc.txt"),
    (3, 19,"2025_03_19_abc.txt"),
])    
def test_filename_generator(month, day, expected):
    filename = generate_filename(owner="abc", date=datetime(2025, month, day), filetype="txt")
    assert filename == expected
    
def test_utilities_function_raises_type_error():
    with pytest.raises(TypeError) as excinfo:
        parse_date("2025_04_16")
    assert excinfo.type is TypeError
    assert "Expected" in str(excinfo.value)
    
    with pytest.raises(TypeError) as excinfo:
        parse_read_file([])
    assert excinfo.type is TypeError
    assert "Expected" in str(excinfo.value)
    
    with pytest.raises(TypeError) as excinfo:
        generate_filename(0, datetime.now())
    assert excinfo.type is TypeError
    assert "Expected" in str(excinfo.value)

def test_generate_absolute_filename():
    filename = generate_absolute_filename(parent_dir=DATA_DIR/"input",owner="abc", date=datetime(2025, 4, 21), filetype="txt")
    parent_dir = DATA_DIR / "input"
    assert filename == f"{parent_dir}/2025_04_21_abc.txt"
    
def test_separator():
    entries = [
        "1 2 3 5", # valid entry
        "", # must be ignored
        # invalid entries below
        "1 2 3 4", # wrong bet
        "10 20 30", # wrong length
        "10 20 30 30 30", # wrong length
        "10 10 20 30", # double entry
        "test_kabo"
    ]
    expected_wrong_input = {
        3: "1 2 3 4",
        4: "10 20 30",
        5: "10 20 30 30 30",
        6: "10 10 20 30"
    }
    wrong_input, valid_entries = separator(entries, owner="abc", game_date=datetime(2025, 4, 21), kabos=["test"])
    assert wrong_input == expected_wrong_input
    assert valid_entries == [(1, "1 2 3 5", "abc", "test_kabo")]
    
def test_combiner(entries_01, entries_02):
    list_of_sorted_entries = [entries_01.sort(), entries_02.sort()]
    combined_entries = combine_entries(list_of_sorted_entries)
    
    assert len(combined_entries) == 5
    
    
def test_filewriter_get_limited_entries(file_writer, limited_output):
    file_writer.write_limited(limited_output)
    assert file_writer.body == "abc,def\n1-2-3-10,1-2-3-5\n1-2-4-5,\n"
    
    
def test_filewriter_get_tulog_entries(file_writer, entries_01):
    tulog_entries = entries_01.tulog_items()
    file_writer.write_tulog(tulog_entries)
    assert file_writer.body == "1-2-3-10-abc\n1-2-3-5-def\n"
    
# def test_filewriter_get_draws_and_winners(file_writer, entries_01):
#     file_writer = FileWriter(base_dir=DATA_DIR, owner="test", game_date=datetime(2025, 4, 22))
#     winning_numbers = [1,2,3,10,20,30]
#     draws_entries, winners_entries = entries_01.draws_and_winners_entries(winning_numbers=winning_numbers)
#     draws_entries_limited = draws_entries.limited_entries(10)
#     winners_entries_limited = winners_entries.limited_entries(10)
#     file_writer.write_tulog(draws_entries_limited, winners_entries_limited)
#     assert file_writer.body == "WINNERS\nabc,def\n1-2-3-10,1-2-3-5\n\nTOTAL:,10,5\n\nDRAWS\n1-2-4-5,\nTOTAL:,5,0\n"

    