import pytest

@pytest.fixture
def valid_input():
    return "1 2 3 5"

@pytest.fixture
def another_valid_input():
    return "1-2-3-5"

@pytest.fixture
def wrong_input_bet():
    return "1 2 3 4"

@pytest.fixture
def wrong_input_wrong_combination_double_entry():
    return "1 3 3 5"

@pytest.fixture
def wrong_input_wrong_combination_exceeds_entry_in_6_42_draw():
    return "1 2 43 10"

@pytest.fixture
def wrong_input_wrong_combination_exceeds_entry_in_6_45_draw():
    return "1 2 46 10"

@pytest.fixture
def wrong_input_wrong_combination_exceeds_entry_in_6_49_draw():
    return "1 2 50 10"

@pytest.fixture
def wrong_input_length_less_than_valid():
    return "1 2 5"

@pytest.fixture
def wrong_input_length_only_one():
    return "10"

@pytest.fixture
def wrong_input_more_than_valid():
    return "1 2 3 4 5"

@pytest.fixture
def ignored_line():
    return " "


@pytest.fixture
def sample_input_str_only_valid(
    valid_input,
    another_valid_input,
):
    return "\n".join([valid_input, another_valid_input])

@pytest.fixture
def sample_input_str_only_wrong(
    wrong_input_bet,
    wrong_input_wrong_combination_double_entry,
    wrong_input_wrong_combination_exceeds_entry_in_6_42_draw,
    wrong_input_wrong_combination_exceeds_entry_in_6_45_draw,
    wrong_input_wrong_combination_exceeds_entry_in_6_49_draw,
    wrong_input_length_less_than_valid,
    wrong_input_length_only_one,
    wrong_input_more_than_valid,
    ignored_line,
):
    return "\n".join([
        wrong_input_bet,
        wrong_input_wrong_combination_double_entry,
        wrong_input_wrong_combination_exceeds_entry_in_6_42_draw,
        wrong_input_wrong_combination_exceeds_entry_in_6_45_draw,
        wrong_input_wrong_combination_exceeds_entry_in_6_49_draw,
        wrong_input_length_less_than_valid,
        wrong_input_length_only_one,
        wrong_input_more_than_valid,
        ignored_line,
    ])


@pytest.fixture
def sample_input_str(
    valid_input,
    another_valid_input,
    wrong_input_bet,
    wrong_input_wrong_combination_double_entry,
    wrong_input_wrong_combination_exceeds_entry_in_6_42_draw,
    wrong_input_wrong_combination_exceeds_entry_in_6_45_draw,
    wrong_input_wrong_combination_exceeds_entry_in_6_49_draw,
    wrong_input_length_less_than_valid,
    wrong_input_length_only_one,
    wrong_input_more_than_valid,
    ignored_line,
):
    return "\n".join([
        valid_input,
        another_valid_input,
        wrong_input_bet,
        wrong_input_wrong_combination_double_entry,
        wrong_input_wrong_combination_exceeds_entry_in_6_42_draw,
        wrong_input_wrong_combination_exceeds_entry_in_6_45_draw,
        wrong_input_wrong_combination_exceeds_entry_in_6_49_draw,
        wrong_input_length_less_than_valid,
        wrong_input_length_only_one,
        wrong_input_more_than_valid,
        ignored_line,
    ])
