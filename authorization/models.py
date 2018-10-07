# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from marshmallow import Schema, fields
from helpers.custome_fields import MobilePhone


class User(AbstractUser):
    mobile_phone = models.CharField(max_length=15, unique=True)
    username = models.CharField(
        max_length=150,
    )

    @staticmethod
    def get_or_create_user(phone):
        user = User.objects.filter(mobile_phone=phone)
        if user:
            return user
        user = User.objects.create_user(mobile_phone=phone, username=" ")
        return user

    USERNAME_FIELD = 'mobile_phone'
    REQUIRED_FIELDS = []


class OTP(Schema):
    phone_number = MobilePhone(required=True)


class OTPVerify(OTP):
    otp = fields.Integer(required=True)

