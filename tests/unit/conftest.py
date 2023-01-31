import pytest
from bot.cocparser import CoCData, load_coc_data_from_file


@pytest.fixture
def coc_test_data_path():
    return 'tests/data/coc_input.json'


@pytest.fixture
def coc_test_data(coc_test_data_path):
    data = CoCData()
    load_coc_data_from_file(data, coc_test_data_path)
    return data
