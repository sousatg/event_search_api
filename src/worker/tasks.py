import requests
import concurrent.futures
from .celery import app
from lxml import etree


def parse_event(event):
    sell_mode = event.xpath("./@sell_mode").pop()

    if sell_mode != "online":
        return

    name = event.xpath("./@title").pop()

    base_event_id = event.xpath("./@base_event_id").pop()
    event_id = event.xpath("./event/@event_id").pop()

    start_hour = event.xpath("./event/@event_start_date").pop()
    end_hour = event.xpath("./event/@event_end_date").pop()

    prices = sorted(event.xpath("./event/zone/@price"))
    min_price = prices[0]
    max_price = prices[-1]

    data = {
        "internal_id": f"{base_event_id}:{event_id}",
        "name" : name,
        "start_hour" : start_hour,
        "end_hour" : end_hour,
        "min_price" : min_price,
        "max_price" : max_price
    }

    app.send_task("extractor.tasks.save_event_in_the_database", args=[data])


@app.task
def save_event_in_the_database(event):
    print(event)
    print("Saving event in the database")


@app.task
def add():
    r = requests.get("http://localhost:5000/")

    if r.status_code != 200:
        print("Error getting the data")
        raise Exception("HTTP Request Failed")
        # Add a retry

    else:
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=3)

        doc = etree.XML(r.content)
        for event in doc.xpath("//eventList/output/base_event"):
            pool.submit(parse_event(event))

        pool.shutdown(wait=True)
