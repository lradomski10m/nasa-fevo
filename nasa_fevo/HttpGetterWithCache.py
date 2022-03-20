from nasa_fevo.HttpGetter import HttpGetter
from nasa_fevo.Cache import Cache
from datetime import date, timedelta, datetime


class HttpGetterWithCache(HttpGetter):
    def __init__(self, cache: Cache):
        super(HttpGetterWithCache, self).__init__()
        self._cache = cache

    async def get(self, url: str) -> object:
        resp = self._cache.get(url)
        if resp is not None:
            return resp
        else:
            resp = await super().get(url)
            today = date.today()
            expires_next_day = datetime.combine(today + timedelta(days=1), datetime.min.time())
            self._cache.put(url, resp, expires_next_day)

        return resp
