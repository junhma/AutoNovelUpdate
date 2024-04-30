"""Parsers for novel sites"""
import re

import cloudscraper
import requests
from bs4 import BeautifulSoup as bs
from requests import URLRequired
from auto_update.exceptions import (ChapterNotFoundException, NcodeNotFoundException)


def syosetuAPI(link: str) -> dict[str, int]:
    """
    Parser for https://ncode.syosetu.com/.

    :param link: a string of the link of the novel
    :return: a dictionary of the updated information of the novel
    :raises HTTPError: HTTP error from a request
    :raises URLRequired: unable to extract ncode from link
    """

    # Define a regular expression pattern to extract the ncode part
    # example url: "https://ncode.syosetu.com/n3930eh/"
    # We are trying to extract "n3930eh".
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

    response = requests.get(url_with_params)
    response.raise_for_status()  # Check for HTTP errors

    # Store it in a dictionary
    syosetu_data = response.json()

    latest_chapter = syosetu_data[1]['general_all_no']
    updated_dictionary = {'latest_chapter': latest_chapter}

    return updated_dictionary


def novel_updates(link: str) -> dict[str, int]:
    """
    Parser for https://www.novelupdates.com/.

    :param link: a string of the link of the novel
    :return: a dictionary of the updated information of the novel
    :raises HTTPError: HTTP error from a request
    :raises TitleNotFoundException: can't find title in soup
    :raises ChapterNotFoundException: can't find chapter in soup
    """

    scraper = cloudscraper.create_scraper()
    req = scraper.get(link)
    req.raise_for_status()

    soup = bs(req.content, 'xml')

    # find latest chapter
    try:
        page = soup.find('div', class_="w-blog-content")
        body = page.find('div', class_="g-cols wpb_row offset_default")
        table = body.find('table', id="myTable") if body else None
        tr = table.find('tbody').find('tr') if table else None
        string = str(tr.select('td')[2].find('span').get('title'))
        # find all the numbers in for example"c11-c12", and choose the last number
        nums = re.findall(r"\d+", string)
        latest_chapter = int(nums[-1])
    except AttributeError:
        raise ChapterNotFoundException

    updated_dictionary = {'latest_chapter': latest_chapter}

    return updated_dictionary
