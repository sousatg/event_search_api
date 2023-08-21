import unittest

from unittest.mock import patch, MagicMock
from worker.store_events.tasks import save_event_in_the_database
from api.models import Event


class TestSaveEventInTheDatabase(unittest.TestCase):
    def test_passing_empty_event_property(self):
        with self.assertRaises(Exception) as context:
            save_event_in_the_database(None)

        self.assertTrue(
            "Passed parameter is not a dictionary" in str(context.exception)
        )

    def test_missing_internal_id(self):
        event = {
            "title": "Test Event",
        }

        with self.assertRaises(Exception) as context:
            save_event_in_the_database(event)

        self.assertTrue("Missing internal id" in str(context.exception))

    @patch("worker.store_events.tasks.SessionLocal")
    def test_event_with_internal_id_already_exists(self, mock_session):
        mock_db_session = MagicMock()
        mock_db_session.query.return_value.filter_by.return_value.one_or_none.return_value = (
            Event()
        )
        mock_session.return_value = mock_db_session

        event = dict(
            {
                "internal_id": "existing_id",
                "title": "Test Event",
            }
        )

        save_event_in_the_database(event)

        mock_db_session.add.assert_not_called()
