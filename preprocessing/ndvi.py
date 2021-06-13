import rasterio
import warnings
import numpy as np


def get_ndvi(red, nir):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ndvi=np.where((nir+red)==0., 0, (nir-red)/(nir+red))

    return ndvi