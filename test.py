from bs4 import BeautifulSoup as bs
import pandas as pd
import cloudscraper


link = 'https://ncode.syosetu.com/n9629ex/'
scraper = cloudscraper.create_scraper()
req = scraper.get(link)

soup = bs(req.text, "html.parser")

LatestChapters = ''
lach = soup.find(class_="novel_title")
LatestChapters = tilacht.get_text()

print(LatestChapters)
