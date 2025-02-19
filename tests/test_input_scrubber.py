import numpy as np
from lotto.input_scrubber import get_lines, validate_line


def test_i_can_parse_output_from_input_file_to_numpy_array(input_from_file):
    input_lines = get_lines(input_from_file)
    expected_output = np.array(["1 2 3 5", "1 2 4 5"])
    assert np.all(input_lines == expected_output) == True
    
def test_i_can_validate_a_valid_line(valid_input):
    sample_draw = "42"
    is_valid = validate_line(valid_input, sample_draw)
    assert is_valid == True