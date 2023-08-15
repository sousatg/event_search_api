from flask import Blueprint


bp = Blueprint('main', __name__)


@bp.route("/")
async def index():
    return "ok"
