import json
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from authorization.logics.otp import set_otp, validate_otp
from .models import OTP, OTPVerify


@require_http_methods(["POST"])
def send_otp(request):
    args = OTP(strict=True).load(json.loads(request.body or {}))[0]
    if set_otp(args["phone_number"]):
        return JsonResponse(status=204, data={})
    return JsonResponse(data={"message": "internal error"}, status=400)


@require_http_methods(["POST"])
def verify_otp(request):
    args = OTPVerify(strict=True).load(json.loads(request.body or {}))[0]
    token, verify = validate_otp(args["phone_number"], args["otp"])
    if verify:
        response = JsonResponse(data=None, status=200, safe=False)
        response["X-Access-Token"] = token
        return response
    return JsonResponse(data={}, status=401)
