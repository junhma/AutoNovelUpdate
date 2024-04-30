"""Unit tests for convert file format and update chapters."""
from auto_update.exceptions import MissingParserException
import auto_update.update as update
import pandas as pd
import logging
import unittest


class TestUpdate(unittest.TestCase):
    """Unit tests for update chapters."""

    ROW_0 = {'title': "狼は眠らない",
             'latest_chapter': 700,
             'link': "https://ncode.syosetu.com/novelview/infotop/ncode/n3930eh/"}
    ROW_1 = {'title': "北の砦にて　新しい季節　～転生して、もふもふ子ギツネな雪の精霊になりました～",
             'latest_chapter': 200,
             'link': "https://ncode.syosetu.com/novelview/infotop/ncode/n9981by/"}
    ROW_2 = {'title': "Heaven Official’s Blessing",
             'latest_chapter': 40,
             'link': "https://www.novelupdates.com/series/heaven-officials-blessing/"}

    MY_DF = pd.DataFrame([ROW_0, ROW_1, ROW_2])

    def test_update(self):
        """Tests if the latest chapter is renewed correctly."""
        self.assertEqual(702, update.update_chapter(self.MY_DF).loc[0, "latest_chapter"])
        self.assertEqual(214, update.update_chapter(self.MY_DF).loc[1, "latest_chapter"])
        self.assertEqual(40, update.update_chapter(self.MY_DF).loc[2, "latest_chapter"])

class TestPassToParser(unittest.TestCase):
    """Unit tests for choosing parsers."""

    LINK_SYOSETU_1 = "https://ncode.syosetu.com/novelview/infotop/ncode/n3930eh/"
    LINK_SYOSETU_2 = "https://ncode.syosetu.com/novelview/infotop/ncode/n9981by/"
    LINK_NOVEL_UPDATES = "https://www.novelupdates.com/series/heaven-officials-blessing/"
    LINK_NO_PARSER = "https://google.com"

    def test_pass_to_parser(self):
        """Tests if the latest chapter is renewed correctly."""
        self.assertEqual(702, update.pass_to_parser(self.LINK_SYOSETU_1)['latest_chapter'])
        self.assertEqual(214, update.pass_to_parser(self.LINK_SYOSETU_2)['latest_chapter'])
        self.assertEqual(40, update.pass_to_parser(self.LINK_NOVEL_UPDATES)['latest_chapter'])

    def test_no_parser_exception(self):
        """Tests if MissingParserException is raised when it is supposed to."""
        with self.assertRaises(MissingParserException) as context:
            update.pass_to_parser(self.LINK_NO_PARSER)
        self.assertEqual('Missing parser', context.exception.msg)


class TestLog(unittest.TestCase):
    """Unit tests for logging."""

    logger = logging.getLogger("auto_update.update")

    LINK_NO_PARSER = "https://google.com"
    LINK_HTTP_ERROR = "https://ncode.syosetu.com/novelview/infotop/ncode/aaaaaaa/"
    LINK_NO_CHAPTER = "https://www.novelupdates.com/series/everyone-else-is-a-returnee/"

    ROW_NO_PARSER = {'title': "no_parser",
                     'latest_chapter': 222,
                     'link': LINK_NO_PARSER}  # shouldn't matter
    ROW_NCODE_NOT_FOUND = {'title': "http_error",
                      'latest_chapter': 555,
                      'link': LINK_HTTP_ERROR}
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

    def test_no_parser(self):
        """Tests if the missing parser log is produced correctly."""
        with self.assertLogs(self.logger) as cm:
            update.update_chapter(self.df_no_parser).loc[0, "latest_chapter"]
        self.assertIn('Missing parser', cm.output[0])
        self.assertIn(self.ROW_NO_PARSER['title'], cm.output[0])

    def test_ncode_not_found(self):
        """Tests if the ncode not found log is produced correctly."""
        with self.assertLogs(self.logger) as cm:
            update.update_chapter(self.df_ncode_not_found).loc[0, "latest_chapter"]
        self.assertIn('Ncode not found', cm.output[0])
        self.assertIn(self.ROW_NCODE_NOT_FOUND['title'], cm.output[0])

    def test_no_chapter(self):
        """Tests if the no chapter log is produced correctly."""
        with self.assertLogs(self.logger) as cm:
            update.update_chapter(self.df_no_chapter).loc[0, "latest_chapter"]
        self.assertIn('No chapter number found', cm.output[0])
        self.assertIn(self.ROW_NO_CHAPTER['title'], cm.output[0])


if __name__ == '__main__':
    unittest.main()
