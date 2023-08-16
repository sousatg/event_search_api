import requests
import concurrent.futures

from api.models import Event
from sqlalchemy.orm import Session
from uuid import uuid4
from lxml import etree
from datetime import datetime
from worker.celery import app
from worker.database import SessionLocal
from worker.util import get_element


@app.task
def save_event_in_the_database(event):
    if type(event) is not dict:
        raise Exception('Passed parameter is not a dictionary')

    session: Session = SessionLocal()

    internal_id = event.get('internal_id', None)

    if internal_id is None:
        raise Exception('Missing internal id')

    result = session.query(Event).filter_by(internal_id=internal_id).one_or_none()

    # Terminate task if internal_id already exists in the database
    if result is not None:
        return

    try:
        entity = Event()

        entity.id = str(uuid4())
        entity.title = event.get('title', None)
        entity.internal_id = event.get('internal_id', None)
        entity.start_date = event.get('start_date', None)
        entity.start_time = event.get('start_time', None)
        entity.end_date = event.get('end_date', None)
        entity.end_time = event.get('end_time', None)
        entity.min_price = event.get('min_price', None)
        entity.max_price = event.get('max_price', None)

        session.add(entity)
        session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()

        raise Exception('Failed to save event in the database')

    session.close()


def parse_doc_to_event(doc):
    sell_mode = get_element(doc, './@sell_mode')

    if sell_mode != 'online':
        return

    title = get_element(doc, './@title')
    base_event_id = get_element(doc, './@base_event_id')
    event_id = get_element(doc, './event/@event_id')

    start_hour = get_element(doc, './event/@event_start_date')
    try:
        start_hour_object = datetime.strptime(start_hour, '%Y-%m-%dT%H:%M:%S')
    except Exception:
        raise Exception(f'Wront datetime format: {start_hour}')

    end_hour = get_element(doc, './event/@event_end_date')
    try:
        end_hour_object = datetime.strptime(end_hour, '%Y-%m-%dT%H:%M:%S')
    except Exception:
        raise Exception(f'Wront datetime format: {end_hour}')

    prices = sorted(doc.xpath('./event/zone/@price'))

    if len(prices) < 1:
        raise Exception('Missing prices')

    min_price = float(prices[0])
    max_price = float(prices[-1])

    return {
        'internal_id': f'1:{base_event_id}:{event_id}',
        'title': title,
        'end_time': end_hour_object.time(),
        'end_date': end_hour_object.date(),
        'start_date': start_hour_object.date(),
        'start_time': start_hour_object.time(),
        'min_price': min_price,
        'max_price': max_price
    }


def handle_extracted_events(doc):
    event = parse_doc_to_event(doc)

    if event is None:
        return

    app.send_task('worker.tasks.save_event_in_the_database', args=[event])



@app.task(bind=True, max_retries=3, retry_backoff=True)
def extract(self):
    try:
        r = requests.get('https://provider.code-challenge.feverup.com/api/events')

        if r.status_code != 200:
            raise Exception(
                f'HTTP connection failed with status code: {r.status_code}'
            )
        else:
            pool = concurrent.futures.ThreadPoolExecutor(max_workers=3)

            doc = etree.XML(r.content)
            event_list = doc.xpath('//eventList/output/base_event')

            for event in event_list:
                pool.submit(handle_extracted_events(event))

            pool.shutdown(wait=True)
    except Exception as e:
        raise self.retry(exc=e)
