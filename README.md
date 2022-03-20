# FEVO NASA challenge

## Setup instructions
- git clone this repo
- install python 3.9
- python -m venv ./venv
- source ./venv/bin/activate
- pip install -r requirements.txt
- python -m pytest --asyncio-mode=strict 

## Running instructions
- python main.py
(this will start the web server locally)

## Testing instructions
While the web server is running locally execute:
- curl http://127.0.0.1:5000/get_photos

The following variations are also supported
- curl http://127.0.0.1:5000/get_photos\?days=5\&imgs-per-day=10

(characters ? and & need to be escaped in bash/zsh - \? or /&)

(Or type the http:// url as-is in the browser, e.g:
http://127.0.0.1:5000/get_photos?days=5&imgs-per-day=10)


## Notes
- basic in-memory caching implemented (can easily be replaced with other type of caching)
- not unit test due to lack of time
- some shortcuts taken (e.g. use of requests-async instead of aiohttp)
