"""Unit tests for convert file format and update chapters."""
import logging
import unittest
from pathlib import Path, PurePath

import pandas as pd

import auto_update.edit as edit


class TestConvert(unittest.TestCase):
    """Unit tests for convert convert csv to dataframe and back."""

    current_directory = Path.cwd()
    folder = current_directory / "tests"
    BASE_NAME = r"test_novel.csv"
    BASE_NAME_COMPARE = r"test_novel_compare.csv"

    file = PurePath(folder, BASE_NAME)
    file_compare = PurePath(folder, BASE_NAME_COMPARE)

    df_compare = pd.read_csv(file_compare, sep=',', on_bad_lines='skip')

    def tearDown(self):
        path = Path('tests/test_novel_out.csv')
        path.unlink()

    def test_csv_to_dataframe(self):
        """Test if the csv is converted to dataframe properly."""
        df = edit.csv_to_dataframe(self.file)
        self.assertTrue(self.df_compare.equals(df))

    def test_auto_update(self):
        """Test if the out file is created each time."""
        path = Path('tests/test_novel_out.csv')
        edit.auto_update(self.file)
        self.assertTrue(path.exists())


class TestUpdate(unittest.TestCase):
    """Unit tests for update chapters."""

    ROW_0 = {'title': "アルマーク",
             'latest_chapter': 670,
             'link': "https://ncode.syosetu.com/novelview/infotop/ncode/n9407fu/",
             'parser': "syosetu"}
    ROW_1 = {'title': "最弱テイマーはゴミ拾いの旅を始めました。",
             'latest_chapter': 825,
             'link': "https://ncode.syosetu.com/novelview/infotop/ncode/n9629ex/",
             'parser': "syosetu"}

    MY_DF = pd.DataFrame([ROW_0, ROW_1])

    def test_update(self):
        """Test if the latest chapter is renewed correctly."""
        self.assertEqual(688, edit.update_chapter(self.MY_DF).loc[0, "latest_chapter"])
        self.assertEqual(903, edit.update_chapter(self.MY_DF).loc[1, "latest_chapter"])


class TestPassToParser(unittest.TestCase):
    """Unit tests for choosing parsers."""

    LINK_SYOSETU = "https://ncode.syosetu.com/novelview/infotop/ncode/n9407fu/"
    LINK_NOVEL_UPDATES = "https://www.novelupdates.com/series/forget-my-husband-ill-go-make-money/"
    PARSER_SYOSETU = "syosetu"
    PARSER_NOVEL_UPDATES = "novel_updates"

    def test_pass_to_parser(self):
        """Test if the latest chapter is renewed correctly."""
        self.assertEqual(688, edit.pass_to_parser(self.LINK_SYOSETU, self.PARSER_SYOSETU)['latest_chapter'])


class TestLog(unittest.TestCase):
    """Unit tests for logging."""

    logger = logging.getLogger("auto_update.edit")

    LINK_404 = "https://ncode.syosetu.com/novelview/infotop/ncode/aaaa/"
    LINK_NO_TITLE = "https://google.com"
    LINK_NO_CHAPTER = "https://www.novelupdates.com/series/forget-my-husband-ill-go-make-money/"  # with syosetu parser

    ROW_404 = {'title': "4_0_4",
               'latest_chapter': 670,
               'link': LINK_404,
               'parser': "syosetu"}
    ROW_NO_TITLE = {'title': "no_title",
                    'latest_chapter': 825,
                    'link': LINK_NO_TITLE,
                    'parser': "syosetu"}
    ROW_NO_CHAPTER = {'title': "no_chapter",
                      'latest_chapter': 825,
                      'link': LINK_NO_CHAPTER,
                      'parser': "syosetu"}
    df_404 = pd.DataFrame([ROW_404])
    df_no_title = pd.DataFrame([ROW_NO_TITLE])
    df_no_chapter = pd.DataFrame([ROW_NO_CHAPTER])

    def tearDown(self):
        logging.shutdown()
        with open('auto_update.edit.log', 'w'):
            pass


    def test_update_404(self):
        """Test if the 404 log is produced correctly."""
        with self.assertLogs(self.logger) as cm:
            edit.update_chapter(self.df_404).loc[0, "latest_chapter"]
        self.assertIn('404', cm.output[0])

    def test_update_no_title(self):
        """Test if the no title log is produced correctly."""
        with self.assertLogs(self.logger) as cm:
            edit.update_chapter(self.df_no_title).loc[0, "latest_chapter"]
        self.assertIn('No title found', cm.output[0])

    def test_update_no_chapter(self):
        """Test if the no chapter log is produced correctly."""
        with self.assertLogs(self.logger) as cm:
            edit.update_chapter(self.df_no_chapter).loc[0, "latest_chapter"]
        self.assertIn('No chapter number found', cm.output[0])


if __name__ == '__main__':
    unittest.main()
