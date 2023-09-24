"""Tests for the load_save module"""
# external imports
from unittest.mock import patch
from pathlib import Path
import os
import pandas as pd

# Local imports
from . import OUTPUT_DIR
from . import FIXTURES_DIR

# Functions to be tested
from life_expectancy.life_expectancy.load_save import load_data
from life_expectancy.life_expectancy.load_save import save_data

def test_load_data(eu_life_expectancy_raw):
    """Tests function load_data"""
    data_directory = str(Path(FIXTURES_DIR, 'eu_life_expectancy_raw.tsv'))
    eu_life_expectancy_raw_actual = load_data(data_directory)

    pd.testing.assert_frame_equal(
        eu_life_expectancy_raw_actual, eu_life_expectancy_raw
    )

@patch('life_expectancy.life_expectancy.load_save.pd.DataFrame.to_csv')
def test_save_data(patched_DataFrame_to_csv, eu_life_expectancy_expected):
    """Tests function save_data"""
    region = "TestRegion"

    save_data(eu_life_expectancy_expected, region)

    # expected output_file name/directory
    output_file = str(Path(OUTPUT_DIR, 'testregion_life_expectancy.csv'))

    # Assert that the function was called with the correct arguments
    patched_DataFrame_to_csv.assert_called_once_with(output_file, index=False)

    # Ensure that the file wasn't created
    assert not os.path.exists(output_file)
