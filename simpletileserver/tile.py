from cStringIO import StringIO

from util import get_tile_corners


class Tile():
    def __init__(self, z, x, y):
        self.corners = get_tile_corners(z, x, y)

    def render(self):
        mem_png = StringIO()
        self.image.save(mem_png, 'png')

        return mem_png.getvalue()
