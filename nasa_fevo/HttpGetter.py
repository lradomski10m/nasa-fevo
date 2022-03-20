import requests


class HttpGetter():
    def __init__(self):
        pass

    async def get(self, url: str) -> object:
        resp = requests.get(url).json()
        return resp
