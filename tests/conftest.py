import pytest
from lotto import file_reader

from tests.fixtures import *

@pytest.fixture
def input_from_file():
    return file_reader.read_input(base_dir="test_data", date_str="02_19_2025", owner_name="one")
