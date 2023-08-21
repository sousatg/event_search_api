import unittest

from worker.provider_scraper.fetcher import DataFetcher
from unittest.mock import patch, Mock
from requests.exceptions import HTTPError


class TestDataFetcher(unittest.TestCase):
    @patch("worker.provider_scraper.fetcher.requests.get")
    def test_fetch_data_successful(self, mock_get):
        mock_response = Mock(status_code=200, content="response")
        mock_get.return_value = mock_response

        data_fetcher = DataFetcher("http://localhost", "test")
        data_fetcher.fetch_data()

        self.assertEqual(data_fetcher._data, "response")

    @patch("worker.provider_scraper.fetcher.requests.get")
    def test_fetch_data_failed(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_get.return_value = mock_response

        data_fetcher = DataFetcher("http://localhost", "test")

        with self.assertRaises(HTTPError):
            data_fetcher.fetch_data()

    @patch("worker.provider_scraper.fetcher.DataFetcher.process_event")
    def test_fetch_and_parse(self, mock_process_event):
        xml_response = """
        <xml>
        <eventList>
            <output>
                <base_event sell_mode='online'>
                    <event>
                    </event>
                    <event>
                    </event>
                </base_event>
                <base_event sell_mode='place'>
                    <event>
                    </event>
                    <event>
                    </event>
                </base_event>
            </output>
        </eventList>
        </xml>
        """

        mock_process_event.return_value = None
        mock_response = Mock(status_code=200, content=xml_response)

        with patch(
            "worker.provider_scraper.fetcher.requests.get", return_value=mock_response
        ):
            fetcher = DataFetcher("https://localhost", "test")
            fetcher.fetch_and_parse()

            self.assertEqual(mock_process_event.call_count, 2)
