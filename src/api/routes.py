from flask import Blueprint, request, jsonify
from api.schemas import SearchSchema, EventSchema
from api.models import Event
from datetime import datetime
from sqlalchemy.sql import and_

bp = Blueprint("main", __name__)


@bp.route("/")
async def index():
    return "ok"


@bp.route("/search", methods=["GET"])
async def search_events():
    errors = SearchSchema().validate(request.args)

    if errors:
        return (
            jsonify(
                {
                    "error": {"code": 400, "message": "Bad Request"},
                    "data": None,
                }
            ),
            400,
        )

    starts_at = request.args.get("starts_at", None)
    ends_at = request.args.get("ends_at", None)

    start_date = datetime.strptime(starts_at, "%Y-%m-%dT%H:%M:%SZ")
    end_date = datetime.strptime(ends_at, "%Y-%m-%dT%H:%M:%SZ")

    all_events = Event.query.filter(
        and_(
            Event.start_date + Event.start_time <= end_date,
            Event.end_date + Event.end_time >= start_date
        )
    ).all()

    result = EventSchema(many=True).dump(all_events)

    response = {"data": {"events": result}, "error": None}

    return response
