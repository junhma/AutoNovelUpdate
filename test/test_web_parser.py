"""Unit tests for parsers"""

import unittest
import cloudscraper
# from . import web_parser
# import doesnt work

class TestWebParser(unittest.TestCase):
    """Unit tests for parsers"""

    LINK = "https://ncode.syosetu.com/novelview/infotop/ncode/n9407fu/"

    def test_title(self):
        """Test if title matches"""
        scraper = cloudscraper.create_scraper()
        req = scraper.get(self.LINK)
        self.assertEqual(web_parser.syosetsu(
            req)["title"], "【書籍化】アルマーク   ～北の剣、南の杖～")

    def test_url(self):
        """Test if url matches"""
        scraper = cloudscraper.create_scraper()
        req = scraper.get(self.LINK)
        self.assertEqual(web_parser.syosetsu(
            req)["link"], "https://ncode.syosetu.com/novelview/infotop/ncode/n9629ex/")

    def test_latest_chapter(self):
        """Test if latest chapter matches"""
        scraper = cloudscraper.create_scraper()
        req = scraper.get(self.LINK)
        self.assertEqual(web_parser.syosetsu(
            req)["latest_chapter"], "https://ncode.syosetu.com/novelview/infotop/ncode/n9629ex/")


if __name__ == '__main__':
    unittest.main()
