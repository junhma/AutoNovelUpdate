"""Convert a csv file to DataFrame and back to a csv file."""
import logging
from pathlib import PurePath

import pandas as pd
from requests import HTTPError

import auto_update.web_parser as web_parser
from auto_update.exceptions import (ChapterNotFoundException,
                                    MissingParserException,
                                    TitleNotFoundException)


def auto_update(file: PurePath):
    """
    Given a csv file with novel links and chapters, output a csv file with updated chapters in the same folder.

    :param file: the PurePath of the input csv file
    """
    my_df = csv_to_dataframe(file)
    update_chapter(my_df)
    base_name = PurePath(file).stem
    output_file_name = base_name + "_out.csv"
    csv_path = PurePath(file.parent, output_file_name)
    file = dataframe_to_csv(my_df, csv_path)


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


def update_chapter(my_df: pd.DataFrame) -> pd.DataFrame:
    """
    Update the chapter of the DataFrame, return the updated DataFrame.

    :param my_df: the pandas Dataframe to be updated
    :return: the updated pandas Dataframe
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(f"{__name__}.log", mode='w')
    formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    for i in range(my_df.shape[0]):
        try:
            link = str(my_df.loc[i, 'link'])
            parser = str(my_df.loc[i, 'parser'])
            updated_dictionary = pass_to_parser(link, parser)
            my_df.loc[i, 'latest_chapter'] = updated_dictionary['latest_chapter']
        except (MissingParserException) as e:
            error_message = f"{e.__class__.__name__}: {e.msg} - {my_df.loc[i, 'title']}"
            logger.info(error_message)
        except (HTTPError) as e:
            error_message = f"{e.__class__.__name__}: {e.response.status_code} - {my_df.loc[i, 'title']}"
            logger.exception(error_message)
        except (TitleNotFoundException, ChapterNotFoundException) as e:
            error_message = f"{e.__class__.__name__}: {e.msg} - {my_df.loc[i, 'title']}"
            logger.exception(error_message)
        except Exception as e:
            error_message = f"Unexpected Exception: {e.__class__.__name__} - {my_df.loc[i, 'title']}"
            logger.exception(error_message)
    return my_df


def pass_to_parser(link: str, parser: str) -> dict[str, str]:
    """
    Choose which parser to use based on choices noted in the csv, then pass the link of the novel to web_parser.

    :param link: a string of the link of the novel
    :param parser: a string of the name of the parser of the novel
    :return: a dictionary of the updated information of the novel from web_parser
    :raises MissingParserException: no parser applies to the novel
    """
    if (parser == 'syosetu'):
        updated_dictionary = web_parser.syosetuAPI(link)
    elif (parser == 'novel_updates'):
        updated_dictionary = web_parser.novel_updates(link)
    else:
        raise MissingParserException
    return updated_dictionary
