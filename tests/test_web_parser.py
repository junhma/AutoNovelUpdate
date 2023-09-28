"""Unit tests for parsers."""

import unittest
import auto_update.web_parser as web_parser
from auto_update.exceptions import Exception404, TitleNotFoundException, ChapterNotFoundException

class TestExceptions(unittest.TestCase):
    """Unit tests for exceptions shared between parsers."""

    LINK_404 = "https://ncode.syosetu.com/novelview/infotop/ncode/aaaa/"
    LINK_NO_TITLE = "https://google.com"
    LINK_NO_CHAPTER = "https://www.novelupdates.com/series/forget-my-husband-ill-go-make-money/"


    def test_404(self):
        """Test if Exception404 works."""
        with self.assertRaises(Exception404) as context:
            web_parser.syosetu(self.LINK_404)['latest_chapter']
        self.assertEqual('404', context.exception.args[0])

    def test_no_title(self):
        """Test if TitleNotFoundException works."""
        with self.assertRaises(TitleNotFoundException) as context:
            web_parser.syosetu(self.LINK_NO_TITLE)['latest_chapter']
        self.assertEqual('No title found.', context.exception.args[0])

    def test_no_chapter(self):
        """Test if ChapterNotFoundException works."""
        with self.assertRaises(ChapterNotFoundException) as context:
            web_parser.syosetu(self.LINK_NO_CHAPTER)['latest_chapter']
        self.assertEqual('No chapter number found.', context.exception.args[0])

class TestWebParserSyosetu(unittest.TestCase):
    """Unit tests for syosetu parser."""

    LINK = "https://ncode.syosetu.com/novelview/infotop/ncode/n9407fu/"

    def test_title(self):
        """Test if title matches."""
        self.assertEqual("【書籍化】アルマーク   ～北の剣、南の杖～", 
            web_parser.syosetu(self.LINK)['title'])

    def test_url(self):
        """Test if url matches."""
        self.assertEqual(self.LINK, web_parser.syosetu(self.LINK)['link'])

    def test_latest_chapter(self):
        """Test if latest chapter matches."""
        self.assertEqual(688, web_parser.syosetu(self.LINK)['latest_chapter'])

class TestWebParserNovelUpdates(unittest.TestCase):
    """Unit tests for novel updates parser."""

    LINK = "https://www.novelupdates.com/series/forget-my-husband-ill-go-make-money/"
        
    def test_title(self):
        """Test if title matches."""
        self.assertEqual("Forget My Husband, I’ll Go Make Money", 
            web_parser.novel_updates(self.LINK)['title'])
        
    def test_url(self):
        """Test if url matches."""
        self.assertEqual(self.LINK, web_parser.novel_updates(
            self.LINK)['link'])
        
    def test_latest_chapter(self):
        """Test if latest chapter matches."""
        self.assertEqual(281, web_parser.novel_updates(
            self.LINK)["latest_chapter"])
    
    def test_english_publisher(self):
        """Test if latest chapter matches."""
        self.assertEqual("None", web_parser.novel_updates(
            self.LINK)['english_publisher'])

if __name__ == '__main__':
    unittest.main()
