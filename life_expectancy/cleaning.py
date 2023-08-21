"""Module to read, clean and save to csv the life_expectancy_raw.tsv
"""
# Imports
import argparse
from pathlib import Path
import pandas as pd

# Constants
CURRENT_PATH = Path(__file__).parent

# Functions
def load_data(file_path: str) -> pd.DataFrame:
    """Loads tsv file to pandas dataframe

    Parameters
    ----------
    file_path : str
        path of the tsv file to be read

    Returns
    -------
    pd.DataFrame
        loaded data
    """
    # Loads the eu_life_expectancy_raw.tsv data from the data folder.
    return pd.read_csv(file_path, sep='\t')

def _split_columns_into_several(life_expectancy_df: pd.DataFrame) -> pd.DataFrame:
    """Split the first column of the dataframe into several"""
    # Unpivots the date to long format, so that we have the following columns:
    # unit, sex, age, region, year, value.
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
    # unpivot the dataframe
    return pd.melt(life_expectancy_df, id_vars=life_expectancy_df.columns[0:4],
                                 value_vars=life_expectancy_df.columns[4:],
                                 var_name='year')

def _remove_nans(life_expectancy_df: pd.DataFrame) -> pd.DataFrame:
    """cleaning value column and removing missing values"""
    # cleaning of the column value
    life_expectancy_df['value'] = pd.DataFrame(life_expectancy_df.value.str.strip(' epb:'))

    # Remove NaNs from 'value
    life_expectancy_df = life_expectancy_df[life_expectancy_df['value']!=''].reset_index(drop=True)

    return life_expectancy_df

def _cast_types(life_expectancy_df: pd.DataFrame) -> pd.DataFrame:
    """cast columns year and value to int and float, respectivly"""
    return life_expectancy_df.astype({'year': 'int', 'value': 'float'})

def _filter_region(life_expectancy_df: pd.DataFrame, region: str) -> pd.DataFrame:
    """Filters only the data where region equal to the desired region"""
    return life_expectancy_df[life_expectancy_df.region==region]

def save_data(life_expectancy_df: pd.DataFrame, region: str) -> None:
    """Saves the dataframe to csv"""
    life_expectancy_df.to_csv(str(CURRENT_PATH) + '/data/' + region.lower() + \
                              '_life_expectancy.csv',
                              index=False)

def clean_data(life_expectancy_df: pd.DataFrame, region: str) -> pd.DataFrame:
    """
    Function to preprocess and clean data.

    Parameters
    ----------
    life_expectancy_df : pd.DataFrame
        Pandas dataframe with the original data (imported using load_data)
    region : str
        Region to filter the data (e.g.: 'PT' for Portugal)

    Returns
    -------
    pd.DataFrame
        Pandas dataframe with cleaned data.
    """

    return (
        life_expectancy_df
        .pipe(_split_columns_into_several) # split columns into several
        .pipe(_unpivot_dataframe) # Unpivots dataframe
        .pipe(_remove_nans) # Clean and remove nans
        .pipe(_cast_types) # Ensures 'year' is an int and 'value' to float
        .pipe(_filter_region, region=region) # Filters data for the specifyed region.
    )

def main(region: str = 'PT') -> None:
    "main function to import, clean and save cleaned data"
    # File path
    file_path = Path(CURRENT_PATH,
                     'data', 
                     'eu_life_expectancy_raw.tsv')

    life_expectancy_df = load_data(file_path=file_path)

    life_expectancy_df_cleaned = clean_data(life_expectancy_df, region=region)

    save_data(life_expectancy_df_cleaned, region=region)

if __name__ == '__main__': # pragma: no cover
    # parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--region', type=str, required=False, default='PT')
    args = parser.parse_args()

    # function call
    main(region=args.region)
