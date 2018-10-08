from django.test import TestCase
from authorization.models import User


class DjangoTests(TestCase):
    def setUp(self):
        User.objects.create(mobile_phone="09192910466", username=" ")
        User.objects.create(mobile_phone="09192910465", username=" ")

    def tearDown(self):
        pass
