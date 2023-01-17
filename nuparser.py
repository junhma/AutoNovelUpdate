from bs4 import BeautifulSoup as bs
import pandas as pd


def parseSeries(req):
    soup = bs(req.text, "html.parser")
    page = soup.find("div", class_="w-blog-content")
    body = page.find("div", class_="g-cols wpb_row offset_default")
    ot = body.find("div", class_="one-third").find("div",
                                                   class_="wpb_text_column").find("div", class_="wpb_wrapper")
    tt = body.find("div", class_="two-thirds").find("div",
                                                    class_="wpb_text_column").find("div", class_="wpb_wrapper")

    Title = page.find("div", class_="seriestitlenu").text

    EnglishPublisher = []
    if ot.find("div", id="showepublisher").find("a") is not None:
        EnglishPublisher = {"name": ot.find("div", id="showepublisher").find(
            "a").text, "link": ot.find("div", id="showepublisher").find("a").get("href")}
    else:
        EnglishPublisher = None

    LatestChapters = []
    if tt.find("table", id="myTable") is not None:
        rel = tt.find("table", id="myTable").find("tbody").find("tr")
        release = rel.select("td")[2].find("a").get("title")
        LatestChapters = release
    else:
        LatestChapters = None

    result = pd.Series([Title, LatestChapters, EnglishPublisher], index=[
                       "Title", "LatestChapters", "EnglishPublisher"])

    return result
