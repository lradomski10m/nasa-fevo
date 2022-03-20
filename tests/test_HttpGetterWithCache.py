import unittest
from unittest.mock import MagicMock, patch


from nasa_fevo.HttpGetterWithCache import HttpGetterWithCache

from nasa_fevo.InMemoryCache import InMemoryCache
from nasa_fevo.HttpGetter import HttpGetter

from test_data import TEST_RESP


class HttpGetterWithCacheTest(unittest.IsolatedAsyncioTestCase):
    async def test_cache_hit(self):
        cache = MagicMock()
        cache.get.return_value = TEST_RESP

        getter = HttpGetterWithCache(cache)

        TEST_URL = "http://test.url.com"
        resp = await getter.get(TEST_URL)
        cache.get.assert_called_with(TEST_URL)
        self.assertEqual(resp, TEST_RESP)

        cache.put.assert_not_called()

    async def test_cache_miss(self):
        cache = MagicMock()
        cache.get.return_value = None

        getter = HttpGetterWithCache(cache)

        TEST_URL = "http://test.url.com"
        with patch("nasa_fevo.HttpGetter.requests.get") as reqs_get:
            mock_resp = MagicMock()
            mock_resp.json.return_value = TEST_RESP
            reqs_get.return_value = mock_resp

            resp = await getter.get(TEST_URL)
            mock_resp.json.assert_called_once()

        cache.get.assert_called_with(TEST_URL)
        reqs_get.assert_awaited_once_with(TEST_URL)
        self.assertEqual(resp, TEST_RESP)

        cache.put.assert_called_once()


if __name__ == '__main__':
    unittest.main()
