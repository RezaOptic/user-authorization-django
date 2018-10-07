import json
from datetime import datetime

from django.test import TestCase
from authorization.models import User
# Create your tests here.
from helpers.redis_manager import save_to_redis


class OTPTestCase(TestCase):
    def setUp(self):
        User.objects.create(mobile_phone="09192910466", username=" ")
        User.objects.create(mobile_phone="09192910465", username=" ")

    def test_send_otp__return_204_success_send_otp(self):
        data = json.dumps({"phone_number": "09192910466"})
        result = self.client.post("/auth/otp", data=data, content_type="application/json")
        self.assertEqual(result.status_code, 204)

    def test_verify_otp__return_200_success_verify_otp(self):
        phone_number = "09192910466"
        otp = 1111
        current_time = int(datetime.utcnow().timestamp())
        data = str(otp) + ":" + str(current_time)
        save_to_redis(phone_number, data, 120)
        data = json.dumps({"phone_number": phone_number, "otp": 1111})
        result = self.client.post("/auth/otp/verify", data=data, content_type="application/json")
        self.assertEqual(result.status_code, 200)
        self.assertIsInstance(result._headers.get("x-access-token"), tuple)

    def test_verify_otp__return_400_otp_missing(self):
        data = json.dumps({"phone_number": "09192910466"})
        result = self.client.post("/auth/otp/verify", data=data, content_type="application/json")
        self.assertEqual(result.status_code, 400)

    def test_verify_otp__return_401_wrong_otp(self):
        data = json.dumps({"phone_number": "09192910466", "otp": 2222})
        result = self.client.post("/auth/otp/verify", data=data, content_type="application/json")
        self.assertEqual(result.status_code, 401)
