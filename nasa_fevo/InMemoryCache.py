from typing import Dict, Union
from nasa_fevo.Cache import Cache
from datetime import datetime


# very simple in-memory cache
# meant for small # of items
class InMemoryCache(Cache):
    def __init__(self):
        self.store: Dict[str, object] = {}

    def get(self, key: str) -> Union[object, None]:
        val_exp = self.store.get(key, None)
        if val_exp is None:
            return None
        else:
            return val_exp[0]

    def put(self, key: str, value: object, expiration: datetime) -> None:
        if value is None:
            raise ValueError("Value mustn't be None")
        self.store[key] = (value, expiration)
        self.purge_expired()

    def purge_expired(self) -> None:
        keys_to_delete = []

        now = datetime.now()
        for item in self.store.items():
            key = item[0]
            # value = item[1][0]
            expiration = item[1][1]
            if expiration < now:
                print(f"key={key}, now={now} > exp={expiration}")
                keys_to_delete.append(key)

        for key in keys_to_delete:
            del self.store[key]

    def clear(self, key: str):
        if key in self.store:
            del self.store[key]