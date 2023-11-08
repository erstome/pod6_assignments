"""
Module to load and save data
"""
# imports
from pathlib import Path
import pandas as pd

# Constants
CURRENT_PATH = Path(__file__).parent.parent

# Functions
def load_data(file_path: str) -> pd.DataFrame:
    """Loads tsv file to pandas dataframe"""

    # Loads the eu_life_expectancy_raw.tsv data from the data folder.
    return pd.read_csv(file_path, sep='\t')

def save_data(life_expectancy_df: pd.DataFrame, region: str) -> None:
    """Saves the dataframe to csv"""

    life_expectancy_df.to_csv(str(CURRENT_PATH) + '/data/' + region.lower() + \
                              '_life_expectancy.csv',
                              index=False)
