"""Unit tests for parsers."""

import unittest

from requests import HTTPError

from auto_update.update import pass_to_parser
from auto_update.web_parser import syosetuAPI, novel_updates
from auto_update.exceptions import ChapterNotFoundException, NcodeNotFoundException, MissingParserException


class TestExceptions(unittest.TestCase):
    """Unit tests for exceptions shared between parsers."""

    LINK_HTTP_ERROR = "http://httpbin.org/status/404"
    LINK_NO_CHAPTER = "https://www.novelupdates.com/series/everyone-else-is-a-returnee/"
    LINK_NO_NCODE = "https://google.com"
    LINK_NO_PARSER = LINK_NO_NCODE

    def test_http_error(self):
        """Tests if HTTPError is raised when it is supposed to."""
        with self.assertRaises(HTTPError) as context:
            novel_updates(self.LINK_HTTP_ERROR)['latest_chapter']
        self.assertEqual('404 Client Error: NOT FOUND for url: http://httpbin.org/status/404',
                         context.exception.args[0])

    def test_no_chapter(self):
        """Tests if ChapterNotFoundException is raised when it is supposed to."""
        with self.assertRaises(ChapterNotFoundException):
            novel_updates(self.LINK_NO_CHAPTER)['latest_chapter']
    
    def test_no_ncode(self):
        """Tests if NcodeNotFoundException is raised when it is supposed to."""
        with self.assertRaises(NcodeNotFoundException):
            syosetuAPI(self.LINK_NO_NCODE)['latest_chapter']
    
    def test_no_parser(self):
        """Tests if NcodeNotFoundException is raised when it is supposed to."""
        with self.assertRaises(MissingParserException):
            pass_to_parser(self.LINK_NO_PARSER)['latest_chapter']

class TestWebParserSyosetuAPI(unittest.TestCase):
    """Unit tests for syosetu parser."""

    LINK_SYOSETU_1 = "https://ncode.syosetu.com/n3930eh/"
    LINK_SYOSETU_2 = "https://ncode.syosetu.com//n9981by/"

    def test_latest_chapter(self):
        """Tests if latest chapter matches."""
        self.assertEqual(702, syosetuAPI(self.LINK_SYOSETU_1)['latest_chapter'])
        self.assertEqual(214, syosetuAPI(self.LINK_SYOSETU_2)['latest_chapter'])


class TestWebParserNovelUpdates(unittest.TestCase):
    """Unit tests for novel updates parser."""

    LINK_NOVEL_UPDATES = "https://www.novelupdates.com/series/heaven-officials-blessing/"

    def test_latest_chapter(self):
        """Tests if latest chapter matches."""
        self.assertEqual(40, novel_updates(
            self.LINK_NOVEL_UPDATES)["latest_chapter"])


if __name__ == '__main__':
    unittest.main()
