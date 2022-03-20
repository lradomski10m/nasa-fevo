from typing import Dict, Union
from datetime import datetime


class Cache():
    def get(self, key: str) -> Union[object, None]:
        pass

    def put(self, key: str, value: object, expiration: Union[datetime, None]) -> None:
        pass

    def clear(self, key: str):
        pass
