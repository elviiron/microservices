import unittest
from unittest.mock import Mock, patch
from main import Parser


class TestParser(unittest.TestCase):

    @patch('selenium.webdriver.Chrome')
    @patch('selenium.webdriver.chrome.service.Service')
    @patch('webdriver_manager.chrome.ChromeDriverManager')
    @patch('database.Database')
    def setUp(self, mock_db, mock_driver_manager, mock_service, mock_chrome):
        self.mock_driver = mock_chrome.return_value
        self.mock_db = mock_db.return_value

        self.parser = Parser()

    def test_init(self):
        self.assertIsNotNone(self.parser.driver)
        self.assertIsNotNone(self.parser.db)
        self.assertEqual(len(self.parser.urls), 3)
        self.assertTrue("--headless" in self.parser.chrome_options.arguments)

if __name__ == '__main__':
    unittest.main()





