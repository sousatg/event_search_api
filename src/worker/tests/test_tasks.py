import unittest

import datetime
from lxml import etree
from worker.tasks import parse_doc_to_event


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
