"""Convert a csv file to dataframe and back to a csv file."""
import pathlib
import pandas as pd
import autoupdate.web_parser as web_parser

def convert(file, base_folder):
    """Convert a csv file to dataframe and back to a csv file."""
    my_df = pd.read_csv(file)  # csv to dataframe

    update(my_df)

    BASE_NAME = pathlib.PurePath(file).name
    out_path = pathlib.Path(base_folder, BASE_NAME)

    file = my_df.to_csv(out_path, mode='w+', sep = ",", header = True, index = False)  # dataframe to csv


def update(my_df):
    """Update the chapter of the dataframe, return the updated dataframe."""
    for i in range(my_df.shape[0]):

        link = my_df.loc[i, "link"]

        updated_chapter = web_parser.syosetsu(link)

        if (updated_chapter["latest_chapter"] != 0):
            my_df.loc[i, "latest_chapter"] = updated_chapter["latest_chapter"]

    return my_df

# choose parser function
# https://ncode.syosetu.com/novelview/infotop/ncode/n9629ex/