from unittest import mock, main, TestCase
from api.initialization import init_http_handlers
from api.handlers import HttpHandlers


class TestInitiHttpHandlers(TestCase):
    "test class for the method 'init_http_handlers'"

    def test_valid_1(self):
        "succesfully init the class static fields"
        init_http_handlers("localhost", 1234, "pass")

        self.assertIsNotNone(HttpHandlers.redis_client)
        self.assertEqual(HttpHandlers.HTTP_STATUS_OK, 200)
        self.assertEqual(HttpHandlers.HTTP_STATUS_INTERNAL_SERVER_ERROR, 500)

    @mock.patch('api.initialization.redis.Redis', side_effect=RuntimeError("Test Exception"))
    def test_invalid_1(self, m_redis):
        "exception encountered instantiating the redis object"
        with self.assertRaises(ConnectionError):
            init_http_handlers("localhost", 1234, "pass")

    def test_invalid_2(self):
        "invalid args given to method"
        with self.assertRaises(ValueError):
            init_http_handlers("", 1234, "pass")


if __name__ == "__main__":
    main()
