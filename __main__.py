from pathlib import Path
import autoupdate.edit as edit


BASE_FOLDER = Path(__file__).parent.resolve()
BASE_NAME = r"reading_list.csv"
file = Path(BASE_FOLDER, BASE_NAME)
"""
edit.convert(file, BASE_FOLDER)
"""

import pandas
import pathlib
my_df = pandas.read_csv(file, sep = ',', on_bad_lines='skip')  # csv to dataframe


for i in range(my_df.shape[0]):
    try:
        link = my_df.loc[i, 'link']
        parser = my_df.loc[i, 'parser']

        updated_dictionary = edit.choose(link, parser)

        if (updated_dictionary['latest_chapter'] != -1):
            my_df.loc[i, 'latest_chapter'] = updated_dictionary['latest_chapter']
    except ValueError:
        print(my_df.loc[i, 'title'], my_df.loc[i, 'parser'])
        #value error trash of the count family latest chapter
