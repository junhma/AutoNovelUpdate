"""Unit tests for convert file format and update chapters."""

import unittest
from pathlib import Path
import pandas as pd
import autoupdate.edit as edit

# class TestConvert(unittest.TestCase):
#     """Unit tests for convert file format."""

#     BASE_FOLDER = Path(__file__).parent.resolve()
#     BASE_NAME = r"test_novel.csv"
#     BASE_NAME_NEW = r"test_novel_new.csv"
    
#     file = Path(BASE_FOLDER, BASE_NAME)
#     new_file = Path(BASE_FOLDER, BASE_NAME_NEW)

#     my_df_new = pd.read_csv(new_file)

#     def test_convert(self):
#         """Unit tests for convert file format."""
#         edit.convert(self.file, self.BASE_FOLDER)
#         my_df_out = pd.read_csv(self.file)
#         self.assertTrue(self.my_df_new.equals(my_df_out))

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