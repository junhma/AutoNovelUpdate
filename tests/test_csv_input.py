import auto_update.csv_input as csv_input
import pandas as pd
import unittest
from pathlib import Path, PurePath

class TestConvert(unittest.TestCase):
    """Unit tests for convert convert csv to dataframe and back."""

    current_directory = Path.cwd()
    folder = current_directory / "tests"
    BASE_NAME = r"test_novel.csv"
    file = PurePath(folder, BASE_NAME)

    ROW_0 = {'title': "狼は眠らない",
             'latest_chapter': 700,
             'link': "https://ncode.syosetu.com/novelview/infotop/ncode/n3930eh/"}
    ROW_1 = {'title': "北の砦にて　新しい季節　～転生して、もふもふ子ギツネな雪の精霊になりました～",
             'latest_chapter': 200,
             'link': "https://ncode.syosetu.com/novelview/infotop/ncode/n9981by/"}
    ROW_2 = {'title': "The Founder of Diabolism",
             'latest_chapter': 40,
             'link': "https://www.novelupdates.com/series/the-founder-of-diabolism/"}

    DF_COMPARE = pd.DataFrame([ROW_0, ROW_1, ROW_2])

    def tearDown(self):
        path = Path('tests/test_novel_out.csv')
        try:
            path.unlink()
        except FileNotFoundError:
            pass

    def test_csv_to_dataframe(self):
        """Tests if the csv is converted to dataframe properly."""
        df = csv_input.csv_to_dataframe(self.file)
        self.assertTrue(self.DF_COMPARE.equals(df))

    def test_auto_update(self):
        """Tests if the out file is created each time."""
        csv_input.auto_update_csv(self.file)
        path = Path('tests/test_novel_out.csv')
        self.assertTrue(path.exists())