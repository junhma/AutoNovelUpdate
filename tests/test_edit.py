"""Unit tests for convert file format and update chapters."""
from auto_update.exceptions import MissingParserException
import auto_update.edit as edit
import pandas as pd
import logging
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
             'link': "https://ncode.syosetu.com/novelview/infotop/ncode/n3930eh/",
             'parser': "syosetu"}
    ROW_1 = {'title': "北の砦にて　新しい季節　～転生して、もふもふ子ギツネな雪の精霊になりました～",
             'latest_chapter': 200,
             'link': "https://ncode.syosetu.com/novelview/infotop/ncode/n9981by/",
             'parser': "syosetu"}
    ROW_2 = {'title': "The Founder of Diabolism",
             'latest_chapter': 40,
             'link': "https://www.novelupdates.com/series/the-founder-of-diabolism/",
             'parser': "novel_updates"}

    DF_COMPARE = pd.DataFrame([ROW_0, ROW_1, ROW_2])

    def tearDown(self):
        path = Path('tests/test_novel_out.csv')
        try:
            path.unlink()
        except FileNotFoundError:
            pass

    def test_csv_to_dataframe(self):
        """Tests if the csv is converted to dataframe properly."""
        df = edit.csv_to_dataframe(self.file)
        self.assertTrue(self.DF_COMPARE.equals(df))

    def test_auto_update(self):
        """Tests if the out file is created each time."""
        edit.auto_update(self.file)
        path = Path('tests/test_novel_out.csv')
        self.assertTrue(path.exists())


class TestUpdate(unittest.TestCase):
    """Unit tests for update chapters."""

    ROW_0 = {'title': "狼は眠らない",
             'latest_chapter': 700,
             'link': "https://ncode.syosetu.com/novelview/infotop/ncode/n3930eh/",
             'parser': "syosetu"}
    ROW_1 = {'title': "北の砦にて　新しい季節　～転生して、もふもふ子ギツネな雪の精霊になりました～",
             'latest_chapter': 200,
             'link': "https://ncode.syosetu.com/novelview/infotop/ncode/n9981by/",
             'parser': "syosetu"}
    ROW_2 = {'title': "The Founder of Diabolism",
             'latest_chapter': 40,
             'link': "https://www.novelupdates.com/series/the-founder-of-diabolism/",
             'parser': "novel_updates"}

    MY_DF = pd.DataFrame([ROW_0, ROW_1, ROW_2])

    def test_update(self):
        """Tests if the latest chapter is renewed correctly."""
        self.assertEqual(702, edit.update_chapter(self.MY_DF).loc[0, "latest_chapter"])
        self.assertEqual(214, edit.update_chapter(self.MY_DF).loc[1, "latest_chapter"])
        self.assertEqual(46, edit.update_chapter(self.MY_DF).loc[2, "latest_chapter"])


class TestPassToParser(unittest.TestCase):
    """Unit tests for choosing parsers."""

    LINK_SYOSETU_1 = "https://ncode.syosetu.com/novelview/infotop/ncode/n3930eh/"
    LINK_SYOSETU_2 = "https://ncode.syosetu.com/novelview/infotop/ncode/n9981by/"
    PARSER_SYOSETU = "syosetu"
    LINK_NOVEL_UPDATES = "https://www.novelupdates.com/series/the-founder-of-diabolism/"
    PARSER_NOVEL_UPDATES = "novel_updates"

    def test_pass_to_parser(self):
        """Tests if the latest chapter is renewed correctly."""
        self.assertEqual(702, edit.pass_to_parser(self.LINK_SYOSETU_1, self.PARSER_SYOSETU)['latest_chapter'])
        self.assertEqual(214, edit.pass_to_parser(self.LINK_SYOSETU_2, self.PARSER_SYOSETU)['latest_chapter'])
        self.assertEqual(46, edit.pass_to_parser(self.LINK_NOVEL_UPDATES, self.PARSER_NOVEL_UPDATES)['latest_chapter'])

    def test_no_parser_exception(self):
        """Tests if MissingParserException is raised when it is supposed to."""
        with self.assertRaises(MissingParserException) as context:
            edit.pass_to_parser(self.LINK_SYOSETU_1, "")["latest_chapter"]
        self.assertEqual('Missing parser', context.exception.msg)


class TestLog(unittest.TestCase):
    """Unit tests for logging."""

    logger = logging.getLogger("auto_update.edit")

    LINK_HTTP_ERROR = "https://ncode.syosetu.com/novelview/infotop/ncode/aaaaaaa/"
    LINK_NO_TITLE = "https://google.com"
    LINK_NO_CHAPTER = "https://www.novelupdates.com/series/everyone-else-is-a-returnee/"

    ROW_NO_PARSER = {'title': "no_parser",
                     'latest_chapter': 222,
                     'link': LINK_NO_TITLE,  # shouldn't matter
                     'parser': ""}
    ROW_HTTP_ERROR = {'title': "http_error",
                      'latest_chapter': 555,
                      'link': LINK_HTTP_ERROR,
                      'parser': "novel_updates"}
    ROW_NO_TITLE = {'title': "no_title",
                    'latest_chapter': 444,
                    'link': LINK_NO_TITLE,
                    'parser': "novel_updates"}
    ROW_NO_CHAPTER = {'title': "no_chapter",
                      'latest_chapter': 333,
                      'link': LINK_NO_CHAPTER,
                      'parser': "novel_updates"}
    df_no_parser = pd.DataFrame([ROW_NO_PARSER])
    df_http_error = pd.DataFrame([ROW_HTTP_ERROR])
    df_no_title = pd.DataFrame([ROW_NO_TITLE])
    df_no_chapter = pd.DataFrame([ROW_NO_CHAPTER])

    def tearDown(self):
        logging.shutdown()
        with open('auto_update.edit.log', 'w'):
            pass

    def test_no_parser(self):
        """Tests if the missing parser log is produced correctly."""
        with self.assertLogs(self.logger) as cm:
            edit.update_chapter(self.df_no_parser).loc[0, "latest_chapter"]
        self.assertIn('Missing parser', cm.output[0])
        self.assertIn(self.ROW_NO_PARSER['title'], cm.output[0])

    def test_http_error(self):
        """Tests if the HTTP ERROR log is produced correctly."""
        with self.assertLogs(self.logger) as cm:
            edit.update_chapter(self.df_http_error).loc[0, "latest_chapter"]
        self.assertIn('404 Client Error', cm.output[0])
        self.assertIn(self.ROW_HTTP_ERROR['title'], cm.output[0])

    def test_no_title(self):
        """Tests if the no title log is produced correctly."""
        with self.assertLogs(self.logger) as cm:
            edit.update_chapter(self.df_no_title).loc[0, "latest_chapter"]
        self.assertIn('No title found', cm.output[0])
        self.assertIn(self.ROW_NO_TITLE['title'], cm.output[0])

    def test_no_chapter(self):
        """Tests if the no chapter log is produced correctly."""
        with self.assertLogs(self.logger) as cm:
            edit.update_chapter(self.df_no_chapter).loc[0, "latest_chapter"]
        self.assertIn('No chapter number found', cm.output[0])
        self.assertIn(self.ROW_NO_CHAPTER['title'], cm.output[0])


if __name__ == '__main__':
    unittest.main()
