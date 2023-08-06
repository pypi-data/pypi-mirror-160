import pandas as pd

COUNTRIES = {
    "belgium": {"abbrv": "B", "tiers": [1]},
    "england": {"abbrv": "E", "tiers": [0, 1, 2, 3, "C"]},
    "france": {"abbrv": "F", "tiers": [1, 2]},
    "germany": {"abbrv": "D", "tiers": [1, 2]},
    "greece": {"abbrv": "G", "tiers": [1]},
    "italy": {"abbrv": "I", "tiers": [1, 2]},
    "portugal": {"abbrv": "P", "tiers": [1]},
    "scotland": {"abbrv": "SC", "tiers": [0, 1, 2, 3]},
    "spain": {"abbrv": "SP", "tiers": [1, 2]},
    "turkey": {"abbrv": "T", "tiers": [1]},
}


def list_countries() -> list:
    """
    Lists all the countries currently available
    """
    countries = list(COUNTRIES.keys())
    return countries


def _season_code(season_start_year):
    season_str = str(season_start_year)[-2:] + str(season_start_year + 1)[-2:]
    return season_str


def fetch_data(country: str, season_start_year: int, division: int) -> pd.DataFrame:
    """
    Fetches the requested data from football-data.co.uk

    Parameters
    ----------
    country : string
        The name of the country of interest
    season_start_year : int
        The year the season started, e.g. `2018` for the 2018/2019 season
    division : int
        The division's level, where `0` is the top tier, `1` is the second tier etc

    Examples
    --------
    >>> import penaltyblog as pb
    >>> pb.footballdata.fetch("England", 2018, 0)

    Returns
    -------
    Returns a Pandas dataframe containing the requested data
    """
    if country.lower() not in COUNTRIES:
        raise ValueError("Country not recognised")
    country_code = COUNTRIES[country.lower()]["abbrv"]

    if division > len(COUNTRIES[country.lower()]["tiers"]):
        raise ValueError("Division not recognised")
    division_code = COUNTRIES[country.lower()]["tiers"][division]

    season_str = _season_code(season_start_year)

    base_url = (
        "https://www.football-data.co.uk/mmz4281/{season}/{country}{division}.csv"
    )

    url = base_url.format(
        season=season_str, country=country_code, division=str(division_code)
    )

    df = pd.read_csv(url)
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

    return df
