import unittest
from lxml import etree
from worker.util import get_element


class TestGetElement(unittest.TestCase):
    def setUp(self):
        self.xml = """
            <root>
                <element1>Value1</element1>
                <element2>Value2</element2>
            </root>
        """

        self.doc = etree.fromstring(self.xml)

    def test_get_existing_element(self):
        xpath = '//element1'

        result = get_element(self.doc, xpath)
        self.assertEqual(result.text, 'Value1')

    def test_get_missing_element(self):
        xpath = '//element3'
        with self.assertRaises(Exception) as context:
            get_element(self.doc, xpath)
        self.assertTrue('Missing element' in str(context.exception))

    def test_empty_document(self):
        empty_doc = etree.fromstring('<root></root>')
        xpath = '//element1'
        with self.assertRaises(Exception) as context:
            get_element(empty_doc, xpath)
        self.assertTrue('Missing element' in str(context.exception))
