from src.api.extensions import db
from sqlalchemy.types import Float, String, Date, DateTime


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(String, primary_key=True)
    title = db.Column(String, nullable=False)
    start_date = db.Column(Date, nullable=False)
    start_time = db.Column(DateTime, nullable=False)
    end_date = db.Column(Date, nullable=False)
    end_time = db.Column(DateTime, nullable=False)
    min_price = db.Column(Float, nullable=False)
    max_price = db.Column(Float, nullable=False)
