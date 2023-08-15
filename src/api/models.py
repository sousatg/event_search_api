from src.api.extensions import db


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    start_date = db.Column(db.Date, nullable=False, index=True)
    start_time = db.Column(db.Time, nullable=False, index=True)
    end_date = db.Column(db.Date, nullable=False, index=True)
    end_time = db.Column(db.Time, nullable=False, index=True)
    min_price = db.Column(db.Float, nullable=False)
    max_price = db.Column(db.Float, nullable=False)
