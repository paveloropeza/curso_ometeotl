#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WRF variables
"""
import netCDF4 as nc
import numpy as np

WRF_file = "/LUSTRE/cursos/2025/semestre2/seminarioiv/p.8510/WRFV4/WRF/wrfout_d02_2022-06-12_00.nc"
ds = nc.Dataset(WRF_file, 'r')

print(WRF_file)

print(ds.variables.keys())
# Radiacion de onda corta que llega a superficie
swdown = ds.variables['SWDOWN']
print(swdown[:])
# Valor maximo para las 3 primeras horas 
max_value = np.max(swdown[:])
print(max_value)
ds.close()

