import requests_async as requests


class HttpGetter():
    def __init__(self):
        pass

    async def get(self, url: str) -> object:
        resp = await requests.get(url)
        return resp.json()
