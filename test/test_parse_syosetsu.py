# ok

import unittest
import cloudscraper
from parsers.parse_syosetsu import parse_syosetsu
from novel import Novel

class TestCsvToObject(unittest.TestCase):

    # check if it's a Novel
    def test_is_novel(self):
        WEBSITE = "https://ncode.syosetu.com/novelview/infotop/ncode/n9629ex/"
        scraper = cloudscraper.create_scraper()
        req = scraper.get(WEBSITE)
        self.assertIsInstance(parse_syosetsu(req), Novel)

    # check if novel has the right title
    def test_title(self):
        WEBSITE = "https://ncode.syosetu.com/novelview/infotop/ncode/n9629ex/"
        scraper = cloudscraper.create_scraper()
        req = scraper.get(WEBSITE)
        self.assertEqual(parse_syosetsu(req).title, "最弱テイマーはゴミ拾いの旅を始めました。")

    # check if novel has the right url
    def test_url(self):
        WEBSITE = "https://ncode.syosetu.com/novelview/infotop/ncode/n9629ex/"
        scraper = cloudscraper.create_scraper()
        req = scraper.get(WEBSITE)
        self.assertEqual(parse_syosetsu(
            req).link, "https://ncode.syosetu.com/novelview/infotop/ncode/n9629ex/")
if __name__ == '__main__':
    unittest.main()
