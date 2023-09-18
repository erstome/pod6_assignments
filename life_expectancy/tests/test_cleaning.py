"""Tests for the cleaning module"""
from unittest.mock import patch
import pandas as pd

from life_expectancy.cleaning import main
# from . import OUTPUT_DIR

@patch("life_expectancy.cleaning.load_data")
def test_main_data(patched_load_data, pt_life_expectancy_expected, eu_life_expectancy_raw):
    """Run the `clean_data` function and compare the output to the expected output"""

    patched_load_data.return_value = eu_life_expectancy_raw
    pt_life_expectancy_actual = main(region='PT')

    print(pt_life_expectancy_actual.head())
    print(pt_life_expectancy_expected.head())

    pd.testing.assert_frame_equal(
        pt_life_expectancy_actual, pt_life_expectancy_expected
    )

