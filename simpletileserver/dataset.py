import gdal
import numpy as np
import osr
from PIL import Image
from shapely.geometry import Polygon

from tile import Tile
from util import get_mercator_projection, corner_to_extent


class Dataset(object):
    def __init__(self, file_path, resampling_method, memory):
        self.file_path = file_path
        self.resampling_method = resampling_method
        self.memory = memory
        self.dataset = gdal.Open(file_path)
        self.cols = self.dataset.RasterXSize
        self.rows = self.dataset.RasterYSize
        self.number_of_bands = self.dataset.RasterCount
        self.extent = self.get_mercator_extent()

    def get_corners(self):
        xmin, xres, xskew, ymax, yskew, yres  = self.dataset.GetGeoTransform()
        xmax = xmin + (self.cols * xres)
        ymin = ymax + (self.rows * yres)

        return xmin, ymin, xmax, ymax

    def get_source_projection(self):
        srs = osr.SpatialReference()
        file_srs = self.dataset.GetProjection()
        srs.ImportFromWkt(file_srs)

        return srs

    def get_mercator_extent(self):
        source_srs = self.get_source_projection()
        target_srs = get_mercator_projection()
        transform = osr.CoordinateTransformation(source_srs, target_srs)
        xmin, ymin, xmax, ymax = self.get_corners()

        xmin, ymin, _ = transform.TransformPoint(xmin, ymin)
        xmax, ymax, _ = transform.TransformPoint(xmax, ymax)

        return corner_to_extent((xmin, ymin, xmax, ymax))

    def intersects_with_tile(self, tile):
        dataset_polygon = Polygon(self.extent)
        tile_polygon = Polygon(corner_to_extent(tile.corners))

        return dataset_polygon.intersects(tile_polygon)

    def get_reprojected_tile(self, tile):
        source_srs = self.get_source_projection()
        target_srs = get_mercator_projection()
        warp_options = gdal.WarpOptions(srcSRS=source_srs,
                                        dstSRS=target_srs,
                                        format="MEM",
                                        warpMemoryLimit=self.memory,
                                        multithread=True,
                                        outputBounds=tile.corners,
                                        width=256,
                                        height=256,
                                        resampleAlg=self.resampling_method)
        tile = gdal.Warp("", self.file_path, options=warp_options)

        return tile

    def format_array(self, array):
        if np.issubdtype(array.dtype, np.integer):
            array *= 255 / array.max()
        else:
            array *= 255.0 / array.max()

        if self.number_of_bands >= 3:
            rgb_bands = array[:3]
            return rgb_bands.transpose(1, 2, 0).astype('uint8')
        else:
            return array.astype('uint8')

    
    def get_tile(self, z, x, y):
        tile = Tile(z, x, y)
        if self.intersects_with_tile(tile):
            reprojected_tile = self.get_reprojected_tile(tile)
            array = reprojected_tile.ReadAsArray()
            formatted_array = self.format_array(array)
            image = Image.fromarray(formatted_array)
        else:
            image = Image.new('RGBA', (256, 256), (255, 0, 0, 0))

        tile.image = image

        return tile

