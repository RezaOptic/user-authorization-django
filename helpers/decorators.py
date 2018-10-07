from django.conf import settings
from django.contrib.auth.models import User
from functools import wraps

from django.http import JsonResponse
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from authorization.logics.otp import check_access_phone_number_to_otp, check_max_otp_request_and_block
from authorization.models import OTP


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


def otp_firewall(**options):
    def _login_required(f):
        @wraps(f)
        def wrapper(request, *args, **kwargs):
            try:
                data = OTP(strict=True).load(request.get_json() or {})[0] or {}
                if check_access_phone_number_to_otp(data["phone"]):
                    if not check_max_otp_request_and_block(data["phone"]):
                        print("max otp request")
                        return JsonResponse(data={"message": "max otp request"}, status=401)
                else:
                    print("check acess phone number")
                    return JsonResponse(data={"message": "max otp request"}, status=401)
            except ForbiddenError as ex:
                print(ex)
                raise ex
            except HTTPException as ex:
                print(ex)
                raise ex
            except:
                return JsonResponse(data={"message": "max otp request"}, status=401)
            return f(request, *args, **kwargs)
        return wrapper
    return _login_required
