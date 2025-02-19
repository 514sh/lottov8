import numpy as np
from lotto.input_scrubber import get_lines


def test_i_can_parse_output_from_input_file_to_numpy_array(input_from_file):
    input_lines = get_lines(input_from_file)
    expected_output = np.array(["1 2 3 5", "1 2 4 5"])
    assert np.all(input_lines == expected_output) == True
        