import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tempfile import NamedTemporaryFile
from main import read_logs_to_list


class TestReadLogs(unittest.TestCase):
    def test_reading_valid_file(self):
        log_content = (
            "2025-03-26 12:24:27,000 INFO django.request: GET /api/v1/reviews/ 200 OK [192.168.1.41]\n"
            "2025-03-26 12:49:53,000 ERROR django.request: Internal Server Error: /admin/dashboard/ [192.168.1.64] - \n"
            "2025-03-26 12:49:57,000 INFO django.request: Internal Server Error: /api/v1/reviews/ [192.168.1.64] - \n"
        )

        template_log = (
            "INFO /api/v1/reviews/\nERROR /admin/dashboard/\nINFO /api/v1/reviews/\n"
        )

        with NamedTemporaryFile(delete=False, mode="w") as temp_file:
            temp_file.write(log_content)
            temp_file_path = temp_file.name
        try:
            result = read_logs_to_list(temp_file_path)
            expected_result = template_log.splitlines()
            print(expected_result)
            self.assertEqual(result, expected_result)
        finally:
            os.remove(temp_file_path)

    def test_reading_invalid_file(self):
        result = read_logs_to_list("non_existing_file.log")
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
