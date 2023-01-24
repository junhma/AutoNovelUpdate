# ok

from parsers.parse_syosetsu import parse_syosetsu
import cloudscraper

# REQUIRE: list of Novel objects
# RETURN: list of Novel objects
def update_chapter(novels):

    for i in range(len(novels)):
        link = novels[i].link

        # Create CloudScraper Instance
        scraper = cloudscraper.create_scraper()

        # Make Request
        req = scraper.get(link)
        new_novel = parse_syosetsu(req)
        if new_novel.latest_chapter != novels[i].latest_chapter:
            novels[i].latest_chapter = new_novel.latest_chapter
    
    return novels

