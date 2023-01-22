# in progress


from parsers.parse_novel_updates import parse_novel_updates
from parsers.parse_syosetsu import parse_syosetsu
from csv_to_object_list import csv_to_object_list
import cloudscraper
from bs4 import BeautifulSoup as bs
import pandas as pd


# link = dfcsv['Link'][0]
# link = "https://www.novelupdates.com/series/the-sword-and-the-dress/"
# scraper = cloudscraper.create_scraper()
# req = scraper.get(websites[0].link)
# output = parse_novel_updates(req)

""" 



SYOSETSU = "https://ncode.syosetu.com"
SYOSETSU_INFO = "https://ncode.syosetu.com/novelview/infotop/ncode"

https://ncode.syosetu.com/novelview/infotop/ncode/n9629ex/

def get_info_panel(nid):
    return f"{SYOSETSU_INFO}/n{nid}/"



https://ncode.syosetu.com/novelview/infotop/ncode/n9629ex/

link = 'https://ncode.syosetu.com/n9629ex/'
scraper = cloudscraper.create_scraper()
req = scraper.get(link)

soup = bs(req.text, "html.parser")

LatestChapters = ''
lach = soup.find(class_="novel_title")
LatestChapters = lach.get_text()

print(LatestChapters)

 """
