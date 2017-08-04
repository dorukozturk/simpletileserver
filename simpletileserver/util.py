import math
import osr

# Earth circumference for web mercator
circumference = 20037508.342789244

def get_pixel_size(zoom):
    """Returns an approximate pixel size for a given zoom level"""

    equator_latitude = 0
    # For simplification we assume everything is equator latitude
    pixel_size = circumference * math.cos(equator_latitude) / 2 ** (zoom + 7)

    return pixel_size


def get_tile_corners(z, x, y, tile_size=256):
    """Returns bounds of a tile for a given x,y,z index"""

    number_of_tiles = 2.0 ** (z * 2)
    pixel_size = get_pixel_size(z)
    xmin = x / number_of_tiles * (circumference * 2 ** (z + 1)) - circumference
    ymin = y / number_of_tiles * (circumference * 2 ** (z + 1)) - circumference
    xmax = xmin + pixel_size * tile_size
    ymax = ymin + pixel_size * tile_size

    return xmin, ymin, xmax, ymax

def get_mercator_projection():
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(3857)

    return srs

def corner_to_extent(corners):
    """Corners are in xmin, ymin, xmax, ymax order"""
    

    extent = [[corners[0], corners[1]],
              [corners[2], corners[1]],
              [corners[2], corners[3]],
              [corners[0], corners[3]],
              [corners[0], corners[1]]]

    return extent

def get_maximum_zoom_level(pixel_size):
    for i in range(1,30):
        mercator_pixel_size = get_pixel_size(i)
        if mercator_pixel_size <= pixel_size:
            max_zoom = i + 1
            break

    return max_zoom
