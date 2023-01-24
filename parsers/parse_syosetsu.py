# ok

# parser for syosetsu

from bs4 import BeautifulSoup as bs
import re
from novel import Novel


# REQUIRE: Request made from cloudscraper instance
# RETURN: Novel object
def parse_syosetsu(req):
    if req.status_code == 404:
        raise ValueError

    soup = bs(req.text, "html.parser")

    # find title
    if soup.find("meta", {"property": "og:title"}):
        meta_title_tag = soup.find("meta", {"property": "og:title"})
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

    new_novel = Novel(title, latest_chapter, req.url)

    return new_novel
