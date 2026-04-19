import unittest
import io
from unittest.mock import patch, mock_open

# Import the module to be tested
import Part1

class TestDataLakeValidation(unittest.TestCase):

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('os.path.exists')
    def test_raw_data_dir_missing(self, mock_exists, mock_stdout):
        # Simulate the raw data directory not existing
        mock_exists.return_value = False
        
        Part1.run_tests()
        
        output = mock_stdout.getvalue()
        self.assertIn("[FAIL] Raw data directory does not exist.", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('os.path.exists')
    def test_files_missing(self, mock_exists, mock_stdout):
        # Return True for the directory check, but False for everything else (the files)
        mock_exists.side_effect = lambda path: path == Part1.RAW_DATA_DIR
        
        Part1.run_tests()
        
        output = mock_stdout.getvalue()
        self.assertIn("[FAIL] cms_enrollment_raw.json is missing.", output)
        self.assertIn("[FAIL] reddit_sentiment_raw.json is missing.", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('builtins.open', new_callable=mock_open, read_data="this is not valid json")
    @patch('os.path.exists')
    def test_invalid_json(self, mock_exists, mock_file, mock_stdout):
        # Simulate everything existing, but reading the file returns invalid JSON
        mock_exists.return_value = True
        
        Part1.run_tests()
        
        output = mock_stdout.getvalue()
        self.assertIn("[FAIL] cms_enrollment_raw.json contains invalid JSON.", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('builtins.open', new_callable=mock_open, read_data='{"wrong_schema": true}')
    @patch('os.path.exists')
    def test_missing_schema_keys(self, mock_exists, mock_file, mock_stdout):
        # Simulate valid JSON but missing the required keys
        mock_exists.return_value = True
        
        Part1.run_tests()
        
        output = mock_stdout.getvalue()
        self.assertIn("is missing required 'metadata' or 'records' keys.", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('builtins.open', new_callable=mock_open, read_data='{"metadata": {"record_count": 1}, "records": [{"test_key": "test_value"}]}')
    @patch('os.path.exists')
    def test_successful_parsing(self, mock_exists, mock_file, mock_stdout):
        # Simulate a perfect file structure
        mock_exists.return_value = True
        
        Part1.run_tests()
        
        output = mock_stdout.getvalue()
        self.assertIn("[PASS] cms_enrollment_raw.json parsed successfully. Contains 1 records.", output)
        self.assertIn("First record sample keys: ['test_key']", output)

if __name__ == '__main__':
    unittest.main()