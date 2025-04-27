import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import DatabaseLogs


class TestDatabaseLogs(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseLogs()

    def test_add_loglevel(self):
        self.db.add_loglevel('INFO', '/api/test')
        self.assertEqual(self.db.get_total_count(), 1)
        report = self.db.get_report()
        self.assertEqual(report[0][0], '/api/test')
        self.assertEqual(report[0][1], 0)
        self.assertEqual(report[0][2], 1)
        self.assertEqual(report[0][3], 0)
        self.assertEqual(report[0][4], 0)
        self.assertEqual(report[0][5], 0)

    def closeDB(self):
        self.db.close()

if __name__ == '__main__':
    unittest.main()
