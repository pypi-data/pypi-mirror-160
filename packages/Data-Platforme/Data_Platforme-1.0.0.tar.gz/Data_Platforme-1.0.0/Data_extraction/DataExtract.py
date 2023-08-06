import pandas as pd
import ee
import geemap
import os
from osgeo import gdal
import  numpy as np
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt

def AuthenticateEE():
    ee.Initialize();

def get_s2_sr_cld_col(Type_data,aoi, start_date, end_date,CLOUD_FILTER):
    # Import and filter S2 SR.
    s2_sr_col = (ee.ImageCollection(Type_data)
        .filterBounds(aoi)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE', CLOUD_FILTER)))

    # Import and filter s2cloudless.
    s2_cloudless_col = (ee.ImageCollection('COPERNICUS/S2_CLOUD_PROBABILITY')
        .filterBounds(aoi)
        .filterDate(start_date, end_date))

    # Join the filtered s2cloudless collection to the SR collection by the 'system:index' property.
    return ee.ImageCollection(ee.Join.saveFirst('s2cloudless').apply(**{
        'primary': s2_sr_col,
        'secondary': s2_cloudless_col,
        'condition': ee.Filter.equals(**{
            'leftField': 'system:index',
            'rightField': 'system:index'
        })
    }))

def list_images(image_collection):
    """
    Get the list of images from an image collection
    """

    size_image_collection = image_collection.size().getInfo()
    list_img = [ee.Image(image_collection.toList(size_image_collection).get(i)) for i in range(size_image_collection)]

    return(list_img)

def Extract_Data(type_data,aoi, start_date, end_date,CLOUD_FILTER):
    out_dir = os.path.join(path= "C:\\images")
    collectionImages= get_s2_sr_cld_col(type_data,aoi,start_date,end_date,CLOUD_FILTER)
    listimages = list_images(collectionImages)
    for image in listimages:

        filename = os.path.join(out_dir, 'image'+ str(listimages.index(image))+'.tif')
        images = geemap.ee_export_image(image, filename=filename ,scale=90, region=aoi,)
    return images


def readImage():
    gdal.UseExceptions()
    dataset = gdal.Open('image.tif')
    band = dataset.GetRasterBand(2)
    arr = band.ReadAsArray()
    plt.imshow(arr)
    return arr


