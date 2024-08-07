"""
Convert a csv file to DataFrame, then call the method update.update_chapter on the DataFrame.
Convert the returned DataFrame back to a csv file.
"""

from pathlib import PurePath
import pandas as pd
from pyvirtualdisplay.display import Display
import auto_update.update as update


async def auto_update_csv(file: PurePath):
    """
    Given a csv file with novel links and chapters, output a csv file with updated chapters in the same folder.
    For example, given new.csv, it would output new_out.csv.

    :param file: the PurePath of the input csv file
    """
    df = csv_to_dataframe(file)
    with Display(visible=False, size=(1080,720)):
        df_new = await update.update_chapter(df)
    base_name = PurePath(file).stem
    output_file_name = base_name + "_out.csv"
    csv_path = PurePath(file.parent, output_file_name)
    file = dataframe_to_csv(df_new, csv_path)


def csv_to_dataframe(file: PurePath) -> pd.DataFrame:
    """
    Convert the csv to a pandas Dataframe

    :param file: the PurePath of the input csv file
    :return: the converted pandas Dataframe
    """
    df_out = pd.read_csv(file, sep=',', on_bad_lines='skip')
    return df_out


def dataframe_to_csv(df: pd.DataFrame, csv_path: PurePath) -> PurePath:
    """
    Convert the pandas Dataframe to a PurePath of a csv file

    :param df: the pandas Dataframe to be converted
    :param csv_path: the PurePath for the csv file to be saved at
    :return: the PurePath of the output csv file
    """
    csv_new = df.to_csv(csv_path, mode='w+', sep=',', header=True, index=False)
    csv_new = PurePath(str(csv_new))
    return csv_new
