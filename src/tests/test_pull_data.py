import unittest
from unittest.mock import patch, MagicMock
from src.pull_data import pull_data


class TestPullDataFunction(unittest.TestCase):
    @patch('requests.get')
    def test_successful_request(self, mock_get):
        # Set up the mock response for a successful request
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = 'Mocked data response'

        # Call the function with the mocked response
        result = pull_data('https://example.com')

        # Add your assertions here based on the expected behavior of pull_data
        self.assertEqual(result, 'Mocked data response')

    @patch('requests.get')
    def test_unsuccessful_request(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = 'Mocked error response'
        mock_get.return_value = mock_response

        # Call the function with the mocked response
        result = pull_data('https://example.com')

        # Add your assertions here based on the expected behavior of pull_data for unsuccessful requests
        self.assertEqual(result, 'Mocked error response')

if __name__ == '__main__':
    unittest.main()