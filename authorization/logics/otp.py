from datetime import datetime, timedelta

from authorization.logics.users import generate_token
from helpers.redis_manager import (get_from_redis,
                                   save_to_redis,
                                   save_to_redis_with_score,
                                   delete_redis_by_key,
                                   get_from_redis_with_zrangebyscore
                                   )
from helpers.utils import create_sso_otp
from services.otp import send_otp


def set_otp(phone_number):
    value = get_from_redis(phone_number)
    current_time = int(datetime.utcnow().timestamp())
    if not value:
        otp = create_sso_otp()
        data = str(otp) + ":" + str(current_time)
        save_to_redis(phone_number, data, 120)
        _otp = otp
    else:
        _otp, time = value.decode("utf-8").split(":")
        if (int(time) + 60) <= current_time:
            otp = create_sso_otp()
            data = str(otp) + ":" + str(current_time)
            save_to_redis(phone_number, data, 120)
            _otp = otp

    # send_otp.delay(phone_number, int(_otp))
    send_otp(phone_number, int(_otp))
    key = phone_number + ":" + "try"
    value = score = int(datetime.utcnow().timestamp())
    save_to_redis_with_score(key, value, score)
    return True


def validate_otp(phone, otp):
    if not get_otp(phone, otp):
        return None, False
    token = generate_token(phone)
    return token, True


def get_otp(phone_number, otp):
    value = get_from_redis(phone_number)
    if value:
        _otp, time = value.decode("utf-8").split(":")
        if _otp and otp == int(_otp):
            delete_redis_by_key(phone_number)
            return True
    return False


def check_access_phone_number_to_otp(phone_number):
    _min = int((datetime.utcnow() - timedelta(days=7)).timestamp())
    _max = int(datetime.utcnow().timestamp())
    key = phone_number + ":" + "block"
    value = get_from_redis_with_zrangebyscore(key, _min, "+inf")
    if value and _max < int(value[-1].decode("utf-8")):
        return False
    return True


def check_max_otp_request_and_block(phone_number):
    _min = int((datetime.utcnow() - timedelta(minutes=2)).timestamp())
    _max = int(datetime.utcnow().timestamp())
    key = phone_number + ":" + "try"
    value = get_from_redis_with_zrangebyscore(key, _min, _max)
    if len(value) > 3:
        key = phone_number + ":" + "block"
        _min = int((datetime.utcnow() - timedelta(days=7)).timestamp())
        value = get_from_redis_with_zrangebyscore(key, _min, "+inf")
        minutes = 2 ** len(value)
        score = int((datetime.utcnow() + timedelta(minutes=minutes)).timestamp())
        save_to_redis_with_score(key, score, score)
        return False
    else:
        return True
