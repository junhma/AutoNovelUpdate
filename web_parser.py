"""Parsers for novel sites"""
import re
from bs4 import BeautifulSoup as bs

def syosetsu(req):
    """Parser for syosetsu

    take a request made from cloudscraper instance
    returns a dictionary
    """
    if req.status_code == 404:
        raise ValueError

    soup = bs(req.text, "html.parser")

    # find title
    if soup.find("meta",
                 {"property": "og:title"}):
        meta_title_tag = soup.find("meta",
                                   {"property": "og:title"})
        title = meta_title_tag["content"]
    else:
        print("No title tag found.")

    # find latest chapter
    latest_chapter = int()
    if soup.find("span", {"id": "noveltype_notend"}):
        string = soup.find("span", {"id": "noveltype_notend"}).next_sibling
        latest_chapter = int(re.findall("\d+", string)[0])
    else:
        print("No latest chapter tag found.")

    updated_dictionary = {"title": title,
                          "latest_chapter": latest_chapter,
                          "link": req.url}

    return updated_dictionary

def parse_novel_updates(req):
    """Parser for novel updates

    take a request made from cloudscraper instance
    returns a dictionary
    """
    if req.status_code == 404:
        raise ValueError
    soup = bs(req.text, "html.parser")

    # split page in parts
    page = soup.find("div", class_="w-blog-content")
    body = page.find("div", class_="g-cols wpb_row offset_default")
    one_third = body.find("div",
                        class_="one-third").find("div",
                        class_="wpb_text_column").find("div", class_="wpb_wrapper")
    two_thirds = body.find("div",
                        class_="two-thirds").find("div",
                        class_="wpb_text_column").find("div", class_="wpb_wrapper")

    # find title
    title = page.find("div", class_="seriestitlenu").text

    # find English publisher
    english_publisher = []
    if one_third.find("div", id="showepublisher").find("a") is not None:
        english_publisher = {"name": one_third.find("div",
            id="showepublisher").find("a").text,
            "link": one_third.find("div",
            id="showepublisher").find("a").get("href")}
    else:
        english_publisher = None

    # find latest chapter
    latest_chapter = []
    if two_thirds.find("table", id="myTable") is not None:
        rel = two_thirds.find("table", id="myTable").find("tbody").find("tr")
        release = rel.select("td")[2].find("a").get("title")
        latest_chapter = release
    else:
        latest_chapter = None

    updated_dictionary = {"title": title,
        "latest_chapter": latest_chapter,
        "link": req.url, "english_publisher": english_publisher}

    return updated_dictionary