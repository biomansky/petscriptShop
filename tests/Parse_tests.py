import unittest
import requests
from bs4 import BeautifulSoup
from Parse import get_html, get_content_moizver, parse


class ParseTestCase(unittest.TestCase):
    def test_getcontent(self):
        self.assertEqual(get_content_moizver('https://moizver.com/catalog/item/6069/'), [])
        self.



if __name__ == '__main__':
    unittest.main()
