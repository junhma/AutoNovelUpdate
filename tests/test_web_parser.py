"""Unit tests for parsers."""

import unittest

from requests import HTTPError,URLRequired

from auto_update.web_parser import syosetuAPI, novel_updates
from auto_update.exceptions import (ChapterNotFoundException,
                                    TitleNotFoundException)


class TestExceptions(unittest.TestCase):
    """Unit tests for exceptions shared between parsers."""

    LINK_HTTP_ERROR = "http://httpbin.org/status/404"
    LINK_NO_TITLE = "https://google.com"
    LINK_NO_CHAPTER = "https://www.novelupdates.com/series/everyone-else-is-a-returnee/"
    LINK_BAD_URL = LINK_NO_TITLE

    def test_http_error(self):
        """Tests if HTTPError is raised when it is supposed to."""
        with self.assertRaises(HTTPError) as context:
            novel_updates(self.LINK_HTTP_ERROR)['latest_chapter']
        self.assertEqual('404 Client Error: NOT FOUND for url: http://httpbin.org/status/404',
                         context.exception.args[0])

    def test_no_title(self):
        """Tests if TitleNotFoundException is raised when it is supposed to."""
        with self.assertRaises(TitleNotFoundException):
            novel_updates(self.LINK_NO_TITLE)['latest_chapter']

    def test_no_chapter(self):
        """Tests if ChapterNotFoundException is raised when it is supposed to."""
        with self.assertRaises(ChapterNotFoundException):
            novel_updates(self.LINK_NO_CHAPTER)['latest_chapter']
    
    def test_bad_url(self):
        """Tests if URLRequired is raised when it is supposed to."""
        with self.assertRaises(URLRequired):
            syosetuAPI(self.LINK_BAD_URL)['latest_chapter']

class TestWebParserSyosetuAPI(unittest.TestCase):
    """Unit tests for syosetu parser."""

    LINK_SYOSETU_1 = "https://ncode.syosetu.com/novelview/infotop/ncode/n3930eh/"
    LINK_SYOSETU_2 = "https://ncode.syosetu.com/novelview/infotop/ncode/n9981by/"

    def test_title(self):
        """Tests if title matches."""
        self.assertEqual("狼は眠らない",
                         syosetuAPI(self.LINK_SYOSETU_1)['title'])
        self.assertEqual("北の砦にて　新しい季節　～転生して、もふもふ子ギツネな雪の精霊になりました～",
                         syosetuAPI(self.LINK_SYOSETU_2)['title'])

    def test_latest_chapter(self):
        """Tests if latest chapter matches."""
        self.assertEqual(702, syosetuAPI(self.LINK_SYOSETU_1)['latest_chapter'])
        self.assertEqual(214, syosetuAPI(self.LINK_SYOSETU_2)['latest_chapter'])


class TestWebParserNovelUpdates(unittest.TestCase):
    """Unit tests for novel updates parser."""

    LINK_NOVEL_UPDATES = "https://www.novelupdates.com/series/the-founder-of-diabolism/"

    def test_title(self):
        """Tests if title matches."""
        self.assertEqual("The Founder of Diabolism",
                         novel_updates(self.LINK_NOVEL_UPDATES)['title'])

    def test_latest_chapter(self):
        """Tests if latest chapter matches."""
        self.assertEqual(46, novel_updates(
            self.LINK_NOVEL_UPDATES)["latest_chapter"])


if __name__ == '__main__':
    unittest.main()
