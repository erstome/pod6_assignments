"""Module to read, clean and save to csv the life_expectancy_raw.tsv
"""
# Imports
import argparse
from pathlib import Path
import pandas as pd

# Constants
CURRENT_PATH = Path(__file__).parent

# Functions
def read_tsv_file_to_pandas_dataframe(file_path: str) -> pd.DataFrame:
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

def split_columns_into_several(life_expectancy_df: pd.DataFrame) -> pd.DataFrame:
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

def unpivot_dataframe(life_expectancy_df: pd.DataFrame) -> pd.DataFrame:
    """Unpivot the life_expenctancy_df dataframe"""
    # unpivot the dataframe
    return pd.melt(life_expectancy_df, id_vars=life_expectancy_df.columns[0:4],
                                 value_vars=life_expectancy_df.columns[4:],
                                 var_name='year')

def remove_nans(life_expectancy_df: pd.DataFrame) -> pd.DataFrame:
    """cleaning value column and removing missing values"""
    # cleaning of the column value
    life_expectancy_df['value'] = pd.DataFrame(life_expectancy_df.value.str.strip(' epb:'))

    # Remove NaNs from 'value
    life_expectancy_df = life_expectancy_df[life_expectancy_df['value']!=''].reset_index(drop=True)

    return life_expectancy_df

def cast_types(life_expectancy_df: pd.DataFrame) -> pd.DataFrame:
    """cast columns year and value to int and float, respectivly"""
    return life_expectancy_df.astype({'year': 'int', 'value': 'float'})

def filter_region(life_expectancy_df: pd.DataFrame, region: str) -> pd.DataFrame:
    """Filters only the data where region equal to the desired region"""
    return life_expectancy_df[life_expectancy_df.region==region]

def save_dataframe_to_csv(life_expectancy_df: pd.DataFrame, region: str) -> None:
    """Saves the dataframe to csv"""
    life_expectancy_df.to_csv(str(CURRENT_PATH) + '/data/' + region.lower() + \
                              '_life_expectancy.csv',
                              index=False)

def clean_data(region: str = 'PT') -> None:
    """
    Function to import, clean and save data.
    Saves to a *.csv file.
    """
    # File path
    file_path = Path(CURRENT_PATH,
                     'data', 
                     'eu_life_expectancy_raw.tsv')

    # Loads the eu_life_expectancy_raw.tsv data from the data folder.
    life_expectancy_df = read_tsv_file_to_pandas_dataframe(file_path)

    # split columns into several
    life_expectancy_df = split_columns_into_several(life_expectancy_df)

    # Unpivots dataframe
    life_expectancy_df = unpivot_dataframe(life_expectancy_df)

    # Clean and remove nans
    life_expectancy_df = remove_nans(life_expectancy_df)

    # Ensures 'year' is an int and 'value' to float
    life_expectancy_df = cast_types(life_expectancy_df)

    # Filters data for the specifyed region.
    life_expectancy_df = filter_region(life_expectancy_df=life_expectancy_df,
                                       region=region)

    # Save the resulting data frame to the data folder as pt_life_expectancy.csv.
    # Ensure that no numerical index is saved.
    save_dataframe_to_csv(life_expectancy_df, region=region)


if __name__ == '__main__': # pragma: no cover
    # parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--region', type=str, required=False, default='PT')
    args = parser.parse_args()

    # function call
    clean_data(region=args.region)
