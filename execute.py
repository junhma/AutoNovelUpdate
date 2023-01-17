from nuparser import parseSeries
import cloudscraper
import pandas as pd

dfcsv = pd.read_csv('autoupdate/test.csv')  # csv to dataframe
link = dfcsv['Link'][0]
# link = "https://www.novelupdates.com/series/the-sword-and-the-dress/"
scraper = cloudscraper.create_scraper()
req = scraper.get(link)
output = parseSeries(req)
print(output)
