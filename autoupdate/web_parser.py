"""Parsers for novel sites"""
import re
import cloudscraper
from bs4 import BeautifulSoup as bs


def syosetsu(link):
    """Parser for syosetsu

    take a link
    returns a dictionary
    """
    tries = 10

    title = ""
    latest_chapter = 0

    for i in range(tries):
        try:
            scraper = cloudscraper.create_scraper()
            req = scraper.get(link)

            if req.status_code == 404:
               raise ValueError

            soup = bs(req.content, "xml")
            
            # find title
            if (soup.find("meta",
                          {"property": "og:title"})):
                meta_title_tag = soup.find("meta", {"property": "og:title"})
                title = meta_title_tag["content"]
            else:
                raise ValueError

            # find latest chapter
            if (soup.find("span", {"id": "noveltype_notend"})):
                string = soup.find("span", {"id": "noveltype_notend"}).next_sibling
                latest_chapter = int(re.search(r"\d+", string).group())
            else:
                raise ValueError
            
        except ValueError:
            if i < tries - 1:  # i is zero indexed
                continue
            else:
                raise
        break

    updated_dictionary = {"title": title,
                          "latest_chapter": latest_chapter,
                          "link": req.url}
    
    return updated_dictionary


def parse_novel_updates(link):
    """ Parser for novel updates

    take a link
    returns a dictionary
    """
    tries = 10

    title = ""
    latest_chapter = 0
    english_publisher = ""

    for i in range(tries):
        try:
            scraper = cloudscraper.create_scraper()
            req = scraper.get(link)
            if req.status_code == 404:
                raise ValueError

            soup = bs(req.content, "xml")

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
            if (page.find("div", class_="seriestitlenu")):
                title = page.find("div", class_="seriestitlenu").text
            else:
                raise ValueError

            # find English publisher
            if (one_third.find("div", id="showepublisher").find("a")):
                english_publisher = {"name": 
                            one_third.find("div",
                            id="showepublisher").find("a").text,
                            "link": 
                            one_third.find("div",
                            id="showepublisher").find("a").get("href")}
            else:
                raise ValueError

            # find latest chapter
            if (two_thirds.find("table", id="myTable")):
                rel = two_thirds.find("table", id="myTable").find("tbody").find("tr")
                latest_chapter = rel.select("td")[2].find("a").get("title")
            else:
                raise ValueError   
        except ValueError:
            if i < tries - 1:  # i is zero indexed
                continue
            else:
                raise
        break

    updated_dictionary = {"title": title,
                          "latest_chapter": latest_chapter,
                          "link": req.url, "english_publisher": english_publisher}

    return updated_dictionary
