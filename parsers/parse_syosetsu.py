# ok

# parser syosetsu

from bs4 import BeautifulSoup as bs
import re
from novel import Novel

def parse_syosetsu(req):
    if req.status_code == 404:
        raise ValueError

    soup = bs(req.text, "html.parser")

    # find title
    title = soup.find("h1").get_text()

    # find latest chapter
    if soup.find(id="noveltype_notend"):
        string = soup.find(id="noveltype_notend").next_sibling
        latest_chapter = re.findall("\d+", string)[0]
    else:
        latest_chapter = 0

    new_novel = Novel(title, latest_chapter, req.url)

    return new_novel
