import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import DatabaseLogs


class TestDatabaseLogs(unittest.TestCase):
    def setUp(self):
        self.db_logs = DatabaseLogs()

    def tearDown(self):
        self.db_logs.close()

    def test_get_total_count_initial(self):
        self.assertEqual(self.db_logs.get_total_count(), 0)

    def test_get_total_count_after_adding(self):
        self.db_logs.add_loglevel("INFO", "/api/test1")
        self.db_logs.add_loglevel("ERROR", "/api/test2")

        self.assertEqual(self.db_logs.get_total_count(), 2)

    def test_get_total_count_after_removing(self):
        self.db_logs.add_loglevel("INFO", "/api/test1")
        self.db_logs.add_loglevel("ERROR", "/api/test2")
        self.assertEqual(self.db_logs.get_total_count(), 2)


if __name__ == "__main__":
    unittest.main()
