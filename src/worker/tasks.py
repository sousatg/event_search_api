import requests
import concurrent.futures
from worker.celery import app
from lxml import etree
from sqlalchemy.orm import Session
from worker.database import SessionLocal
from uuid import uuid4
from api.models import Event
from datetime import datetime
from worker.util import get_element


@app.task
def save_event_in_the_database(event):
    session: Session = SessionLocal()

    entity = Event()

    entity.id = str(uuid4())
    entity.title = event.get("title", None)
    entity.internal_id = event.get("internal_id", None)
    entity.start_date = event.get("start_date", None)
    entity.start_time = event.get("start_time", None)
    entity.end_date = event.get("end_date", None)
    entity.end_time = event.get("end_time", None)
    entity.min_price = event.get("min_price", None)
    entity.max_price = event.get("max_price", None)

    try:
        print("Saving event in the database")
        session.add(entity)
        session.commit()
        print("Saved in the database")
    except Exception as e:
        print("Failed to save in the database: ", e, event)
        session.rollback()
        session.close()

    session.close()


def parse_doc_to_event(doc):
    sell_mode = get_element(doc, "./@sell_mode")

    if sell_mode != "online":
        return

    title = get_element(doc, "./@title")
    base_event_id = get_element(doc, "./@base_event_id")
    event_id = get_element(doc, "./event/@event_id")

    start_hour = get_element(doc, "./event/@event_start_date")
    try:
        start_hour_object = datetime.strptime(start_hour, "%Y-%m-%dT%H:%M:%S")
    except Exception as e:
        raise Exception(f"Wront datetime format: {start_hour}")

    end_hour = get_element(doc, "./event/@event_end_date")
    try:
        end_hour_object = datetime.strptime(end_hour, "%Y-%m-%dT%H:%M:%S")
    except Exception as e:
        raise Exception(f"Wront datetime format: {end_hour}")

    prices = sorted(doc.xpath("./event/zone/@price"))

    if len(prices) < 1:
        raise Exception("Missing prices")

    min_price = float(prices[0])
    max_price = float(prices[-1])

    return {
        "internal_id": f"1:{base_event_id}:{event_id}",
        "title": title,
        "end_time": end_hour_object.time(),
        "end_date": end_hour_object.date(),
        "start_date": start_hour_object.date(),
        "start_time": start_hour_object.time(),
        "min_price": min_price,
        "max_price": max_price
    }


def handle_extracted_events(doc):
    event = parse_doc_to_event(doc)
    app.send_task("worker.tasks.save_event_in_the_database", args=[event])


@app.task(bind=True, max_retries=3, retry_backoff=True)
def extract(self):
    try:
        r = requests.get("https://provider.code-challenge.feverup.com/api/events")

        if r.status_code != 200:
            print(f"HTTP connection failed with status code: {r.status_code}")
            raise Exception(
                f"HTTP connection failed with status code: {r.status_code}"
            )
        else:
            pool = concurrent.futures.ThreadPoolExecutor(max_workers=3)

            doc = etree.XML(r.content)
            for event in doc.xpath("//eventList/output/base_event"):
                pool.submit(handle_extracted_events(event))

            pool.shutdown(wait=True)
    except Exception as e:
        raise self.retry(exc=e)
