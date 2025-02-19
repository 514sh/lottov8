import numpy as np

def read_input(base_dir,date_str,owner_name):
    with open(f"{base_dir}/input/{date_str}_{owner_name}.txt", encoding="utf-8") as input_file:
        return input_file.read()
    
def get_lines(input_str):
    return np.array(input_str.split("\n"))