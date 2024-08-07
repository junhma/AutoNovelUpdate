"""Unit tests for parsers."""

import unittest

import asyncio
from pyvirtualdisplay.display import Display
from auto_update.web_parser import syosetuAPI, novel_updates, book_walker, book_meter
from auto_update.exceptions import ChapterNotFoundException, NcodeNotFoundException

class TestExceptionsParser(unittest.IsolatedAsyncioTestCase):
    """Unit tests for exceptions."""
    LINK_NO_CHAPTER = "https://www.novelupdates.com/series/everyone-else-is-a-returnee/"
    LINK_NO_NCODE = "https://google.com"
    LINK_NO_PARSER = LINK_NO_NCODE

    async def test_no_chapter(self):
        """Tests if ChapterNotFoundException is raised when it is supposed to."""
        with self.assertRaises(ChapterNotFoundException):
            with Display(visible=False, size=(1080,720)):
                await novel_updates(self.LINK_NO_CHAPTER)
    
    async def test_no_ncode(self):
        """Tests if NcodeNotFoundException is raised when it is supposed to."""
        with self.assertRaises(NcodeNotFoundException):
            await syosetuAPI(self.LINK_NO_NCODE)

class TestWebParserSyosetuAPI(unittest.IsolatedAsyncioTestCase):
    """Unit tests for syosetu parser."""

    LINK_SYOSETU_1 = "https://ncode.syosetu.com/n3930eh/"
    LINK_SYOSETU_2 = "https://ncode.syosetu.com/n9981by/"
    LINK_SYOSETU_3 = "https://ncode.syosetu.com/n5011bc/"
    links = [LINK_SYOSETU_1, LINK_SYOSETU_2, LINK_SYOSETU_3]
    async def test_latest_chapter(self):
        """Tests if latest chapter matches."""
        tasks = [asyncio.create_task(syosetuAPI(link)) for link in self.links]
        results = await asyncio.gather(*tasks)
        self.assertEqual(702, results[0]["latest_chapter"])
        self.assertEqual(214, results[1]["latest_chapter"])
        self.assertEqual(186, results[2]["latest_chapter"])


class TestWebParserNovelUpdates(unittest.IsolatedAsyncioTestCase):
    """Unit tests for novel updates parser."""

    LINK_NOVEL_UPDATES_1 = "https://www.novelupdates.com/series/heaven-officials-blessing/"
    LINK_NOVEL_UPDATES_2 = "https://www.novelupdates.com/series/my-disciple-died-yet-again/"
    LINK_NOVEL_UPDATES_3 = "https://www.novelupdates.com/series/thousand-autumns/"
    links = [LINK_NOVEL_UPDATES_1, LINK_NOVEL_UPDATES_2, LINK_NOVEL_UPDATES_3]
    async def test_latest_chapter(self):
        """Tests if latest chapter matches."""
        with Display(visible=False, size=(1080,720)):
            tasks = [asyncio.create_task(novel_updates(link)) for link in self.links]
            results = await asyncio.gather(*tasks)
        self.assertEqual(40, results[0]["latest_chapter"])
        self.assertEqual(393, results[1]["latest_chapter"])
        self.assertEqual(87, results[2]["latest_chapter"])


class TestWebParserBookWalker(unittest.IsolatedAsyncioTestCase):
    """Unit tests for book walker parser."""

    LINK_BOOK_WALKER_1 = "https://bookwalker.jp/series/22301/"
    LINK_BOOK_WALKER_2 = "https://bookwalker.jp/series/12997/"
    LINK_BOOK_WALKER_3 = "https://bookwalker.jp/series/23628/"
    links = [LINK_BOOK_WALKER_1, LINK_BOOK_WALKER_2, LINK_BOOK_WALKER_3]
    async def test_latest_chapter(self):
        """Tests if latest chapter matches."""
        with Display(visible=False, size=(1080,720)):
            tasks = [asyncio.create_task(book_walker(link)) for link in self.links]
            results = await asyncio.gather(*tasks)
        self.assertEqual(14, results[0]["latest_chapter"])
        self.assertEqual(49, results[1]["latest_chapter"])
        self.assertEqual(40, results[2]["latest_chapter"])

class TestWebParserBookMeter(unittest.IsolatedAsyncioTestCase):
    """Unit tests for book meter parser."""

    LINK_BOOK_METER_1 = "https://bookmeter.com/series/2450"
    LINK_BOOK_METER_2 = "https://bookmeter.com/series/6242"
    links = [LINK_BOOK_METER_1, LINK_BOOK_METER_2]
    async def test_latest_chapter(self):
        """Tests if latest chapter matches."""
        with Display(visible=False, size=(1080,720)):
            tasks = [asyncio.create_task(book_meter(link)) for link in self.links]
            results = await asyncio.gather(*tasks)
        self.assertEqual(16, results[0]["latest_chapter"])
        self.assertEqual(14, results[1]["latest_chapter"])

if __name__ == '__main__':
    unittest.main()
