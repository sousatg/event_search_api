from api.tests.functional.base import BaseTestCase


class EventSearchTestCase(BaseTestCase):
    url = "/search"

    def test_search_events(self):
        response = self._client.get(self.url)

        self.assertEqual(response.status_code, 200)
