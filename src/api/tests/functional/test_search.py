from api.tests.functional.base import BaseTestCase


class EventSearchTestCase(BaseTestCase):
    url = "/search"

    def test_search_events(self):
        response = self._client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_search_bad_starts_at(self):
        response = self._client.get(f"{self.url}?starts_at=None")

        self.assertEqual(response.status_code, 400)

    def test_search_bad_ends_at(self):
        response = self._client.get(f"{self.url}?ends_at=None")

        self.assertEqual(response.status_code, 400)

    def test_search_bad_starts_at_and_ends_at(self):
        response = self._client.get(f"{self.url}?starts_at=None&ends_at=None")

        self.assertEqual(response.status_code, 400)
