# ok

import unittest
import cloudscraper
from parsers.parse_syosetsu import parse_syosetsu
from novel import Novel

class TestCsvToObject(unittest.TestCase):

    # check if it's a Novel
    def test_is_novel(self):
        LINK = "https://ncode.syosetu.com/novelview/infotop/ncode/n9629ex/"
        scraper = cloudscraper.create_scraper()
        req = scraper.get(LINK)
        self.assertIsInstance(parse_syosetsu(req), Novel)

    # check if novel has the right title
    def test_title(self):
        LINK = "https://ncode.syosetu.com/novelview/infotop/ncode/n9407fu/"
        scraper = cloudscraper.create_scraper()
        req = scraper.get(LINK)
        self.assertEqual(parse_syosetsu(req).title, "【書籍化】アルマーク   ～北の剣、南の杖～")

    # check if novel has the right url
    def test_url(self):
        LINK = "https://ncode.syosetu.com/novelview/infotop/ncode/n9629ex/"
        scraper = cloudscraper.create_scraper()
        req = scraper.get(LINK)
        self.assertEqual(parse_syosetsu(
            req).link, "https://ncode.syosetu.com/novelview/infotop/ncode/n9629ex/")
if __name__ == '__main__':
    unittest.main()
