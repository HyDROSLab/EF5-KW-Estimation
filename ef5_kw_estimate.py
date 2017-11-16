#!/usr/bin/env python
from sklearn import linear_model
from sklearn import preprocessing
import pandas as pd
import numpy as np
import osgeo.osr as osr
import osgeo.gdal as gdal
from osgeo.gdalconst import *
import pickle

gt = None
proj = None
mask = None
nx = 0
ny = 0

def ReadGrid(gridIn, keepInfo=False):
        global gt, proj, mask, nx, ny
        dem = gdal.Open(gridIn, GA_ReadOnly)
        data_dem = dem.ReadAsArray()
        data_dem1 = data_dem.flatten()
        if keepInfo:
                gt = dem.GetGeoTransform()
                proj = dem.GetProjection()
                mask = np.where((data_dem1 < -9000.0))
                mask = mask[0]
                nx = dem.GetRasterBand(1).XSize
                ny = dem.GetRasterBand(1).YSize
        data_dem1 = np.ma.masked_array(data_dem1, data_dem1 < -9000.0)
        return data_dem1

def WriteGrid(gridOutName, dataOut):
        driver = gdal.GetDriverByName('GTiff')
        dst_ds = driver.Create(gridOutName, nx, ny, 1, gdal.GDT_Float32)
        dst_ds.SetGeoTransform(gt)
        dst_ds.SetProjection(proj)
        dataOut[mask] = -9999.0
        dataOut.shape = (-1, nx)
        dst_ds.GetRasterBand(1).WriteArray(dataOut, 0, 0)
        dst_ds.GetRasterBand(1).SetNoDataValue(-9999.0)
        dst_ds = None
