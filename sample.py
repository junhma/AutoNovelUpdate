from bs4 import BeautifulSoup as bs
import re
import cloudscraper
from parsers.parse_syosetsu import parse_syosetsu
from csv_to_object_list import csv_to_object_list
from novel import Novel



WEBSITE = "https://ncode.syosetu.com/novelview/infotop/ncode/n9629ex/"
scraper = cloudscraper.create_scraper()
req = scraper.get(WEBSITE)
title = parse_syosetsu(req).title

print(title)
