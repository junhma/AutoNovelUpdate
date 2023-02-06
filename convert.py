"""Convert a csv file to dataframe and back to a csv file."""
import pandas as pd
import cloudscraper
from web_parser import syosetsu

def convert(file):
    """Convert a csv file to dataframe and back to a csv file."""
    my_df = pd.read_csv(file)  # csv to dataframe


    for i in range(my_df.shape[0]):
        update(my_df.iloc[i,:]) # pass the ith row

    new_file = my_df.to_csv()  # dataframe to csv
    return new_file


def update(series):
    """Update the chapter of the series, return the updated series."""

    link = series.loc("link")

    # create cloudScraper instance
    scraper = cloudscraper.create_scraper()

    # make request
    req = scraper.get(link)
    updated_chapter = syosetsu(req)
    if (updated_chapter["latest_chapter"] !=
        series.loc["latest_chapter"]):
        series.loc["latest_chapter"] = updated_chapter["latest_chapter"]

    return series

# choose parser function
# https://ncode.syosetu.com/novelview/infotop/ncode/n9629ex/