from flask import Flask
from gunicorn.app.base import BaseApplication
from gunicorn.six import iteritems
from gunicorn.util import import_app


application = Flask(__name__)

@application.route('/tiles/<int:z>/<int:x>/<int:y>.png')
def serve_tiles(z, x, y):
    tile = TileServer.dataset.get_tile(z, x, y)
    return tile.render()


class TileServer(BaseApplication):

    def __init__(self, options=None):
        self.options = options or {}
        self.application = application
        super(TileServer, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return application
