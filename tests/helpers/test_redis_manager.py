import redis
from helpers.redis_manager import (get_from_redis,
                                   save_to_redis,
                                   delete_redis_by_key,
                                   get_from_redis_with_zrangebyscore,
                                   save_to_redis_with_score
                                   )
from tests._tests import DjangoTests
from mysite.settings import redis_conn


class HelpersRedisManagerTestsCases(DjangoTests):
    def setUp(self):
        self.r = redis.Redis(connection_pool=redis_conn)

    def test_save_to_redis(self):
        save_to_redis("test", "test", 10)
        result = self.r.get("test")
        self.assertEqual(result.decode("utf-8"), "test")

    def test_get_from_redis__return_value(self):
        self.r.set("test", "test", 10)
        result = get_from_redis("test")
        self.assertEqual(result.decode("utf-8"), "test")

    def test_delete_redis_by_key(self):
        self.r.set("test", "test", 10)
        delete_redis_by_key("test")
        result = self.r.get("test")
        self.assertEqual(result, None)

    def test_get_from_redis_with_zrangebyscore(self):
        self.r.zadd("test", "test", 1)
        result = get_from_redis_with_zrangebyscore("test", "-inf", "+inf")
        self.assertEqual(result[0].decode("utf-8"), "test")

    def test_save_to_redis_with_score(self):
        save_to_redis_with_score("test", "test", 1)
        result = self.r.zrangebyscore("test", "-inf", "+inf")
        self.assertEqual(result[0].decode("utf-8"), "test")

    def tearDown(self):
        self.r.flushall()
