from marshmallow import fields, ValidationError

from helpers.utils import normalized_mobile


class MobilePhone(fields.Field):
    def _deserialize(self, value, attr, data):
        mobile = normalized_mobile(value)
        if mobile is None:
            raise ValidationError("invalid mobile phone number")
        return mobile.title()
