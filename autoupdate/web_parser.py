"""Parsers for novel sites"""
from pathlib import Path
import re
import cloudscraper
from bs4 import BeautifulSoup as bs


def syosetu(link):
    """Parser for syosetu.

    Takes a link,
    returns a dictionary.
    """

    title = "NA"
    latest_chapter = -1

    scraper = cloudscraper.create_scraper()
    req = scraper.get(link)

    if req.status_code == 404:
        raise ValueError

    soup = bs(req.content, 'xml')
    
    # find title
    if (soup.find('meta',
                    {'property': "og:title"})):
        meta_title_tag = soup.find('meta', {'property': "og:title"})
        title = meta_title_tag["content"]
    else:
        raise ValueError

    # find latest chapter
    if (soup.find(string = re.compile("全\d?,?\d{1,3}部分"))):
        # string looks like "全1,145部分"
        string = soup.find(string = re.compile("全\d?,?\d{1,3}部分"))
        # num is [1, 145] when chapter is more than 3 digits, [145] when less.
        nums = re.findall(r"\d+", string)
        # concatnate the 2 numbers
        latest_chapter = int("".join(nums))
    else:
        raise ValueError
    
    updated_dictionary = {'title': title,
                          'latest_chapter': latest_chapter,
                          'link': req.url}
    
    return updated_dictionary


def novel_updates(link):
    """ Parser for novel updates.

    Takes a link,
    returns a dictionary
    """

    title = "NA"
    latest_chapter = -1
    english_publisher = "None"

    scraper = cloudscraper.create_scraper()
    req = scraper.get(link)
    if req.status_code == 404:
        raise ValueError

    soup = bs(req.content, 'xml')

    # split page in parts
    page = soup.find('div', class_ = "w-blog-content")
    body = page.find('div', class_ = "g-cols wpb_row offset_default")
    # "wpb_text_column " has a space at the end
    one_third = body.find('div',
                class_ = "one-third").find('div',
                class_ = "wpb_text_column ").find('div', 
                class_ =  "wpb_wrapper")
    two_thirds = body.find('div',
                class_ = "two-thirds").find('div',
                class_ = "wpb_text_column ").find('div',
                class_ = "wpb_wrapper") 

    # find title
    if (page.find('div', class_ = "seriestitlenu")):
        title = page.find('div', class_ = "seriestitlenu").text
    else:
        raise ValueError
    
    # find English publisher
    if (one_third.find('div', id = "showepublisher").find('a')):
        english_publisher = one_third.find('div',
                            id = "showepublisher").find('a').text

    # find latest chapter
    if (two_thirds.find('table', id = "myTable")):
        rel = two_thirds.find('table', id = "myTable").find('tbody').find('tr')
        string = rel.select('td')[2].find('a').get('title')
        # find all the numbers in for example"c11-c12"
        nums = re.findall(r"\d+", string)
        # choose the last number
        latest_chapter = int(nums[-1])
    else:
        raise ValueError 
             
    updated_dictionary = {'title': title,
                          'latest_chapter': latest_chapter,
                          'link': req.url, 
                          'english_publisher': english_publisher}

    return updated_dictionary
