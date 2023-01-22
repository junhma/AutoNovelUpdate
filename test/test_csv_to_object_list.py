# ok

import unittest
from csv_to_object_list import csv_to_object_list

class TestCsvToObject(unittest.TestCase):
    
    # check if it's a list
    def test_is_list(self):
        TEST_CSV = 'novel.csv'
        LIST_CSV = csv_to_object_list(TEST_CSV)
        self.assertIsInstance(LIST_CSV, list)

    # check if the first entry of the list has the right title
    def test_first_entry_title(self):
        TEST_CSV = 'novel.csv'
        LIST_CSV = csv_to_object_list(TEST_CSV)
        self.assertEqual(LIST_CSV[0].title, "book1")

    # check if the first entry of the list has the right latest chapter
    def test_first_entry_chapter(self):
        TEST_CSV = 'novel.csv'
        LIST_CSV = csv_to_object_list(TEST_CSV)
        self.assertEqual(LIST_CSV[0].latest_chapter, 40)

    # check if the second entry of the list has the right link
    def test_second_entry_link(self):
        TEST_CSV = 'novel.csv'
        LIST_CSV = csv_to_object_list(TEST_CSV)
        self.assertEqual(
            LIST_CSV[1].link, "https://google.com")

if __name__ == '__main__':
    unittest.main()
