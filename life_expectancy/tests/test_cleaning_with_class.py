# """Tests for the cleaning module"""
# import pandas as pd

# from life_expectancy.cleaning_with_class import main
# from . import OUTPUT_DIR


# def test_main(pt_life_expectancy_expected):
#     """Run the `clean_data` function and compare the output to the expected output"""
#     main(region='PT')
#     pt_life_expectancy_actual = pd.read_csv(
#         OUTPUT_DIR / "pt_life_expectancy.csv"
#     )
#     pd.testing.assert_frame_equal(
#         pt_life_expectancy_actual, pt_life_expectancy_expected
#     )
