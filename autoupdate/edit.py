"""Convert a csv file to dataframe and back to a csv file."""
from pathlib import Path, PurePath
import pandas as pd
import autoupdate.web_parser as web_parser

def convert(file, base_folder):
    """Convert a csv file to dataframe and back to a csv file."""
    my_df = pd.read_csv(file, sep = ',', on_bad_lines='skip')  # csv to dataframe

    update(my_df)

    BASE_NAME = PurePath(file).name
    out_path = Path(base_folder, BASE_NAME)

    file = my_df.to_csv(out_path, mode='w+', sep = ',', 
                        header = True, index = False)  
                        # dataframe to csv


def update(my_df):
    """Update the chapter of the dataframe, return the updated dataframe."""
    for i in range(my_df.shape[0]):
        try:
            link = my_df.loc[i, 'link']
            parser = my_df.loc[i, 'parser']

            updated_dictionary = choose(link, parser)

            if (updated_dictionary['latest_chapter'] != -1):
                my_df.loc[i, 'latest_chapter'] = updated_dictionary['latest_chapter']
            else:
                print(my_df.loc[i, 'title'])

        except ValueError:
            print(my_df.loc[i, 'title'])

    return my_df


def choose(link, parser):
    """Choose which parser to use based on choices noted in the csv."""

    if (parser == 'syosetu'):
        updated_dictionary = web_parser.syosetu(link)
    elif (parser == 'novel_updates'):
        updated_dictionary = web_parser.novel_updates(link)
    else:
        updated_dictionary = {'title': "",
                          'latest_chapter': -1,
                          'link': ""}

    return updated_dictionary