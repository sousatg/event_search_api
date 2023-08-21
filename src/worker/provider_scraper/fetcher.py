import requests
import concurrent.futures

from lxml import etree
from worker.provider_scraper.util import get_element
from worker.store_events.tasks import save_event_in_the_database
from datetime import datetime


class DataFetcher:
    def __init__(self, url, provider_id):
        self._url = url
        self._data = None
        self._provider_id = provider_id

    def fetch_data(self):
        response = requests.get(self._url)

        if response.status_code != 200:
            raise requests.exceptions.HTTPError()

        self._data = response.content

    def parse_xml(self):
        root = etree.XML(self._data)
        event_list = root.xpath("//base_event[@sell_mode='online']/event")

        return event_list

    def process_event(self, root):
        base_event_id = get_element(root, "../@base_event_id")
        event_id = get_element(root, "./@event_id")
        title = get_element(root, "../@title")

        start_hour = get_element(root, "./@event_start_date")
        try:
            start_hour_object = datetime.strptime(start_hour, "%Y-%m-%dT%H:%M:%S")
        except Exception:
            raise Exception(f"Wront datetime format: {start_hour}")

        end_hour = get_element(root, "./@event_end_date")
        try:
            end_hour_object = datetime.strptime(end_hour, "%Y-%m-%dT%H:%M:%S")
        except Exception:
            raise Exception(f"Wront datetime format: {end_hour}")

        prices = sorted(root.xpath("./zone/@price"))

        if len(prices) < 1:
            raise Exception("Missing prices")

        min_price = float(prices[0])
        max_price = float(prices[-1])

        e = {
            "internal_id": f"{self._provider_id}:{base_event_id}:{event_id}",
            "title": title,
            "end_time": end_hour_object.time(),
            "end_date": end_hour_object.date(),
            "start_date": start_hour_object.date(),
            "start_time": start_hour_object.time(),
            "min_price": min_price,
            "max_price": max_price,
        }

        save_event_in_the_database.delay(e)

    def fetch_and_parse(self):
        self.fetch_data()
        events = self.parse_xml()

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            futures = [pool.submit(self.process_event, event) for event in events]
            concurrent.futures.wait(futures)
