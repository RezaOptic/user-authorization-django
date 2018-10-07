import redis

from mysite.settings import redis_conn


def __client():
    """Get new instance of redis client
    :return: Instance of redis client
    """
    return redis.Redis(connection_pool=redis_conn)


def get_from_redis(key):
    """Get existing item with given key
    :param key: key to get value
    :return: return value
    """
    r = __client()
    return r.get(key)


def get_from_redis_with_zrangebyscore(key, _min, _max):
    """
    get existing items with key and min and max score
    :param key: key to get value
    :param _min: min score value
    :param _max: max score value
    :return: value of redis
    """
    r = __client()
    return r.zrangebyscore(key, _min, _max)


def save_to_redis(key, data, ex):
    """Save data with given key with
    expiration with given ex as seconds
    :param key: key to save data with.
    :param data: data to save in redis
    :param ex: expiration time in seconds
    """
    r = __client()
    r.set(key, data, ex=ex)


def save_to_redis_with_score(key, value, score):
    """Save data with given key and value and score of value
    :param key: key to save data with.
    :param value: value to save in key
    :param score: score of value
    """
    r = __client()
    r.zadd(key, value, score)


def delete_redis_by_key(key):
    """Delete existing item from db with given key
    :param key: key to remove data
    :return: True if deleted, Otherwise returns False
    """
    r = __client()
    result = r.delete(key)
    return result is not None
