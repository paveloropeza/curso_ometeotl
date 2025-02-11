#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Read WRF variables
"""
import netCDF4 as nc
import numpy as np

WRF_file = "/LUSTRE/ID/hidromet/WRF/Salidas_WRF_mayo_2022/wrfout_d02_2022-05-02_00.nc"
ds = nc.Dataset(WRF_file, 'r')

print(WRF_file)

print(ds.variables.keys())
swdown = ds.variables['SWDOWN']
print(swdown[:])
max_value = np.max(swdown[:])
print(max_value)
ds.close()

