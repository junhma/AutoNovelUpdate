"""Parsers for novel sites"""
import re

from auto_update.exceptions import (ChapterNotFoundException, NcodeNotFoundException)
import aiohttp
import nodriver as uc
import asyncio

async def syosetuAPI(link: str) -> dict[str, int]:
    """
    Parser for https://ncode.syosetu.com/.

    :param link: a string of the link of the novel
    :return: a dictionary of the updated information of the novel
    :raises NcodeNotFoundException: invalid ncode
    """

    # Define a regular expression pattern to extract the ncode part
    # example url: "https://ncode.syosetu.com/n3930eh/"
    # We are trying to extract "n3930eh".
    # Would not work if the ncode is not between two slashes.
    pattern = r'/n\d{4}[a-zA-Z]*/$'
    match = re.search(pattern, link)

    if match:
        ncode_with_slash = match.group(0)
        ncode = ncode_with_slash[1:-1]
    else:
        raise NcodeNotFoundException

    # Define the base URL
    base_url = 'https://api.syosetu.com/novelapi/api/'

    # Define GET parameters
    out = 'json'
    of = 'ga'  # t: title, ga: total chapter number

    # Construct the URL with the parameters
    url_with_params = f'{base_url}?out={out}&ncode={ncode}&of={of}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url_with_params) as response:
            syosetu_data = await response.json()
            latest_chapter = syosetu_data[1]['general_all_no']
            updated_dictionary = {'latest_chapter': latest_chapter}

    return updated_dictionary


async def novel_updates(link: str) -> dict[str, int]:
    """
    Parser for https://www.novelupdates.com/.

    :param link: a string of the link of the novel
    :return: a dictionary of the updated information of the novel
    :raises ChapterNotFoundException: can't find chapter by css selector
    """
    browser = await uc.start(sandbox = False)
    tab = await browser.get(link)
    try:
        css_selector = "#myTable > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(3) > span:nth-child(1)"
        tag = await tab.select(css_selector, timeout=500) 
        result = tag.text
        # Find all the numbers in for example"c11-c12", and choose the last number
        nums = re.findall(r"\d+", result)
        latest_chapter = int(nums[-1])
    except asyncio.TimeoutError:
        raise ChapterNotFoundException

    updated_dictionary = {'latest_chapter': latest_chapter}
    return updated_dictionary

async def book_walker(link: str) -> dict[str, int]:
    """
    Parser for https://bookwalker.jp/.

    :param link: a string of the link of the novel
    :return: a dictionary of the updated information of the novel
    :raises ChapterNotFoundException: Cannot find chapter by css selector
    """
    browser = await uc.start()
    tab = await browser.get(link)
    try:
        css_selector = ".overview-link > span:nth-child(1)"
        tag = await tab.select(css_selector, timeout=500) # a string that looks like <span>シリーズ14冊</span>"
        result = tag.text # a string that looks like "シリーズ14冊"
        match = re.search(r'(\d+)冊', result)
        if match:
            latest_chapter = int(match.group(1))
        else:
            raise ChapterNotFoundException 
    except asyncio.TimeoutError:
        raise ChapterNotFoundException
    
    updated_dictionary = {'latest_chapter': latest_chapter}
    return updated_dictionary


async def book_meter(link: str) -> dict[str, int]:
    """
    Parser for https://bookmeter.com.

    :param link: a string of the link of the novel
    :return: a dictionary of the updated information of the novel
    :raises ChapterNotFoundException: can't find chapter by css selector
    """
    browser = await uc.start()
    tab = await browser.get(link)
    try:
        css_selector = ".content__count"
        tag = await tab.select(css_selector, timeout=500)
        result = tag.text # The text here should be in the format of "12冊"
        match = re.search(r'(\d+)冊', result)
        if match:
            latest_chapter = int(match.group(1))
        else:
            raise ChapterNotFoundException 
    except asyncio.TimeoutError:
        raise ChapterNotFoundException
    
    updated_dictionary = {'latest_chapter': latest_chapter}
    return updated_dictionary