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
from life_expectancy.life_expectancy.load_save import TSVDataFormat, JSONDataFormat

def test_load_data_tsv(eu_life_expectancy_raw):
    """Tests function load_data tsv files"""
    data_directory = str(Path(FIXTURES_DIR, 'eu_life_expectancy_raw.tsv'))
    eu_life_expectancy_raw_actual = load_data(data_directory, 
                                              data_format_strategy=TSVDataFormat())

    pd.testing.assert_frame_equal(
        eu_life_expectancy_raw_actual, eu_life_expectancy_raw
    )

def test_load_data_json(eurostat_life_expect_raw):
    """Tests function load_data for json files"""
    data_directory = str(Path(FIXTURES_DIR, 'eurostat_life_expect_sample.json'))
    eu_life_expectancy_raw_actual = load_data(data_directory, 
                                              data_format_strategy=JSONDataFormat())
    
    assert eu_life_expectancy_raw_actual.shape[0]==100
    pd.testing.assert_frame_equal(
        eu_life_expectancy_raw_actual, eurostat_life_expect_raw
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
