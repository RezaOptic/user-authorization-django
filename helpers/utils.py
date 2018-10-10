import random
import re

MOBILE_PHONE_CODES = {0: "0"}


def normalized_mobile(mobile):
    """get normalized mobile number
    :return: normalized mobile number
    :rtype: str
    """
    # TODO: handle non-iranian phone numbers
    if not mobile:
        return None
    mobile = ''.join(re.findall("(\d+)", mobile))
    r = re.findall("^(?:0|98|0098)(\d{10})$|^(?:0|216|00216)(\d{8})$", mobile)
    if not r:
        return None
    r = r[0]
    for i, j in enumerate(r):
        if j:
            return MOBILE_PHONE_CODES[i]+j
    return None
    # return "0" + r[0]


def create_sso_otp():
    return random.randrange(1000, 9999)
