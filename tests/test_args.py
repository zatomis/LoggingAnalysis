import os
from unittest.mock import patch
import sys
import unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import main

class TestMain(unittest.TestCase):

    @patch('sys.exit')
    def test_main_arguments(self, mock_exit):
        test_args = ['main.py', 'logs/app1.log', 'logs/app2.log', 'logs/app3.log', '--report', 'Report']
        with patch('sys.argv', test_args):
            main()
        # Проверяем, что sys.exit не вызывался (то есть приложение запустилось успешно)
        mock_exit.assert_not_called()


if __name__ == '__main__':
    unittest.main()
