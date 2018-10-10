from unittest.mock import patch

from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from authorization.logics.users import generate_token
from tests._tests import DjangoTests
from tests.sample_test_data import phone_number


class AuthorizationLogicsUsersTestsCases(DjangoTests):

    @patch("authorization.logics.users.User.get_or_create_user")
    def test_generate_token__return_access_token(self, get_or_create_user):
        get_or_create_user.return_value.id = 1

        data = generate_token(phone_number)
        s = Serializer(settings.SECRET_KEY)
        data = s.loads(data)
        self.assertEqual(data["id"], 1)
