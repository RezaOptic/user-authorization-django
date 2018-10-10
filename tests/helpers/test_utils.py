from helpers.utils import normalized_mobile, create_sso_otp
from tests._tests import DjangoTests
from tests.sample_test_data import phone_number


class HelpersUtilsTestsCases(DjangoTests):
    def test_normalized_mobile__return_mobile_phone(self):
        result = normalized_mobile(phone_number)
        self.assertEqual(result, phone_number)

    def test_normalized_mobile__return_none(self):
        result = normalized_mobile("091929104666")
        self.assertEqual(result, None)

    def test_create_sso_otp__return_a_random_int(self):
        result = create_sso_otp()
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 1000)
        self.assertLessEqual(result, 9999)
