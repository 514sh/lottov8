from src.lotto.core.entry import Entry

def test_entry_class_creation():
    entry = Entry("1 2 3 5")
    assert isinstance(entry, Entry)
    
def test_entry_default_properties():
    entry = Entry(entry="1-2-3-5", owner="test", line_number=1)
    assert entry.line_number == 1
    assert entry.original == "1-2-3-5"
    assert entry.owner == "test"
    assert entry.status == True
    assert entry.limit == None
    assert entry.used_bet == 5
    assert entry.clean_entry == [1,2,3,5]
    assert entry.original_bet == 5
    assert entry.entry_set == frozenset({1,2,3})
    assert entry.ignore == False
    
def test_input_status():
    correct_entry = Entry(entry="1-2-3-5")
    wrong_bet_entry = Entry(entry="1 2 3 4")
    duplicated_entry = Entry(entry="1 1 2 5")
    exceeded_entry = Entry(entry="51 1 10 5")
    assert correct_entry.status == True
    assert wrong_bet_entry.status == False
    assert duplicated_entry.status == False
    assert exceeded_entry.status == False
    
def test_used_bet_with_setting_limit():
    entry_use_limit = Entry(entry="1-2-3-15", limit=10)
    entry_use_bet = Entry(entry="1-2-3-10", limit=15)
    assert entry_use_limit.used_bet == 10
    assert entry_use_bet.used_bet == 10
    
def test_equals():
    entry_1 = Entry("1 2 3 5")
    entry_2 = Entry("2,1,3,10")
    entry_3 = Entry("1,3,4,15")
    assert entry_1 == entry_2
    assert entry_1 != entry_3
    
def test_str():
    wrong_entry = Entry(entry="1 3 4 4", line_number=1, owner="test")
    correct_entry = Entry(entry="1 3 4 5", line_number=1, owner="test")
    print(correct_entry)
    print(wrong_entry)