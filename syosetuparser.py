from bs4 import BeautifulSoup as bs
import pandas as pd


def parseSeries(req):
    soup = bs(req.text, "html.parser")

    Title = ''
    tit = soup.find(class_="novel_title")
    Title = tit.get_text()
    Title = soup.find("p", class_="novel_title")

    LatestChapters = []
    if tt.find("table", id="myTable") is not None:
        rel = tt.find("table", id="myTable").find("tbody").find("tr")
        release = rel.select("td")[2].find("a").get("title")
        LatestChapters = release
    else:
        LatestChapters = None

    result = pd.Series([Title, LatestChapters, "none"], index=[
                       "Title", "LatestChapters", "EnglishPublisher"])

    return result
