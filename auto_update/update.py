"""Update the chapter of the DataFrame, return the updated DataFrame."""
import logging

import pandas as pd
from requests import HTTPError

import auto_update.web_parser as web_parser
from auto_update.exceptions import (ChapterNotFoundException,
                                    MissingParserException,
                                    NcodeNotFoundException)

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
            updated_dictionary = pass_to_parser(link)
            my_df.loc[i, 'latest_chapter'] = updated_dictionary['latest_chapter']
        except MissingParserException as e:
            error_message = f"{e.__class__.__name__}: {e.msg} - {my_df.loc[i, 'title']}"
            logger.info(error_message)
        except HTTPError as e:
            error_message = f"{e.__class__.__name__}: {e.response.status_code} - {my_df.loc[i, 'title']}"
            logger.exception(error_message)
        except NcodeNotFoundException as e:
            error_message = f"{e.__class__.__name__}: {e.msg} - {my_df.loc[i, 'title']}"
            logger.exception(error_message)
        except ChapterNotFoundException as e:
            error_message = f"{e.__class__.__name__}: {e.msg} - {my_df.loc[i, 'title']}"
            logger.exception(error_message)
        except Exception as e:
            error_message = f"Unexpected Exception: {e.__class__.__name__} - {my_df.loc[i, 'title']}"
            logger.exception(error_message)
    return my_df

def pass_to_parser(link: str) -> dict[str, int]:
    """
    Detect which parser to use based the link, then pass the link of the novel to web_parser.

    :param link: a string of the link of the novel
    :return: a dictionary of the updated information of the novel from web_parser
    :raises MissingParserException: no parser applies to the novel
    """
    # Choose syosetu if the link contains "ncode.syosetu.com"
    if "ncode.syosetu.com" in link:
        updated_dictionary = web_parser.syosetuAPI(link)
    # Choose novel_updates if the link contains "novelupdates.com"
    elif "novelupdates.com" in link:
        updated_dictionary = web_parser.novel_updates(link)
    else:
        raise MissingParserException
    return updated_dictionary
