from nasa_fevo.Cache import Cache
from nasa_fevo.RoverImagesRetriever import RoverImagesRetriever, \
    DEFAULT_ROVER, DEFAULT_DAYS_TO_GET, DEFAULT_IMAGES_PER_DAY

from urllib.parse import urlencode
from datetime import date, timedelta, datetime
# from nasa_fevo.HttpGetter import HttpGetter
from nasa_fevo.HttpGetterWithCache import HttpGetterWithCache


class RoverImagesRetrieverWithCache(RoverImagesRetriever):
    def __init__(self, cache: Cache):
        http_getter_with_cache = HttpGetterWithCache(cache)
        super(RoverImagesRetrieverWithCache, self).__init__(http_getter_with_cache)
        self._cache: Cache = cache

    async def get_rover_images(self,
                              rover: str = DEFAULT_ROVER,
                              days_to_get: int = DEFAULT_DAYS_TO_GET,
                              max_photos_per_day: int = DEFAULT_IMAGES_PER_DAY) -> str:

        today, url = self._make_pseudo_url_for_caching(days_to_get, max_photos_per_day, rover)

        resp = self._cache.get(url)
        if resp is not None:
            return resp
        else:
            resp = await super().get_rover_images(rover, days_to_get, max_photos_per_day)
            expires_next_day = datetime.combine(today+timedelta(days=1), datetime.min.time())
            self._cache.put(url, resp, expires_next_day)
            return resp

    def _make_pseudo_url_for_caching(self, days_to_get, max_photos_per_day, rover):
        today = date.today()
        params = {
            "today": today, "rover": rover, "days_to_get": days_to_get, "max_photos_per_day": max_photos_per_day
        }
        params = urlencode(params)
        url = f"nasa_fevo://rover-images?{params}"
        return today, url

