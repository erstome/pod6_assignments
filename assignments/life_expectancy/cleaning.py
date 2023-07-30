"""aaa
"""
# Imports
import os
import pandas as pd

# Functions
def clean_data() -> pd.DataFrame:
    """_summary_

    Returns
    -------
    _type_
        _description_
    """
    
    # File path
    file_path = os.path.join(os.path.dirname(__file__),
                             './data/')
    
    # Loads the eu_life_expectancy_raw.tsv data from the data folder.
    data = pd.read_csv(file_path + 'eu_life_expectancy_raw.tsv', sep='\t')
    
    # Unpivots the date to long format, so that we have the following columns:
    # unit, sex, age, region, year, value.
    data = pd.concat(
        [
            pd.DataFrame(data['unit,sex,age,geo\\time'].str.split(',').to_list(),
                        columns=['unit', 'sex', 'age', 'region']),
            data.iloc[:,1:]
        ],
        axis=1
    )

    data = pd.melt(data, id_vars=data.columns[0:4], value_vars=data.columns[4:],
                   var_name='year')
    
    # Ensures year is an int (with the appropriate data cleaning if required)
    data = data.astype({'year': 'int'})

    # Ensures value is a float (with the appropriate data cleaning if required,
    # and do remove the NaNs).
    ## Remove NaNs from 'value
    data = data[data['value']!=': '].reset_index(drop=True)

    ## cleaning of the column value
    data['value'] = pd.DataFrame(data.value.str.split(' ').to_list())[0].values

    ## 'value' to float
    data = data.astype({'value': 'float'})

    # Filters only the data where region equal to PT (Portugal).
    data = data[data.region=='PT']

    # Save the resulting data frame to the data folder as pt_life_expectancy.csv. 
    # Ensure that no numerical index is saved.
    data.to_csv(file_path + 'pt_life_expectancy.csv', index=False)


if __name__ == '__main__':
    clean_data()
    