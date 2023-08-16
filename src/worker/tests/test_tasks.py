import unittest

import datetime
from lxml import etree
from unittest.mock import patch, MagicMock, Mock
from worker.tasks import parse_doc_to_event, save_event_in_the_database, extract


class TestSaveEvent(unittest.TestCase):
    @patch('worker.tasks.SessionLocal')
    def test_event_with_internal_id_already_exists(self, mock_session):
        mock_db_session = MagicMock()
        mock_db_session.query.return_value.filter_by.return_value.one_or_none.return_value = None
        mock_session.return_value = mock_db_session

        event = {
            'internal_id': 'existing_id',
            'title': 'Test Event',
        }

        save_event_in_the_database(event)

        mock_db_session.add.assert_not_called()

    @patch('worker.tasks.SessionLocal')
    def test_missing_internal_id(self, mock_session):
        mock_db_session = MagicMock()
        mock_db_session.query.return_value.filter_by.return_value.one_or_none.return_value = None
        mock_session.return_value = mock_db_session

        event = {
            'title': 'Test Event',
        }

        save_event_in_the_database(event)

        mock_db_session.add.assert_not_called()


class TestParseDocToEvent(unittest.TestCase):
    def test_valid_event(self):
        doc = etree.XML("""
            <base_event base_event_id="291" sell_mode="online" title="Camela en concierto">
                <event event_start_date="2021-06-30T21:00:00" event_end_date="2021-06-30T22:00:00" event_id="291" sell_from="2020-07-01T00:00:00" sell_to="2021-06-30T20:00:00" sold_out="false">
                    <zone zone_id="40" capacity="243" price="20.00" name="Platea" numbered="true" />
                    <zone zone_id="38" capacity="100" price="15.00" name="Grada 2" numbered="false" />
                    <zone zone_id="30" capacity="90" price="30.00" name="A28" numbered="true" />
                </event>
            </base_event>
        """)

        result = parse_doc_to_event(doc)

        self.assertEqual(result["title"], "Camela en concierto")
        self.assertEqual(result["min_price"], 15.00)
        self.assertEqual(result["max_price"], 30)
        self.assertIsInstance(result["start_date"], datetime.date)
        self.assertIsInstance(result["start_time"], datetime.time)
        self.assertIsInstance(result["end_date"], datetime.date)
        self.assertIsInstance(result["end_time"], datetime.time)
        self.assertEqual(result["internal_id"], "1:291:291")

    def test_missing_title(self):
        doc = etree.XML("""
            <base_event base_event_id="291" sell_mode="online">
                <event event_start_date="2021-06-30T21:00:00" event_end_date="2021-06-30T22:00:00" event_id="291" sell_from="2020-07-01T00:00:00" sell_to="2021-06-30T20:00:00" sold_out="false">
                    <zone zone_id="40" capacity="243" price="20.00" name="Platea" numbered="true" />
                    <zone zone_id="38" capacity="100" price="15.00" name="Grada 2" numbered="false" />
                    <zone zone_id="30" capacity="90" price="30.00" name="A28" numbered="true" />
                </event>
            </base_event>
        """)

        with self.assertRaises(Exception) as context:
            parse_doc_to_event(doc)

        self.assertEqual(str(context.exception), "Missing element: ./@title")

    def test_wrong_event_start_date_format(self):
        doc = etree.XML("""
            <base_event base_event_id="291" sell_mode="online" title="Camela en concierto">
                <event event_start_date="asd" event_end_date="2021-06-30T22:00:00" event_id="291" sell_from="2020-07-01T00:00:00" sell_to="2021-06-30T20:00:00" sold_out="false">
                    <zone zone_id="40" capacity="243" price="20.00" name="Platea" numbered="true" />
                    <zone zone_id="38" capacity="100" price="15.00" name="Grada 2" numbered="false" />
                    <zone zone_id="30" capacity="90" price="30.00" name="A28" numbered="true" />
                </event>
            </base_event>
        """)

        with self.assertRaises(Exception) as context:
            parse_doc_to_event(doc)

        self.assertEqual(str(context.exception), "Wront datetime format: asd")

    def test_wrong_event_end_date_format(self):
        doc = etree.XML("""
            <base_event base_event_id="291" sell_mode="online" title="Camela en concierto">
                <event event_start_date="2021-06-30T22:00:00" event_end_date="asd" event_id="291" sell_from="2020-07-01T00:00:00" sell_to="2021-06-30T20:00:00" sold_out="false">
                    <zone zone_id="40" capacity="243" price="20.00" name="Platea" numbered="true" />
                    <zone zone_id="38" capacity="100" price="15.00" name="Grada 2" numbered="false" />
                    <zone zone_id="30" capacity="90" price="30.00" name="A28" numbered="true" />
                </event>
            </base_event>
        """)

        with self.assertRaises(Exception) as context:
            parse_doc_to_event(doc)

        self.assertEqual(str(context.exception), "Wront datetime format: asd")


class TestExtract(unittest.TestCase):
    @patch('worker.tasks.requests.get')
    @patch('worker.tasks.handle_extracted_events', side_effect=lambda *args, **kwargs: None)
    def test_successful_extraction(self, mock_handle, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'<root><eventList><output><base_event>Event1</base_event></output></eventList></root>'
        mock_get.return_value = mock_response

        mock_handle.return_value = None

        extract()

        mock_get.assert_called_once()
        mock_handle.assert_called_once()

    @patch('worker.tasks.requests.get')
    @patch('worker.tasks.handle_extracted_events', side_effect=lambda *args, **kwargs: None)
    def test_failed_http_connection(self, mock_handle, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        mock_handle.return_value = None

        with self.assertRaises(Exception) as context:
            extract()

        self.assertTrue('HTTP connection failed' in str(context.exception))
        mock_handle.assert_not_called()
