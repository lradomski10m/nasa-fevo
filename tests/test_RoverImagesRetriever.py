import unittest
from unittest.mock import MagicMock, patch, AsyncMock
from datetime import date, datetime
from nasa_fevo.RoverImagesRetriever import RoverImagesRetriever, DEFAULT_ROVER

from test_data import TEST_RESP, FIRST_PHOTO_URL


class RoverImagesRetrieverTest(unittest.IsolatedAsyncioTestCase):
    async def test_last_days(self):
        self.maxDiff = None
        getter = MagicMock()
        rir = RoverImagesRetriever(getter)

        with patch("nasa_fevo.RoverImagesRetriever.date") as date:
            date.today.return_value = datetime(2022, 3, 19)
            dates = rir._get_last_dates(10)
            date.today.assert_called_once()
            self.assertEqual(len(dates), 10)
            self.assertEqual(dates[0], "2022-03-18")
            self.assertEqual(dates[9], "2022-03-09")

    async def test_get(self):
        self.maxDiff = None
        getter = AsyncMock()
        rir = RoverImagesRetriever(getter)

        with patch("nasa_fevo.RoverImagesRetriever.date") as date:
            date.today.return_value = datetime(2022, 3, 19)
            getter.get.return_value = TEST_RESP

            resp = await rir.get_rover_images(rover=DEFAULT_ROVER, days_to_get=2, max_photos_per_day=1)
            date.today.assert_called_once()
            getter.get.assert_awaited()

            self.assertIn("2022-03-18", resp)
            self.assertEqual(len(resp["2022-03-18"]), 1)
            self.assertEqual(resp["2022-03-18"][0], FIRST_PHOTO_URL)
            self.assertIn("2022-03-17", resp)
            self.assertEqual(len(resp["2022-03-17"]), 1)
            self.assertEqual(resp["2022-03-17"][0], FIRST_PHOTO_URL)


if __name__ == '__main__':
    unittest.main()
