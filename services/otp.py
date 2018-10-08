import requests
from django.conf import settings


# @celery.task(bind=True, max_retries=10)
def send_otp(phone_number, otp):
    pass
    # try:
    #     url = settings.SMS_PANEL_URL
    #     headers = {"Authorization": settings.SMS_PANEL_TOKEN,
    #                "Content-Type": "application/json"}
    #     data = {}
    #     response = requests.post(url, json=data)
    #     if response.ok:
    #         return True
    # except Exception as e:
    #     print(e)
    #     send_otp.retry(countdown=2 ** send_otp.request.retries)
