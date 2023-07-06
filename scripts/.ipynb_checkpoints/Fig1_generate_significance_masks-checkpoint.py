#!/usr/bin/env python
# coding: utf-8

# THIS PYTHON SCRIPT READS VARIOUS MODEL OUTPUTS 
# (here: 100yrs seasonal means ECHAM6 atmosphere outputs at T63 resolution).
# AT EACH GRID POINT THE SIGNIFICANCE OF MULTIYEAR ANOMALIES RELATIVE TO A 
# REFERENCE IS COMPUTED BASED ON A T-TEST. AT EACH POINT THE RESULT IS 0 IF 
# THE SEASONAL MEAN OF THE TIME SERIES DIFFERS SIGNIFICANTLY FROM THE REFERENCE
# WITH 95% CONFIDENCE LEVEL
# RESPECTIVE SIGNIFICANCE MASKS ARE SAVED IN NETCDF FORMAT
# Based on code Created on Tue Nov 26 07:15:23 2019
# 
# @author: Christian Stepanek
# 

# In[2]:
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import xarray as xr
from cartopy.util import add_cyclic_point
import matplotlib.colors as colors
import os as os
import scipy.stats
import matplotlib as mpl
from netCDF4 import Dataset

path='../data/'
def load_ym(path,pattern):
    return xr.open_mfdataset(path+pattern, decode_times=False)
tempPL_dsJJA   = Dataset(path+'ALLplake_temp2_JJA_2250_2349.nc')
tempPL_dsDJF   = Dataset(path+'ALLplake_temp2_DJF_2250_2349.nc')
precipPL_ds = Dataset(path+'ALLplake_precip_ym_2250_2349.nc')
tempAL_dsDJF   = Dataset(path+'ALLalake13ka_temp2_DJF_2250_2349.nc')
tempAL_dsJJA   = Dataset(path+'ALLalake13ka_temp2_JJA_2250_2349.nc')
precipAL_ds = Dataset(path+'ALLalake13ka_precip_ym_2250_2349.nc')
tempREF_dsDJF   = Dataset(path+'ALLalakeGLAC_temp2_DJF_2250_2349.nc')
tempREF_dsJJA   = Dataset(path+'ALLalakeGLAC_temp2_JJA_2250_2349.nc')
precipREF_ds = Dataset(path+'ALLalakeGLAC_precip_ym_2250_2349.nc')
t_ref_dataJJA=tempREF_dsJJA.variables['temp2'][:].squeeze()
t_ref_dataDJF=tempREF_dsDJF.variables['temp2'][:].squeeze()
t_exp1_dataJJA=tempPL_dsJJA.variables['temp2'][:].squeeze()
t_exp1_dataDJF=tempPL_dsDJF.variables['temp2'][:].squeeze()
t_exp2_dataJJA=tempAL_dsJJA.variables['temp2'][:].squeeze()
t_exp2_dataDJF=tempAL_dsDJF.variables['temp2'][:].squeeze()
p_ref_data=precipREF_ds.variables['precip'][:].squeeze()
p_exp1_data=precipPL_ds.variables['precip'][:].squeeze()
p_exp2_data=precipAL_ds.variables['precip'][:].squeeze()

lon=tempREF_dsJJA.variables['lon'][:]
lat=tempREF_dsJJA.variables['lat'][:]

lons,lats=np.meshgrid(lon,lat)
#%%define auxiliary functions that are employed for significance testing
#functions and procedure taken over from Paul Gierz
def estimated_autocorrelation(x):
    n=len(x)
    variance=x.var()
    x=x-x.mean()
    r=np.correlate(x, x, mode='full')[-n:]
    result=r/(variance*(np.arange(n,0,-1)))
    return result

def compute_significance(experiment,reference,lons,lats,mask_cutoff,verbose=False):
    sig_mask=np.zeros((len(lats),len(lons)))
    sig_mask[:]=np.nan
    n_time=experiment.shape[0]
    for i in range(len(lons)):
        for j in range(len(lats)):
            xx=experiment[:, j, i]
            yy=reference[:, j, i]
            #breakpoint()
            autocorrx=max(estimated_autocorrelation(xx)[1], 0)
            autocorry=max(estimated_autocorrelation(yy)[1], 0)
            eff_dof1=n_time * (1 - autocorrx) / (1 + autocorrx)
            eff_dof2=n_time * (1 - autocorry) / (1 + autocorry)
            eff_dof_comb = min(eff_dof1, eff_dof2)
            cutoff=scipy.stats.t.ppf(mask_cutoff, eff_dof_comb)
            t_test = abs(xx.mean()-yy.mean())/((xx.var()/n_time+yy.var()/n_time)**0.5)
            if t_test<cutoff:
                sig_mask[j,i]=1
            else:
                sig_mask[j,i]=0
            if verbose:
                print(cutoff, t_test)
                print(t_test < cutoff)
    return sig_mask
ppmask=compute_significance(p_exp1_data,p_ref_data,lon,lat,.95)
tempmaskJJA=compute_significance(t_exp1_dataJJA,t_ref_dataJJA,lon,lat,.95)
tempmaskDJF=compute_significance(t_exp1_dataDJF,t_ref_dataDJF,lon,lat,.95)
tmaskJJA=np.ma.masked_not_equal(tempmaskJJA, 0)
tmaskDJF=np.ma.masked_not_equal(tempmaskDJF, 0)
pmask=np.ma.masked_not_equal(ppmask, 0)

#print(pmask)
#np.savetxt('PLpp_mask.txt', pmask)
#np.savetxt('PLtemp_mask.txt', tmask)
xr.Dataset({'prcip_mask': (["x", "y"], pmask),'temp_maskDJF': (["x", "y"], tmaskDJF),'temp_maskJJA': (["x", "y"], tmaskJJA)},
    coords={
        "lon": (["x", "y"], lons),
        "lat": (["x", "y"], lats),}).to_netcdf('../data/PL_SigMaskSM.nc')


ppmask=compute_significance(p_exp2_data,p_ref_data,lon,lat,.95)
tempmaskJJA=compute_significance(t_exp2_dataJJA,t_ref_dataJJA,lon,lat,.95)
tempmaskDJF=compute_significance(t_exp2_dataDJF,t_ref_dataDJF,lon,lat,.95)
tmaskJJA=np.ma.masked_not_equal(tempmaskJJA, 0)
tmaskDJF=np.ma.masked_not_equal(tempmaskDJF, 0)
pmask=np.ma.masked_not_equal(ppmask, 0)
xr.Dataset({'prcip_mask': (["x", "y"], pmask),'temp_maskJJA': (["x", "y"], tmaskJJA),'temp_maskDJF': (["x", "y"], tmaskDJF)},
    coords={
        "lon": (["x", "y"], lons),
        "lat": (["x", "y"], lats),}).to_netcdf('../data/AL_SigMaskSM.nc')
