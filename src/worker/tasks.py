import requests
import concurrent.futures
from worker.celery import app
from lxml import etree
from sqlalchemy.orm import Session
from worker.database import SessionLocal
from uuid import uuid4
from api.models import Event
from datetime import datetime


@app.task(bind=True, max_retries=3, retry_backoff=True)
def save_event_in_the_database(self, event):
    session: Session = SessionLocal()

    entity = Event()

    entity.id = str(uuid4())
    entity.title = event.get("title")
    entity.internal_id = event.get("internal_id")
    entity.start_date = event.get("start_date")
    entity.start_time = event.get("start_time")
    entity.end_date = event.get("end_date")
    entity.end_time = event.get("end_time")
    entity.min_price = event.get("min_price")
    entity.max_price = event.get("max_price")

    try:
        print("Saving event in the database")
        session.add(entity)
        session.commit()
        print("Saved in the database")
    except Exception as e:
        print("Failed to save in the database")
        session.rollback()
        session.close()
        raise self.retry(exc=e)

    session.close()


@app.task(bind=True, max_retries=3, retry_backoff=True)
def extract(self):
    def parse_event(event):
        sell_mode = event.xpath("./@sell_mode").pop()

        if sell_mode != "online":
            return

        title = event.xpath("./@title").pop()

        base_event_id = event.xpath("./@base_event_id").pop()
        event_id = event.xpath("./event/@event_id").pop()

        start_hour = event.xpath("./event/@event_start_date").pop()
        start_hour_object = datetime.strptime(start_hour, "%Y-%m-%dT%H:%M:%S")

        end_hour = event.xpath("./event/@event_end_date").pop()
        end_hour_object = datetime.strptime(end_hour, "%Y-%m-%dT%H:%M:%S")

        prices = sorted(event.xpath("./event/zone/@price"))
        min_price = prices[0]
        max_price = prices[-1]

        data = {
            "internal_id": f"1:{base_event_id}:{event_id}",
            "title": title,
            "end_time": end_hour_object.time(),
            "end_date": end_hour_object.date(),
            "start_date": start_hour_object.date(),
            "start_time": start_hour_object.time(),
            "min_price": min_price,
            "max_price": max_price
        }

        app.send_task("worker.tasks.save_event_in_the_database", args=[data])

    try:
        r = requests.get("http://localhost:5000/")

        if r.status_code != 200:
            print("Error getting the data")
            raise Exception(
                f"HTTP connection failed with status code: {r.status_code}"
            )
        else:
            pool = concurrent.futures.ThreadPoolExecutor(max_workers=3)

            doc = etree.XML(r.content)
            for event in doc.xpath("//eventList/output/base_event"):
                pool.submit(parse_event(event))

            pool.shutdown(wait=True)
    except Exception as e:
        raise self.retry(exc=e)
