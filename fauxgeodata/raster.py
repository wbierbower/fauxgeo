
import tempfile


class Raster(object):
    # any global variables here

    def __init__(self, uri):
        self.uri = uri
        self.bands = []
        self.width = None
        self.height = None
        self.crs = None
        self.affine = None
        self.count = None
        self.nodata = None

        # if url and exists: initialize values

        # if no url, make tmp url

        # if url and does not yet exist, make it exist?

    def read():
        pass

    def read_band(num):
        pass

    def write_band(num, array):
        pass

    def _get_nodata():
        pass

    def _get_geotransform():
        pass

    def _update_metadata():
        pass

    def __str__(self):
        return "raster at %s" % (self.uri)
