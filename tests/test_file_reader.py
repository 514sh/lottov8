from lotto import file_reader

def test_read_input_file_given_base_dir_date_and_owner_name(input_from_file):
    # input_contents = file_reader.read_input(base_dir="test_data", date_str="02_19_2025", owner_name="one")
    assert input_from_file == "1 2 3 5\n1 2 4 5"
    