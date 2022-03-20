from typing import Dict, List
from datetime import date, timedelta
from urllib.parse import urlencode
from nasa_fevo.HttpGetter import HttpGetter

DEFAULT_ROVER = "curiosity"
DEFAULT_DAYS_TO_GET = "10"
DEFAULT_IMAGES_PER_DAY = "3"

API_KEY = "6DaD1GqXObIt96eZaslCAnWuNNycEhrsPYFI9byb"
MAX_DAYS_TO_GET = 30


class RoverImagesRetriever():
    def __init__(self, http_getter: HttpGetter):
        self._fixed_params: dict = {"camera": "NAVCAM", "api_key": API_KEY}
        self._http_getter: HttpGetter = http_getter

    def _get_last_dates(self, days_to_get: int) -> List[str]:
        days_to_get = min(days_to_get, MAX_DAYS_TO_GET)  # cap it
        yesterday = date.today()-timedelta(1)

        # get last 'days_to_get' days and format as YYYY-mm-dd
        dates = [(yesterday - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days_to_get)]
        return dates

    async def get_rover_images(self,
                              rover=DEFAULT_ROVER,
                              days_to_get=DEFAULT_DAYS_TO_GET,
                              max_photos_per_day=DEFAULT_IMAGES_PER_DAY):
        dates = self._get_last_dates(days_to_get)

        all_photos = {}

        for day in dates:
            url = self._make_url(day, rover)

            resp = await self._http_getter.get(url)

            day_photos = resp.get('photos', [])
            extract_img_src = lambda photo_data: photo_data.get("img_src", "")

            # get just the img_src of each photo - and get only max_photos_per_day first photos
            day_photo_urls = list(map(extract_img_src, day_photos))[:max_photos_per_day]

            all_photos[day] = day_photo_urls

        return all_photos

    def _make_url(self, day, rover):
        date_param = {"earth_date": day}
        params = urlencode(self._fixed_params | date_param)
        url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos?{params}"
        return url




