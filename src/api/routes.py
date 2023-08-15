from flask import Blueprint, request, jsonify
from api.schemas import SearchSchema


bp = Blueprint('main', __name__)


@bp.route("/")
async def index():
    return "ok"


@bp.route("/search", methods=["GET"])
async def search_events():
    errors = SearchSchema().validate(request.args)

    if errors:
        print(errors)
        return jsonify({
            "error": {
                "code": "INVALID_INPUT",
                "message": "INVALID_INPUT"
            },
            "data": errors
        }), 400

    return {}
