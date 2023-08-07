from pathlib import Path
import argparse
import pandas as pd


CURRENT_DIR = str(Path(__file__).parent)


class LifeExpectancyData:
    """Life Expectancy Data Structure"""
    def __init__(self, path) -> None:
        self.life_expectancy_df = self._read_tsv_file_to_pandas_dataframe(path)

    @staticmethod
    def _read_tsv_file_to_pandas_dataframe(path: str) -> pd.DataFrame:
        """Reads tsv file and loads it to pandas DataFrame"""
        return pd.read_table(path)

    def get_life_expectancy_df(self) -> pd.DataFrame:
        """Returns the life expectancy DataFrame"""
        return self.life_expectancy_df

    def _set_life_expectancy_df(self, new_df: pd.DataFrame) -> None:
        """Sets the life expectancy DataFrame"""
        self.life_expectancy_df = new_df

    def split_column_into_several(self) -> pd.DataFrame:
        """Split column into several columns of a pandas DataFrame"""
        return (  # Use raw string due to \t
            self.life_expectancy_df[r"unit,sex,age,geo\time"]
            .str.split(",", expand=True)
            .rename(
                {0: "unit", 1: "sex", 2: "age", 3: "region"},
                axis=1
            )
        )

    def clean_dataframe(self) -> None:
        """Cleans the DataFrame to be in a suitable format"""
        left_df = self.split_column_into_several()
        right_df = self.life_expectancy_df.iloc[:, 1:]

        df_melted = pd.melt(
            left_df.join(right_df),
            id_vars =["unit", "sex", "age", "region"],
            value_vars=list(right_df.columns)
        ).rename({"variable": "year"}, axis=1)

        return df_melted

    def cast_columns_to_correct_types(self):
        """Cast columns to their proper types"""
        df_clean = self.clean_dataframe()
        df_clean.loc[:, "year"] = df_clean.year.str.strip()
        df_clean.loc[:, "value"] = df_clean.value.str.strip(" epb: ")

        self._set_life_expectancy_df(
            df_clean.astype({"year": "int"})  # , "value": "float"
        )


    def filter_dataset_by_region(self, region: str = "PT") -> pd.DataFrame:
        """Filter dataset by region"""
        return self.life_expectancy_df[
            (self.life_expectancy_df.region == region)
            & (self.life_expectancy_df.value != "")
        ]


def clean_data(region: str) -> None:
    """Cleans the life expectancy dataset and saves it to a csv"""
    life_expectancy = LifeExpectancyData(
        f"{CURRENT_DIR}/data/eu_life_expectancy_raw.tsv"
    )
    life_expectancy.cast_columns_to_correct_types()
    life_expectancy.get_life_expectancy_df()

    life_expectancy.filter_dataset_by_region(region).to_csv(
        f"{CURRENT_DIR}/data/pt_life_expectancy.csv", index=False
    )


if __name__ == "__main__": # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument("--region", default="PT")
    args = parser.parse_args()

    clean_data(args.region)