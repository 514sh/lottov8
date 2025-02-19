import numpy as np
from lotto.input_scrubber import get_lines, validate_line, split_line


def test_i_can_parse_output_from_input_file_to_numpy_array(input_from_file):
    input_lines = get_lines(input_from_file)
    expected_output = np.array(["1 2 3 5", "1 2 4 5"])
    assert np.all(input_lines == expected_output) == True
    
def test_i_can_split_a_str_line_to_numpy_array(valid_input):
    splitted_line = split_line(valid_input)
    expected_output = np.array([1, 2, 3, 5])
    assert np.all(splitted_line == expected_output) == True
    
# def test_i_can_validate_a_valid_line(valid_input):
#     sample_draw = 42
#     is_valid = validate_line(valid_input, sample_draw)
#     assert is_valid == True