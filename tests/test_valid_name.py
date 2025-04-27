import os
import sys
import unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import is_valid_name

class TestNameValidation(unittest.TestCase):

    def test_valid_names(self):
        """Проверяем корректные имена."""
        self.assertEqual(is_valid_name("Report one"), "Report one")
        self.assertEqual(is_valid_name("Report"), "Report")

    def test_invalid_names(self):
        self.assertEqual(is_valid_name("Cool's report"), "")  # Пробелы допустимы
        self.assertEqual(is_valid_name("Report!@#$%^&*()"), "")
        self.assertEqual(is_valid_name("Report #123"), "")
        self.assertEqual(is_valid_name(""), "")  # Пустая строка

if __name__ == '__main__':
    unittest.main()
