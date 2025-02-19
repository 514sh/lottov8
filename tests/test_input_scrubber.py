import numpy as np
from lotto.input_scrubber import get_lines, validate_line, split_line, lines_separator


sample_draw_6_42 = 42
sample_draw_6_45 = 45
sample_draw_6_49 = 49

def test_i_can_parse_output_from_input_file_to_numpy_array(input_from_file):
    input_lines = get_lines(input_from_file)
    expected_output = ["1 2 3 5", "1 2 4 5"]
    assert input_lines[0] == expected_output[0]
    assert input_lines[1] == expected_output[1]
    assert len(input_lines) == len(expected_output)
    
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
    
def test_i_can_validate_that_if_a_line_has_one_length_it_is_invalid(wrong_input_length_only_one):
    is_valid = validate_line(wrong_input_length_only_one, sample_draw_6_42)
    assert is_valid == False
    
def test_i_can_validate_that_if_a_line_is_more_than_valid_length_it_is_invalid(wrong_input_more_than_valid):
    is_valid = validate_line(wrong_input_more_than_valid, sample_draw_6_42)
    assert is_valid == False
    
def test_i_can_validate_that_if_a_line_contains_only_whitespaces_it_is_ignored(ignored_line):
    is_valid = validate_line(ignored_line, sample_draw_6_42)
    assert is_valid == None
    
def test_i_can_separate_valid_lines_from_invalid_lines_given_only_valid_lines(sample_input_str_only_valid):
    valid_lines = lines_separator(sample_input_str_only_valid, sample_draw_6_42)[0]
    expected_output = {
        1: np.array([1,2,3,5]),
        2: np.array([1,2,3,5]),
    }
    assert np.all(valid_lines[1] == expected_output[1]) == True
    assert np.all(valid_lines[2] == expected_output[2]) == True
    assert len(valid_lines) == len(expected_output)
    
def test_i_can_separate_valid_lines_from_invalid_lines_given_only_invalid_lines_in_a_6_42_game_draw(
    sample_input_str_only_valid):
    valid_lines = lines_separator(sample_input_str_only_valid, sample_draw_6_42)[1]
    expected_output = {
        1: "1 2 3 4",
        2: "1 3 3 5",
        3: "1 2 43 10",
        4: "1 2 46 10",
        5: "1 2 50 10",
        6: "1 2 5",
        7: "10",
        8: "1 2 3 4 5"
    }
    
    assert len(valid_lines) == len(expected_output)