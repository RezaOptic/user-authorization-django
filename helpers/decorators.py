from django.conf import settings
from django.contrib.auth.models import User
from functools import wraps

from django.http import JsonResponse
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


def login_required(f):
    @wraps(f)
    def wrapped(request, *args, **kwargs):
        s = Serializer(settings.SECRET_KEY)
        try:
            token = request.headers.get('Authorization', None)
            data = s.loads(token)
            request.user = User.objects.get(data['id'])
        except SignatureExpired:
            return JsonResponse(data={"message": "token is expire"}, status=401)
        except BadSignature:
            return JsonResponse(data={"message": "token is invalid"}, status=401)
        except Exception as e:
            print(e)
            return JsonResponse(data={"message": "token is invalid"}, status=401)
        return f(request, *args, **kwargs)
    return wrapped
