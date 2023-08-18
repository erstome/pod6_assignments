"""Module to read, clean and save to csv the life_expectancy_raw.tsv
"""
# Imports
import argparse
from pathlib import Path
import pandas as pd

# Constants
CURRENT_PATH = Path(__file__).parent

# Class
class LifeExpectancy():
    """
    Class to load, preprocess, filter and save life expectancy data.

    Parameters
    ----------
    file_path: str
        path of the tsv file to be read
    region: str
        region to filter the data. If None, saves the data for all regions. Default: 'PT'
    """
    def __init__(self, file_path: Path, region: str = 'PT') -> None:
        self.region = region
        self.life_expectancy_df = self._read_tsv_file_to_pandas_dataframe(file_path)

    @staticmethod
    def _read_tsv_file_to_pandas_dataframe(file_path: str) -> pd.DataFrame:
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

    def _split_columns_into_several(self) -> pd.DataFrame:
        """Split the first column of the dataframe into several"""
        # Unpivots the date to long format, so that we have the following columns:
        # unit, sex, age, region, year, value.
        self.life_expectancy_df = pd.concat(
            [
                pd.DataFrame(self.life_expectancy_df['unit,sex,age,geo\\time'].str.split(',')\
                             .to_list(),
                            columns=['unit', 'sex', 'age', 'region']),
                self.life_expectancy_df.iloc[:,1:]
            ],
            axis=1
        )

    def _unpivot_dataframe(self) -> pd.DataFrame:
        """Unpivot the life_expenctancy_df dataframe"""
        # unpivot the dataframe
        self.life_expectancy_df = pd.melt(self.life_expectancy_df,
                                          id_vars=self.life_expectancy_df.columns[0:4],
                                          value_vars=self.life_expectancy_df.columns[4:],
                                          var_name='year')

    def _remove_nans(self) -> pd.DataFrame:
        """cleaning value column and removing missing values"""
        # cleaning of the column value
        self.life_expectancy_df['value'] = \
            pd.DataFrame(self.life_expectancy_df['value'].str.strip(' epb:'))

        # Remove NaNs from 'value
        self.life_expectancy_df = \
            self.life_expectancy_df[self.life_expectancy_df['value']!=''].reset_index(drop=True)


    def _cast_types(self) -> pd.DataFrame:
        """cast columns year and value to int and float, respectivly"""
        self.life_expectancy_df = self.life_expectancy_df.astype({'year': 'int', 'value': 'float'})

    def _filter_region(self) -> pd.DataFrame:
        """Filters only the data where region equal to the desired region"""
        self.life_expectancy_df = \
            self.life_expectancy_df[self.life_expectancy_df.region==self.region]

    def preprocess_data(self) -> pd.DataFrame:
        "Preprocess data (split columns, unpivot dataframe, remove nans and cast types)"
        # split columns into several
        self._split_columns_into_several()

        # Unpivots dataframe
        self._unpivot_dataframe()

        # Clean and remove nans
        self._remove_nans()

        # Ensures 'year' is an int and 'value' to float
        self._cast_types()

        # Filters data for the specifyed region.
        self._filter_region()

    def save_dataframe_to_csv(self) -> None:
        """Saves the dataframe to csv"""
        # Save to disk
        self.life_expectancy_df.to_csv(str(CURRENT_PATH) + '/data/' + self.region.lower() + \
                                '_life_expectancy.csv',
                                index=False)

def main(region: str = 'PT') -> None:
    """
    Function to import, clean and save data.
    Saves to a *.csv file.
    """
    # File path
    file_path = Path(CURRENT_PATH,
                     'data', 
                     'eu_life_expectancy_raw.tsv')

    # Loads the eu_life_expectancy_raw.tsv data from the data folder.
    life_expectancy_class = LifeExpectancy(file_path=file_path, region = region)

    # Preprocess data
    life_expectancy_class.preprocess_data()

    # Save the resulting data frame to the data folder as pt_life_expectancy.csv.
    # Ensure that no numerical index is saved.
    life_expectancy_class.save_dataframe_to_csv()


if __name__ == '__main__': # pragma: no cover
    # parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--region', type=str, required=False, default='PT')
    args = parser.parse_args()

    # function call
    main(region=args.region)
