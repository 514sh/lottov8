import numpy as np
from lotto.input_scrubber import get_lines, validate_line, split_line


sample_draw_6_42 = 42
sample_draw_6_45 = 45
sample_draw_6_49 = 49

def test_i_can_parse_output_from_input_file_to_numpy_array(input_from_file):
    input_lines = get_lines(input_from_file)
    expected_output = np.array(["1 2 3 5", "1 2 4 5"])
    assert np.all(input_lines == expected_output) == True
    
def test_i_can_split_a_str_line_to_numpy_array(valid_input):
    splitted_line = split_line(valid_input)
    expected_output = np.array([1, 2, 3, 5])
    assert np.all(splitted_line == expected_output) == True
    
def test_i_can_validate_a_valid_line(valid_input):
    is_valid = validate_line(valid_input, sample_draw_6_42)
    assert is_valid == True
    
def test_i_can_validate_a_valid_line_separated_by_punctuation(another_valid_input):
    is_valid = validate_line(another_valid_input, sample_draw_6_42)
    assert is_valid == True

def test_i_can_validate_that_a_double_entry_is_not_a_valid_line(wrong_input_wrong_combination_double_entry):
    is_valid = validate_line(wrong_input_wrong_combination_double_entry, sample_draw_6_42)
    assert is_valid == False
    
def test_i_can_validate_that_if_a_combination_exceeds_42_it_is_invalid_in_a_6_42_game_draw(
    wrong_input_wrong_combination_exceeds_entry_in_6_42_draw):
    is_valid = validate_line(wrong_input_wrong_combination_exceeds_entry_in_6_42_draw, sample_draw_6_42)
    assert is_valid == False
    
def test_i_can_validate_that_if_a_combination_exceeds_45_it_is_invalid_in_a_6_45_game_draw(
    wrong_input_wrong_combination_exceeds_entry_in_6_45_draw):
    is_valid = validate_line(wrong_input_wrong_combination_exceeds_entry_in_6_45_draw, sample_draw_6_45)
    assert is_valid == False
    
def test_i_can_validate_that_if_a_combination_exceeds_49_it_is_invalid_in_a_6_49_game_draw(
    wrong_input_wrong_combination_exceeds_entry_in_6_49_draw):
    is_valid = validate_line(wrong_input_wrong_combination_exceeds_entry_in_6_49_draw, sample_draw_6_49)
    assert is_valid == False

def test_i_can_validate_that_if_a_line_is_less_than_valid_length_it_is_invalid(wrong_input_length_less_than_valid):
    is_valid = validate_line(wrong_input_length_less_than_valid, sample_draw_6_42)
    assert is_valid == False