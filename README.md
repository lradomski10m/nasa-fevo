# FEVO NASA challenge

## Setup instructions
- git clone this repo
- install python 3.9
- pip install -r requirements.txt
- export FLASK_APP=nasa_fevo
- flask run

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
- not unit test du to lack of time