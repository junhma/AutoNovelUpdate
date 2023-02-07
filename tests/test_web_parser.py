"""Unit tests for parsers."""

import unittest
import autoupdate.web_parser as web_parser

class TestWebParser(unittest.TestCase):
    """Unit tests for parsers."""

    LINK = "https://ncode.syosetu.com/novelview/infotop/ncode/n9407fu/"

    def test_title(self):
        """Test if title matches"""
        self.assertEqual("【書籍化】アルマーク   ～北の剣、南の杖～", 
            web_parser.syosetsu(self.LINK)["title"])

    def test_url(self):
        """Test if url matches."""
        self.assertEqual(self.LINK, web_parser.syosetsu(
            self.LINK)["link"])

    def test_latest_chapter(self):
        """Test if latest chapter matches."""
        self.assertEqual(678, web_parser.syosetsu(
            self.LINK)["latest_chapter"])

if __name__ == '__main__':
    unittest.main()
