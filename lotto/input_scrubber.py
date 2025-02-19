import re

import numpy as np

def get_lines(input_str):
    return np.array(input_str.split("\n"))


def validate_line(line, game_draw):
    entry = split_line(line)
    if entry.size == 4:
        if len(set(entry[:-1])) != 3:
            return False
        return True
    return False

    
def split_line(line):
    entry = re.split(r"[^0-9]", line)
    return np.array([int(number) for number in entry if number])