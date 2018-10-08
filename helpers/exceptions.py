"""

"""
import json

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from marshmallow import ValidationError


class AuthorizationError(Exception):
    """Authorization exception"""

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.field = None
        self.error = args[0] if args else None


class HandleBusinessExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, exception):
        if isinstance(exception, ValidationError):
            return JsonResponse(data=exception.args, status=400, safe=False)
        elif isinstance(exception, AuthorizationError):
            return JsonResponse(data={"message": [exception.error]}, status=401, safe=False)
