from worker.celery import app
from api.models import Event
from sqlalchemy.orm import Session
from uuid import uuid4
from worker.store_events.database import SessionLocal


@app.task
def save_event_in_the_database(event_dto):
    if type(event_dto) is not dict:
        raise Exception("Passed parameter is not a dictionary")

    session: Session = SessionLocal()

    internal_id = event_dto.get("internal_id", None)

    if internal_id is None:
        raise Exception("Missing internal id")

    event = session.query(Event).filter_by(internal_id=internal_id).one_or_none()

    if event is None:
        event = Event()
        event.id = str(uuid4())

    event.title = event_dto.get("title", event.title)
    event.start_date = event_dto.get("start_date", event.start_date)
    event.start_time = event_dto.get("start_time", event.start_time)
    event.end_date = event_dto.get("end_date", event.end_date)
    event.end_time = event_dto.get("end_time", event.end_time)
    event.min_price = event_dto.get("min_price", event.min_price)
    event.max_price = event_dto.get("max_price", event.max_price)

    try:
        session.add(event)
        session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()
