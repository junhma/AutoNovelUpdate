"""Unit tests for convert file format and update chapters."""

import unittest
from pathlib import Path, PurePath
import pandas as pd
import auto_update.edit as edit

class TestConvert(unittest.TestCase):
    """Unit tests for convert file format."""

    BASE_FOLDER = PurePath(Path.home(), "Documents/GitHub/autoupdate/tests")
    BASE_NAME = r"test_novel.csv"
    BASE_NAME_COMPARE = r"test_novel_compare.csv"
    
    file = PurePath(BASE_FOLDER, BASE_NAME)
    file_compare = PurePath(BASE_FOLDER, BASE_NAME_COMPARE)

    df_compare = pd.read_csv(file_compare, sep = ',', on_bad_lines='skip')

    def test_convert(self):
        """Unit tests for convert csv to dataframe and back."""
        edit.convert(self.file, self.BASE_FOLDER)
        df = pd.read_csv(self.file, sep = ',', on_bad_lines='skip')
        self.assertTrue(self.df_compare.equals(df))

class TestUpdate(unittest.TestCase):
    """Unit tests for update chapters."""

    ROW_1 = {'title': "アルマーク",
                'latest_chapter': 670,
                'link': "https://ncode.syosetu.com/novelview/infotop/ncode/n9407fu/",
                'parser': "syosetu"}
    ROW_2 = {'title': "最弱テイマーはゴミ拾いの旅を始めました。",
                'latest_chapter': 825,
                'link': "https://ncode.syosetu.com/novelview/infotop/ncode/n9629ex/",
                'parser': "syosetu"}
    
    MY_DF = pd.DataFrame([ROW_1, ROW_2])
    def test_update(self):
        """Test if the latest chapter is renewed correctly."""
        self.assertEqual(678, edit.update(self.MY_DF).loc[0, "latest_chapter"])

class TestChoose(unittest.TestCase):
    """Unit tests for choosing parsers."""

    LINK_SYOSETU = "https://ncode.syosetu.com/novelview/infotop/ncode/n9407fu/"
    LINK_NOVEL_UPDATES = "https://www.novelupdates.com/series/forget-my-husband-ill-go-make-money/"
    PARSER_SYOSETU = "syosetu"
    PARSER_NOVEL_UPDATES = "novel_updates"
    
    def test_choose(self):
        """Test if the latest chapter is renewed correctly."""
        self.assertEqual(678, edit.choose(self.LINK_SYOSETU, self.PARSER_SYOSETU)['latest_chapter'])

if __name__ == '__main__':
    unittest.main()