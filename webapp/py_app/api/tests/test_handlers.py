from unittest import mock, main, TestCase
from api.handlers import HttpHandlers


class TestHttpHandlers(TestCase):
    "test class for HttpHandlers"

    def test_valid_visits_1(self):
        "succesfully call the endpoint, key has not yet been setup in Redis"
        m_redis_client = mock.MagicMock()
        m_redis_client.get.return_value = None
        m_redis_client.mset.return_value = None
        HttpHandlers.redis_client = m_redis_client

        result_body, result_code = HttpHandlers.visits()

        self.assertIn("visits", result_body)
        self.assertEqual(result_body["visits"], 1)
        self.assertEqual(result_code, HttpHandlers.HTTP_STATUS_OK)

    def test_valid_visits_2(self):
        "succesfully call the endpoint, key has already been setup in Redis"
        m_redis_client = mock.MagicMock()
        m_redis_client.get.return_value = b"2"
        m_redis_client.mset.return_value = None
        HttpHandlers.redis_client = m_redis_client

        result_body, result_code = HttpHandlers.visits()

        self.assertIn("visits", result_body)
        self.assertEqual(result_body["visits"], 3)
        self.assertEqual(result_code, HttpHandlers.HTTP_STATUS_OK)

    @mock.patch('api.handlers.logging.error', return_value=None)
    def test_invalid_visits_1(self, m_logerr):
        "error when attempting to get the key from redis"
        m_redis_client = mock.MagicMock()
        m_redis_client.get.side_effect = RuntimeError("Test Redis Exception")
        HttpHandlers.redis_client = m_redis_client

        result_body, result_code = HttpHandlers.visits()

        self.assertIn("error", result_body)
        self.assertEqual(result_code, HttpHandlers.HTTP_STATUS_INTERNAL_SERVER_ERROR)

    @mock.patch('api.handlers.logging.error', return_value=None)
    def test_invalid_visits_2(self, m_logerr):
        "error when attempting to get the key from redis"
        HttpHandlers.redis_client = None

        result_body, result_code = HttpHandlers.visits()

        self.assertIn("error", result_body)
        self.assertEqual(result_code, HttpHandlers.HTTP_STATUS_INTERNAL_SERVER_ERROR)
