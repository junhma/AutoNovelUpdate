"""Update the chapter of the DataFrame, return the updated DataFrame."""
import logging
from typing import Optional, Dict
import pandas as pd
import asyncio
from auto_update.web_parser import syosetuAPI, novel_updates, book_walker, book_meter
from auto_update.exceptions import (ChapterNotFoundException,
                                    MissingParserException,
                                    NcodeNotFoundException)

async def update_chapter(df: pd.DataFrame) -> pd.DataFrame:
    """
    Update the chapter of the DataFrame, return the updated DataFrame.

    :param df: the pandas Dataframe to be updated
    :return: the updated pandas Dataframe
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(f"{__name__}.log", mode='w')
    formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    tasks = [process_row(df, i) for i in range(df.shape[0])]
    results = await asyncio.gather(*tasks)
    for result in results:
        index = result['index']
        latest_chapter = result['latest_chapter']
        if latest_chapter is not None and index is not None:
            df.loc[index, 'latest_chapter'] = latest_chapter
    return df

async def process_row(df: pd.DataFrame, index: int) -> Dict[str, Optional[int]]:
    """
    Take a row of the DataFrame, return the updated latest chapter and index of the row as a dictionary.

    :param df: the row of the Dataframe to be updated
    :return: the updated latest chapter and index of the row as a dictionary.
    """
    logger = logging.getLogger(__name__)
    link = str(df.loc[index, 'link'])
    try:
        updated_dictionary = await pass_to_parser(link)
        return {"index": index, 'latest_chapter': updated_dictionary['latest_chapter']}
    except MissingParserException as e:
        error_message = f"{e.__class__.__name__}: {e.msg} - {df.loc[index, 'title']}"
        logger.info(error_message)
        return {"index": index, 'latest_chapter': None}
    except NcodeNotFoundException as e:
        error_message = f"{e.__class__.__name__}: {e.msg} - {df.loc[index, 'title']}"
        logger.exception(error_message)
        return {"index": index, 'latest_chapter': None}
    except ChapterNotFoundException as e:
        error_message = f"{e.__class__.__name__}: {e.msg} - {df.loc[index, 'title']}"
        logger.exception(error_message)
        return {"index": index, 'latest_chapter': None}
    except Exception as e:
        error_message = f"Unexpected Exception: {e.__class__.__name__} - {df.loc[index, 'title']}"
        logger.exception(error_message)
        return {"index": index, 'latest_chapter': None}

async def pass_to_parser(link: str) -> dict[str, int]:
    """
    Detect which parser to use based the link, then pass the link of the novel to web_parser.

    :param link: a string of the link of the novel
    :return: a dictionary of the updated information of the novel from web_parser
    :raises MissingParserException: no parser applies to the novel
    """
    # Choose syosetu if the link contains "ncode.syosetu.com"
    if "ncode.syosetu.com" in link:
        updated_dictionary = await syosetuAPI(link)
    # Choose novel_updates if the link contains "novelupdates.com"
    elif "novelupdates.com" in link:
        updated_dictionary = await novel_updates(link)
    # Choose book_walker if the link contains "bookwalker.jp"
    elif "bookwalker.jp" in link:
        updated_dictionary = await book_walker(link)
    # Choose book_meter if the link contains "bookmeter.com"
    elif "bookmeter.com" in link:
        updated_dictionary = await book_meter(link)
    else:
        raise MissingParserException
    return updated_dictionary
