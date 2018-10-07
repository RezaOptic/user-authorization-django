from django.conf import settings
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer)

from authorization.models import User


def generate_token(phone):
    user = get_or_create_user(phone)
    s = Serializer(settings.SECRET_KEY, expires_in=2592000)
    return s.dumps({'id': user.get().id})


def get_or_create_user(phone):
    user = User.get_or_create_user(phone)
    return user



