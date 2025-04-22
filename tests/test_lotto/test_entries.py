from datetime import datetime

from lotto.entries import Entry, Entries

def test_entry_adt():
    valid_entry_01 = Entry(1, "1 4 2 5", "abc")
    valid_entry_02 = Entry(2, "1 3 2 10", "abc")
    valid_entry_03 = Entry(1, "1 2 3 5", "def")
    new_entry = valid_entry_01.new_entry(bet=100)
    assert valid_entry_01.line_number == 1
    assert valid_entry_01.owner == "abc"
    assert valid_entry_01.combination == (1,2,4)
    assert valid_entry_01.bet == 5
    assert valid_entry_02 < valid_entry_01
    assert valid_entry_02 == valid_entry_03
    assert new_entry.bet == 100
    assert new_entry.combination == (1,2,4)
    assert new_entry.line_number == 1
    
def test_entries_sort(entries_01):
    sorted_entries = entries_01.sort()
    assert sorted_entries[0].line_number == 2
    assert sorted_entries[0].owner == "abc"
    assert sorted_entries[1].line_number == 1
    assert sorted_entries[1].owner == "def"
    assert sorted_entries[2].line_number == 1
    assert sorted_entries[2].owner == "abc"
    
def test_entries_limited(entries_01):
    limited = entries_01.limited(10)
    limited_01 = entries_01.limited(5)
    
    limited_entries = entries_01.limited_entries(10)
    
    assert limited[0].bet == 10
    assert limited[1].bet == 5
    assert len(limited) == 2
    assert limited_01[0].bet == 5
    assert entries_01.total_bet == 20
    
    assert isinstance(limited_entries, Entries)
    assert limited_entries.total_bet == 15
    
    
def test_entries_tulog_items(entries_01):
    tulog_entries = entries_01.tulog_items()
    assert len(tulog_entries[(1,2,3)]) == 2
    assert len(tulog_entries) == 1
    assert tulog_entries == {
        (1,2,3): [entries_01[0], entries_01[1]]
    }
    
def test_entries_draws_and_winners_entries(entries_01):
    winning_numbers = [1,2,3,10,20,30]
    draws, winners = entries_01.draws_and_winners_entries(winning_numbers=winning_numbers)
    assert len(draws) == 1
    assert draws[0] == entries_01[2]
    assert len(winners) == 2
    assert winners[0].owner == "abc"
    assert winners[1].owner == "def"
