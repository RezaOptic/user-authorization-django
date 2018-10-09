from datetime import datetime
from unittest.mock import patch

from authorization.logics.otp import (set_otp,
                                      get_otp,
                                      validate_otp,
                                      check_access_phone_number_to_otp,
                                      check_max_otp_request_and_block
                                      )
from tests._tests import DjangoTests
from tests.sample_test_data import phone_number, fake_token


class AuthorizationLogicsOTPTestsCases(DjangoTests):
    @patch("authorization.logics.otp.save_to_redis_with_score")
    @patch("authorization.logics.otp.send_otp")
    @patch("authorization.logics.otp.create_sso_otp")
    @patch("authorization.logics.otp.get_from_redis")
    def test_send_otp_logic__return_true_success_send_otp(self, get_from_redis, create_sso_otp, send_otp,
                                                          save_to_redis_with_score):
        get_from_redis.return_value = bytearray("1111:{}".format(int(datetime.utcnow().timestamp())), encoding="utf-8")
        create_sso_otp.return_value = 1111
        send_otp.return_value = True
        save_to_redis_with_score.return_value = True

        data = set_otp(phone_number)
        self.assertEqual(data, True)

    @patch("authorization.logics.otp.save_to_redis_with_score")
    @patch("authorization.logics.otp.send_otp")
    @patch("authorization.logics.otp.create_sso_otp")
    @patch("authorization.logics.otp.get_from_redis")
    def test_send_otp_logic__return_true_generate_new_otp(self, get_from_redis, create_sso_otp, send_otp,
                                                          save_to_redis_with_score):
        get_from_redis.return_value = bytearray("1111:{}".format(int(datetime.utcnow().timestamp())-70),
                                                encoding="utf-8")
        create_sso_otp.return_value = 1111
        send_otp.return_value = True
        save_to_redis_with_score.return_value = True

        data = set_otp(phone_number)
        self.assertEqual(data, True)

    @patch("authorization.logics.otp.generate_token")
    @patch("authorization.logics.otp.get_otp")
    def test_validate_otp__return_true_verify_token(self, _get_otp, generate_token):
        _get_otp.return_value = True
        generate_token.return_value = fake_token

        token, verify = validate_otp(phone_number, 1111)
        self.assertEqual(verify, True)
        self.assertEqual(token, fake_token)

    @patch("authorization.logics.otp.generate_token")
    @patch("authorization.logics.otp.get_otp")
    def test_validate_otp__return_true_verify_token(self, _get_otp, generate_token):
        _get_otp.return_value = None
        generate_token.return_value = fake_token

        token, verify = validate_otp(phone_number, 1111)
        self.assertEqual(verify, False)
        self.assertEqual(token, None)

    @patch("authorization.logics.otp.delete_redis_by_key")
    @patch("authorization.logics.otp.get_from_redis")
    def test_get_otp_and_validate_it__return_true(self, get_from_redis, delete_redis_by_key):
        get_from_redis.return_value = bytearray("1111:{}".format(int(datetime.utcnow().timestamp())),
                                                encoding="utf-8")
        delete_redis_by_key.return_value = True

        result = get_otp(phone_number, 1111)
        self.assertEqual(result, True)

    @patch("authorization.logics.otp.get_from_redis")
    def test_get_otp_and_validate_it__return_false(self, get_from_redis):
        get_from_redis.return_value = None

        result = get_otp(phone_number, 1111)
        self.assertEqual(result, False)

    @patch("authorization.logics.otp.get_from_redis_with_zrangebyscore")
    def test_check_access_phone_number_to_request_otp__return_true(self, mock_get_from_redis):
        current_time = int(datetime.utcnow().timestamp())
        mock_get_from_redis.return_value = [bytearray(str(current_time-100), encoding="utf-8")]

        result = check_access_phone_number_to_otp(phone_number)
        self.assertEqual(result, True)

    @patch("authorization.logics.otp.get_from_redis_with_zrangebyscore")
    def test_check_access_phone_number_to_request_otp__return_false(self, mock_get_from_redis):
        current_time = int(datetime.utcnow().timestamp())
        mock_get_from_redis.return_value = [bytearray(str(current_time + 100), encoding="utf-8")]

        result = check_access_phone_number_to_otp(phone_number)
        self.assertEqual(result, False)

    @patch("authorization.logics.otp.get_from_redis_with_zrangebyscore")
    def test_check_max_otp_request_and_block__return_true(self, mock_get_from_redis):
        current_time = int(datetime.utcnow().timestamp())
        mock_get_from_redis.return_value = [current_time+1, current_time+2, current_time+3]

        result = check_max_otp_request_and_block(phone_number)
        self.assertEqual(result, True)

    @patch("authorization.logics.otp.save_to_redis_with_score")
    @patch("authorization.logics.otp.get_from_redis_with_zrangebyscore")
    def test_check_max_otp_request_and_block__return_false(self, mock_get_from_redis, save_to_redis_with_score):
        current_time = int(datetime.utcnow().timestamp())
        mock_get_from_redis.return_value = [current_time + 1, current_time + 2, current_time + 3,  current_time + 4]
        save_to_redis_with_score.return_value = True

        result = check_max_otp_request_and_block(phone_number)
        self.assertEqual(result, False)
