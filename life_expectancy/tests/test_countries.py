"Unit tests of the country module"
from life_expectancy.life_expectancy.countries import Country

def test_Country_list_of_countries():
    "Unit test of the method list_of_countries of the class enum Country"
    list_countries = Country.list_of_countries()

    assert all([len(country)==2 for country in list_countries])
