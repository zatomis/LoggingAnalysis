import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tempfile import NamedTemporaryFile
from main import file_exists


class TestFileExists(unittest.TestCase):
    def test_existing_file(self):
        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file_path = temp_file.name
        try:
            self.assertTrue(file_exists(temp_file_path))
        finally:
            os.remove(temp_file_path)

    def test_non_existing_file(self):
        self.assertFalse(file_exists("no_file.txt"))


if __name__ == "__main__":
    unittest.main()
