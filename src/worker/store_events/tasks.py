from worker.celery import app
from api.models import Event
from sqlalchemy.orm import Session
from uuid import uuid4
from worker.store_events.database import SessionLocal


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
