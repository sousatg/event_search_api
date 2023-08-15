from api.extensions import ma
from marshmallow import fields


class SearchSchema(ma.Schema):
    starts_at = fields.DateTime()
    ends_at = fields.DateTime()
