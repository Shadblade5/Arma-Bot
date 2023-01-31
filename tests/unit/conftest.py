import pytest
from bot.cocparser import CoCData, LoadCoCDataFromFile


@pytest.fixture
def coc_test_data_path():
    return 'tests/data/coc_input.json'


@pytest.fixture
def coc_test_data(coc_test_data_path):
    data = CoCData()
    LoadCoCDataFromFile(data, coc_test_data_path)
    return data
