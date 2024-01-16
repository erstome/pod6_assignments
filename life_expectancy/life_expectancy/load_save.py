"""
Module to load and save data
"""
# imports
from abc import ABC, abstractmethod
import json
from pathlib import Path
import pandas as pd

# Local imports
from .countries import Country

# Constants
CURRENT_PATH = Path(__file__).parent.parent

# Strategy pattern
class DataFormatStrategy(ABC): # pylint: disable=too-few-public-methods
    "Data format strategy abstract class"
    @abstractmethod
    def read_data(self, file_path: str) -> pd.DataFrame:
        "Apply data reading strategy for the data format"

class JSONDataFormat(DataFormatStrategy): # pylint: disable=too-few-public-methods
    "JSON data format strategy class"
    def read_data(self, file_path: str) -> pd.DataFrame:
        with open(file_path, encoding="utf-8") as file:
            return pd.DataFrame(json.load(file))

class TSVDataFormat(DataFormatStrategy): # pylint: disable=too-few-public-methods
    "TSV data format strategy class"
    def read_data(self, file_path: str) -> pd.DataFrame:
        return pd.read_csv(file_path, sep='\t')


# Functions
def load_data(file_path: str,
              data_format_strategy: DataFormatStrategy = TSVDataFormat()) -> pd.DataFrame:
    """Loads file to pandas dataframe"""
    return data_format_strategy.read_data(file_path)

def save_data(life_expectancy_df: pd.DataFrame, region: Country) -> None:
    """Saves the dataframe to csv"""

    life_expectancy_df.to_csv(str(CURRENT_PATH) + '/data/' + region.value.lower() + \
                              '_life_expectancy.csv',
                              index=False)
