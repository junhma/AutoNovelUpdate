"""Parsers for novel sites"""
import re

import cloudscraper
from bs4 import BeautifulSoup as bs
from auto_update.exceptions import Exception404, TitleNotFoundException, ChapterNotFoundException


def syosetu(link: str) -> dict[str]:
    """
    Parser for https://ncode.syosetu.com/.

    :param link: a string of the link of the novel
    :return: a dictionary of the updated information of the novel
    :raises Exception404: a 404 error from a request
    :raises TitleNotFoundException: can't find title in soup
    :raises ChapterNotFoundException: can't find chapter in soup
    """

    title = "NA"
    latest_chapter = -1

    scraper = cloudscraper.create_scraper()
    req = scraper.get(link)

    if req.status_code == 404:
        raise Exception404

    soup = bs(req.content, 'xml')

    # find title
    try:
        if (soup.find('meta',
                    {'property': "og:title"})):
            meta_title_tag = soup.find('meta', {'property': "og:title"})
            title = meta_title_tag["content"]
        else:
            raise TitleNotFoundException
    except AttributeError:
            raise TitleNotFoundException

    # find latest chapter
    try:
        if (soup.find(string=re.compile("全\d?,?\d{1,3}部分"))): # string looks like "全1,145部分"
            string = soup.find(string=re.compile("全\d?,?\d{1,3}部分"))
            # The chapter number is a list like [1, 145], when it is more than 3 digits. 
            # It is one number in a list like [145] when less.
            nums = re.findall(r"\d+", string) # concatenate numbers in the list
            latest_chapter = int("".join(nums))
        else:
            raise ChapterNotFoundException
    except AttributeError:
            raise ChapterNotFoundException

    updated_dictionary = {'title': title,
                          'latest_chapter': latest_chapter,
                          'link': req.url}

    return updated_dictionary


def novel_updates(link: str) -> dict[str]:
    """
    Parser for https://www.novelupdates.com/.

    :param link: a string of the link of the novel
    :return: a dictionary of the updated information of the novel
    """

    title = "NA"
    latest_chapter = -1
    english_publisher = "None"

    scraper = cloudscraper.create_scraper()
    req = scraper.get(link)
    if req.status_code == 404:
        raise Exception404

    soup = bs(req.content, 'xml')

    # split page in parts
    page = soup.find('div', class_="w-blog-content")
    body = page.find('div', class_="g-cols wpb_row offset_default")

    # "wpb_text_column " has a space at the end
    one_third = body.find('div',
                          class_="one-third").find('div',
                                                   class_="wpb_text_column ").find('div',
                                                                                   class_="wpb_wrapper")

    # find title
    try:
        if (page.find('div', class_="seriestitlenu")):
            title = page.find('div', class_="seriestitlenu").text
        else:
            raise TitleNotFoundException
    except AttributeError:
            raise TitleNotFoundException

    # find English publisher
    if (one_third.find('div', id="showepublisher").find('a')):
            english_publisher = one_third.find('div',
                                            id="showepublisher").find('a').text

    # find latest chapter
    try:
        if (body.find('table', id="myTable")):
            rel = body.find('table', id="myTable").find('tbody').find('tr')
            string = rel.select('td')[2].find('span').get('title')
            # find all the numbers in for example"c11-c12"
            nums = re.findall(r"\d+", string)
            # choose the last number
            latest_chapter = int(nums[-1])
        else:
            raise ChapterNotFoundException
    except AttributeError:
            raise ChapterNotFoundException

    updated_dictionary = {'title': title,
                          'latest_chapter': latest_chapter,
                          'link': req.url,
                          'english_publisher': english_publisher}

    return updated_dictionary
