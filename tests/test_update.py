"""Unit tests for convert file format and update chapters."""

import unittest

import asyncio
from pyvirtualdisplay.display import Display
import nodriver as uc
import pandas as pd
import logging
from auto_update.exceptions import MissingParserException
from auto_update.update import update_chapter, pass_to_parser, process_row

class TestExceptionsUpdate(unittest.IsolatedAsyncioTestCase):
    """Unit tests for exceptions."""

    LINK_NO_PARSER = "https://google.com"
    
    async def test_no_parser(self):
        """Tests if MissingParserException is raised when it is supposed to."""
        with self.assertRaises(MissingParserException):
            with Display(visible=False, size=(1080,720)):
                browser = await uc.start(sandbox = False)
                result = await pass_to_parser(browser, self.LINK_NO_PARSER)
                result["latest_chapter"]

class TestUpdate(unittest.IsolatedAsyncioTestCase):
    """Unit tests for update chapters."""

    ROW_0 = {'title': "狼は眠らない",
             'latest_chapter': 700,
             'link': "https://ncode.syosetu.com/novelview/infotop/ncode/n3930eh/"}
    ROW_1 = {'title': "狼と香辛料",
             'latest_chapter': 200,
             'link': "https://bookmeter.com/series/2450"}
    ROW_2 = {'title': "Heaven Official’s Blessing",
             'latest_chapter': 40,
             'link': "https://www.novelupdates.com/series/heaven-officials-blessing/"}
    DF = pd.DataFrame([ROW_0, ROW_1, ROW_2])
    DF_ROW_0 = pd.DataFrame([ROW_0])
    DF_ROW_1 = pd.DataFrame([ROW_1])
    DF_ROW_2 = pd.DataFrame([ROW_2])
    df_row_list = [DF_ROW_0, DF_ROW_1, DF_ROW_2]
    async def test_process_row(self):
        """Tests if the latest chapter is renewed correctly for a row."""
        with Display(visible=False, size=(1080,720)):
            browser = await uc.start(sandbox = False)
            tasks = [asyncio.create_task(process_row(browser, df_row, 0)) for df_row in self.df_row_list]
            results = await asyncio.gather(*tasks)
        self.assertEqual(702, results[0]["latest_chapter"])
        self.assertEqual(16, results[1]["latest_chapter"])
        self.assertEqual(40, results[2]["latest_chapter"])

    async def test_update(self):
        """Tests if the latest chapter is renewed correctly."""
        with Display(visible=False, size=(1080,720)):
            browser = await uc.start(sandbox = False)
            result = await update_chapter(browser, self.DF)
        self.assertEqual(702, result.loc[0, "latest_chapter"])
        self.assertEqual(16, result.loc[1, "latest_chapter"])
        self.assertEqual(40, result.loc[2, "latest_chapter"])

class TestPassToParser(unittest.IsolatedAsyncioTestCase):
    """Unit tests for choosing parsers."""

    LINK_SYOSETU_1 = "https://ncode.syosetu.com/novelview/infotop/ncode/n3930eh/"
    LINK_SYOSETU_2 = "https://ncode.syosetu.com/novelview/infotop/ncode/n9981by/"
    LINK_NOVEL_UPDATES_1 = "https://www.novelupdates.com/series/heaven-officials-blessing/"
    LINK_NOVEL_UPDATES_2 = "https://www.novelupdates.com/series/my-disciple-died-yet-again/"
    LINK_BOOK_WALKER_1 = "https://bookwalker.jp/series/22301/"
    LINK_BOOK_WALKER_2 = "https://bookwalker.jp/series/12997/"
    LINK_BOOK_METER_1 = "https://bookmeter.com/series/2450"
    LINK_BOOK_METER_2 = "https://bookmeter.com/series/6242"
    LINK_NO_PARSER = "https://google.com"
    links = [LINK_SYOSETU_1, LINK_SYOSETU_2, LINK_NOVEL_UPDATES_1, LINK_NOVEL_UPDATES_2, LINK_BOOK_WALKER_1, LINK_BOOK_WALKER_2, LINK_BOOK_METER_1, LINK_BOOK_METER_2]
    async def test_pass_to_parser(self):
        """Tests if the latest chapter is renewed correctly."""
        with Display(visible=False, size=(1080,720)):
            browser = await uc.start(sandbox = False)
            tasks = [asyncio.create_task(pass_to_parser(browser, link)) for link in self.links]
            results = await asyncio.gather(*tasks)
        self.assertEqual(702, results[0]['latest_chapter'])
        self.assertEqual(214, results[1]['latest_chapter'])
        self.assertEqual(40, results[2]['latest_chapter'])
        self.assertEqual(393, results[3]['latest_chapter'])
        self.assertEqual(14, results[4]['latest_chapter'])
        self.assertEqual(49, results[5]['latest_chapter'])
        self.assertEqual(16, results[6]['latest_chapter'])
        self.assertEqual(14, results[7]['latest_chapter'])


    async def test_no_parser_exception(self):
        """Tests if MissingParserException is raised when it is supposed to."""
        with self.assertRaises(MissingParserException) as context:
            with Display(visible=False, size=(1080,720)):
                browser = await uc.start(sandbox = False)
                task_no_parser = asyncio.create_task(pass_to_parser(browser, self.LINK_NO_PARSER))
                await task_no_parser
        self.assertEqual('Missing parser', context.exception.msg)


class TestLog(unittest.IsolatedAsyncioTestCase):
    """Unit tests for logging."""

    logger = logging.getLogger("auto_update.update")

    LINK_NO_PARSER = "https://google.com"
    LINK_NCODE_NOT_FOUND = "https://ncode.syosetu.com/novelview/infotop/ncode/aaaaaaa/"
    LINK_NO_CHAPTER = "https://www.novelupdates.com/series/everyone-else-is-a-returnee/"

    ROW_NO_PARSER = {'title': "no_parser",
                     'latest_chapter': 222,
                     'link': LINK_NO_PARSER}  # shouldn't matter
    ROW_NCODE_NOT_FOUND = {'title': "http_error",
                      'latest_chapter': 555,
                      'link': LINK_NCODE_NOT_FOUND}
    ROW_NO_CHAPTER = {'title': "no_chapter",
                      'latest_chapter': 333,
                      'link': LINK_NO_CHAPTER}
    df_no_parser = pd.DataFrame([ROW_NO_PARSER])
    df_ncode_not_found = pd.DataFrame([ROW_NCODE_NOT_FOUND])
    df_no_chapter = pd.DataFrame([ROW_NO_CHAPTER])

    def tearDown(self):
        logging.shutdown()
        with open('auto_update.update.log', 'w'):
            pass

    async def test_no_parser(self):
        """Tests if the missing parser log is produced correctly."""
        with Display(visible=False, size=(1080,720)):
            with self.assertLogs(self.logger) as cm:
                browser = await uc.start(sandbox = False)
                result = await update_chapter(browser, self.df_no_parser)
                result.loc[0, "latest_chapter"]
        self.assertIn('Missing parser', cm.output[0])
        self.assertIn(self.ROW_NO_PARSER['title'], cm.output[0])

    async def test_ncode_not_found(self):
        """Tests if the ncode not found log is produced correctly."""
        with Display(visible=False, size=(1080,720)):
            with self.assertLogs(self.logger) as cm:
                browser = await uc.start(sandbox = False)
                result = await update_chapter(browser, self.df_ncode_not_found)
                result.loc[0, "latest_chapter"]
        self.assertIn('Ncode not found', cm.output[0])
        self.assertIn(self.ROW_NCODE_NOT_FOUND['title'], cm.output[0])

    async def test_no_chapter(self):
        """Tests if the no chapter log is produced correctly."""
        with Display(visible=False, size=(1080,720)):
            with self.assertLogs(self.logger) as cm:
                browser = await uc.start(sandbox = False)
                result = await update_chapter(browser, self.df_no_chapter)
                result.loc[0, "latest_chapter"]
        self.assertIn('No chapter number found', cm.output[0])
        self.assertIn(self.ROW_NO_CHAPTER['title'], cm.output[0])


if __name__ == '__main__':
    unittest.main()
