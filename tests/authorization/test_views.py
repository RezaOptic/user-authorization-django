import json
from unittest.mock import patch
from tests._tests import DjangoTests
from tests.sample_test_data import phone_number, fake_token


class AuthorizationViewsTestsCases(DjangoTests):
    @patch("authorization.views.set_otp")
    def test_send_otp_controller__return_204_success_send_otp(self, mock_set_otp):
        mock_set_otp.return_value = True

        data = json.dumps({"phone_number": phone_number})
        result = self.client.post("/auth/otp", data=data, content_type="application/json")
        self.assertEqual(result.status_code, 204)

    @patch("authorization.views.set_otp")
    def test_send_otp_controller__return_400_internal_error(self, mock_set_otp):
        mock_set_otp.return_value = False

        data = json.dumps({"phone_number": phone_number})
        result = self.client.post("/auth/otp", data=data, content_type="application/json")
        self.assertEqual(result.status_code, 400)

    @patch("authorization.views.validate_otp")
    def test_verify_otp_controller__return_200_success_verify_otp(self, mock_validate_otp):
        mock_validate_otp.return_value = (fake_token, True)
        data = json.dumps({"phone_number": phone_number, "otp": 1111})
        result = self.client.post("/auth/otp/verify", data=data, content_type="application/json")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result._headers.get("x-access-token")[1], fake_token)

    def test_verify_otp_controller__return_400_otp_missing(self):
        data = json.dumps({"phone_number": phone_number})
        result = self.client.post("/auth/otp/verify", data=data, content_type="application/json")
        self.assertEqual(result.status_code, 400)

    @patch("authorization.views.validate_otp")
    def test_verify_otp_controller__return_401_wrong_otp(self, mock_validate_otp):
        mock_validate_otp.return_value = (None, False)
        data = json.dumps({"phone_number": phone_number, "otp": 2222})
        result = self.client.post("/auth/otp/verify", data=data, content_type="application/json")
        self.assertEqual(result.status_code, 401)
