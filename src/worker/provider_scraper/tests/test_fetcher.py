import unittest

from worker.provider_scraper.fetcher import DataFetcher
from unittest.mock import patch, Mock
from requests.exceptions import HTTPError


class TestDataFetcher(unittest.TestCase):
    @patch("worker.provider_scraper.fetcher.requests.get")
    def test_fetch_data_successful(self, mock_get):
        mock_response = Mock(status_code=200, content="response")
        mock_get.return_value = mock_response

        data_fetcher = DataFetcher("http://localhost")
        data_fetcher.fetch_data()

        self.assertEqual(data_fetcher._data, "response")

    @patch("worker.provider_scraper.fetcher.requests.get")
    def test_fetch_data_failed(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_get.return_value = mock_response

        data_fetcher = DataFetcher("http://localhost")

        with self.assertRaises(HTTPError):
            data_fetcher.fetch_data()
