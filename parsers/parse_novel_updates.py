# novel update ok (no test)

from bs4 import BeautifulSoup as bs
from novel import Novel

# parser novel updates
def parse_novel_updates(req):
    if req.status_code == 404:
        raise ValueError
    soup = bs(req.text, "html.parser")

    # split page in parts
    page = soup.find("div", class_="w-blog-content")
    body = page.find("div", class_="g-cols wpb_row offset_default")
    ot = body.find("div", class_="one-third").find("div",
                                                   class_="wpb_text_column").find("div", class_="wpb_wrapper")
    tt = body.find("div", class_="two-thirds").find("div",
                                                    class_="wpb_text_column").find("div", class_="wpb_wrapper")

    # find title
    title = page.find("div", class_="seriestitlenu").text

    # # find English publisher
    # english_publisher = []
    # if ot.find("div", id="showepublisher").find("a") is not None:
    #     english_publisher = {"name": ot.find("div", id="showepublisher").find(
    #         "a").text, "link": ot.find("div", id="showepublisher").find("a").get("href")}
    # else:
    #     english_publisher = None

    # find latest chapter
    latest_chapter = []
    if tt.find("table", id="myTable") is not None:
        rel = tt.find("table", id="myTable").find("tbody").find("tr")
        release = rel.select("td")[2].find("a").get("title")
        latest_chapter = release
    else:
        latest_chapter = None

    new_novel = Novel(title, latest_chapter, req.url)

    return new_novel

