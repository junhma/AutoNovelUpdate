#ok

import unittest
from update_chapter import update_chapter
from csv_to_object_list import csv_to_object_list


class TestUpdateChapter(unittest.TestCase):

    # check if it returns a list
    def test_is_list(self):
        TEST_CSV = 'autoupdate/test/test_novel.csv'
        NOVELS = csv_to_object_list(TEST_CSV)
        NEW_LIST = update_chapter(NOVELS)
        self.assertIsInstance(NEW_LIST, list)
        
    # check if the first entry of the list has the right latest chapter
    def test_latest_chapter(self):
        TEST_CSV = 'autoupdate/test/test_novel.csv'
        NOVELS = csv_to_object_list(TEST_CSV)
        NEW_LIST = update_chapter(NOVELS)
        self.assertEqual(NEW_LIST[0].latest_chapter, 674)


if __name__ == '__main__':
    unittest.main()
