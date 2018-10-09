import json
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from marshmallow import ValidationError

from authorization.logics.otp import set_otp, validate_otp
from helpers.decorators import login_required, otp_firewall
from helpers.exceptions import AuthorizationError
from .models import OTP, OTPVerify


@require_http_methods(["POST"])
@otp_firewall()
def send_otp(request):
    args = OTP(strict=True).load(json.loads(request.body or {}))[0]
    if set_otp(args["phone_number"]):
        return JsonResponse(status=204, data=None, safe=False)
    raise ValidationError("Internal Service Error")


@require_http_methods(["POST"])
def verify_otp(request):
    args = OTPVerify(strict=True).load(json.loads(request.body or {}))[0]
    token, verify = validate_otp(args["phone_number"], args["otp"])
    if verify:
        response = JsonResponse(data=None, status=200, safe=False)
        response["X-Access-Token"] = token
        return response
    raise AuthorizationError


@require_http_methods(["GET"])
@login_required
def verify_token(request):
    if request.user:
        data = {"mobile_phone": request.user.mobile_phone}
        return JsonResponse(data=data, status=200)
