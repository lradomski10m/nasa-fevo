from flask import Flask
from flask import request
from nasa_fevo.RoverImagesRetrieverWithCache import RoverImagesRetrieverWithCache
from nasa_fevo.RoverImagesRetriever import DEFAULT_ROVER, DEFAULT_IMAGES_PER_DAY, DEFAULT_DAYS_TO_GET
from nasa_fevo.InMemoryCache import InMemoryCache

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    cache = InMemoryCache()
    retriever = RoverImagesRetrieverWithCache(cache)

    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)

    # # ensure the instance folder exists
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    # a simple page that says hello
    @app.route('/')
    async def index():
        return 'NASA Curiosity Rover image fetcher'

    @app.route('/get_photos')
    async def get_photos():
        rover = request.args.get('rover', DEFAULT_ROVER)
        days = int(request.args.get('days', DEFAULT_DAYS_TO_GET))
        imgs_per_day = int(request.args.get('imgs-per-day', DEFAULT_IMAGES_PER_DAY))
        resp = await retriever.get_rover_images(rover=rover, days_to_get=days, max_photos_per_day=imgs_per_day)
        return resp

    return app
