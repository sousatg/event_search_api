from api.extensions import ma
from marshmallow import fields


class SearchSchema(ma.Schema):
    starts_at = fields.DateTime(required=True, allow_none=False)
    ends_at = fields.DateTime(required=True, allow_none=False)


class EventSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'title',
            'start_date',
            'start_time',
            'end_date',
            'end_time',
            'min_price',
            'max_price'
        )
