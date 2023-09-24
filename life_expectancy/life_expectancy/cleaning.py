"""Module to read, clean and save to csv the life_expectancy_raw.tsv
"""
# Imports
import argparse
from pathlib import Path
import pandas as pd

# Local imports
from .load_save import load_data
from .load_save import save_data

# Constants
CURRENT_PATH = Path(__file__).parent.parent
EU_LIFE_EXPECTANCY_DATA_RAW_PATH = Path(CURRENT_PATH,
                                        'data', 
                                        'eu_life_expectancy_raw.tsv')
# Functions
def _split_columns_into_several(life_expectancy_df: pd.DataFrame) -> pd.DataFrame:
    """Split the first column of the dataframe into several.
    Unpivots the date to long format, so that we have the following columns:
    unit, sex, age, region, year, value.
    """

    return pd.concat(
        [
            pd.DataFrame(life_expectancy_df['unit,sex,age,geo\\time'].str.split(',').to_list(),
                        columns=['unit', 'sex', 'age', 'region']),
            life_expectancy_df.iloc[:,1:]
        ],
        axis=1
    )


def _unpivot_dataframe(life_expectancy_df: pd.DataFrame) -> pd.DataFrame:
    """Unpivot the life_expenctancy_df dataframe"""

    return pd.melt(life_expectancy_df, id_vars=life_expectancy_df.columns[0:4],
                                 value_vars=life_expectancy_df.columns[4:],
                                 var_name='year')


def _cleaning_value_column(life_expectancy_df: pd.DataFrame) -> pd.DataFrame:
    """cleaning value column"""

    life_expectancy_df['value'] = pd.DataFrame(life_expectancy_df.value.str.strip(' epb:'))

    return life_expectancy_df


def _remove_nans_from_column_value(life_expectancy_df: pd.DataFrame) -> pd.DataFrame:
    """Remove NaNs from 'value' column"""

    return life_expectancy_df[life_expectancy_df['value']!=''].reset_index(drop=True)


def _cast_types(life_expectancy_df: pd.DataFrame) -> pd.DataFrame:
    """cast columns year and value to int and float, respectivly"""
    return life_expectancy_df.astype({'year': 'int', 'value': 'float'})


def filter_region(life_expectancy_df: pd.DataFrame, region: str) -> pd.DataFrame:
    """Filters only the data where region equal to the desired region"""

    return life_expectancy_df[life_expectancy_df.region==region]


def clean_data(life_expectancy_df: pd.DataFrame) -> pd.DataFrame:
    """Function to preprocess and clean data."""

    return (
        life_expectancy_df
        .pipe(_split_columns_into_several) # split columns into several
        .pipe(_unpivot_dataframe) # Unpivots dataframe
        .pipe(_cleaning_value_column) # Cleaning the 'value' column
        .pipe(_remove_nans_from_column_value) # Remove nans from the value column
        .pipe(_cast_types) # Ensures 'year' is an int and 'value' to float
    )


def main(region: str = 'PT') -> None:
    """main function to import, clean and save cleaned data.
    region (str, optional) is the code of the region to filter the data, by default 'PT'
    """
    # file_path: Path = EU_LIFE_EXPECTANCY_DATA_RAW_PATH
    file_path = Path(CURRENT_PATH,
                    'data', 
                    'eu_life_expectancy_raw.tsv')

    life_expectancy_df = load_data(file_path=file_path)

    life_expectancy_df_cleaned = clean_data(life_expectancy_df)

    life_expectancy_df_cleaned_filtered = filter_region(life_expectancy_df_cleaned, region=region)

    save_data(life_expectancy_df_cleaned_filtered, region=region)

    return life_expectancy_df_cleaned_filtered


if __name__ == '__main__': # pragma: no cover
    # parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--region', type=str, required=False, default='PT')
    args = parser.parse_args()

    # function call
    main(region=args.region)
