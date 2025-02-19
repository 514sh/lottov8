import re

import numpy as np


def get_lines(input_str):
    return input_str.split("\n")


def validate_line(line, game_draw):
    entry = split_line(line)
    if entry.size == 0:
        return None
    elif entry.size == 4:
        if len(set(entry[:-1])) != 3:
            return False
        elif not (entry[-1] % 5 == 0):
            return False
        return np.all(entry[:-1] <= game_draw)
    return False

    
def split_line(line):
    entry = re.split(r"[^0-9]", line)
    return np.array([int(number) for number in entry if number])


def lines_separator(input_str, game_draw):
    splitted_lines = get_lines(input_str)
    valid_lines = {}
    invalid_lines = {}
    for index, line in enumerate(splitted_lines):
        line_number = index + 1
        is_valid = validate_line(line, game_draw)
        if is_valid:
            valid_lines[line_number] = split_line(line)
        elif is_valid is not None:
            invalid_lines[line_number] = line
    return valid_lines, invalid_lines