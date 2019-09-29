import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import griddata

filename = "kaggle_income.csv"

df = pd.read_csv(filename, encoding = "latin-1")

longitudes  = df.Lon#[:10]
latitudes   = df.Lat#[:10]
mean_income = df.Mean#[:10]

da = 1

longitude_bins = np.arange(np.floor(longitudes.min()), np.ceil(longitudes.max()) + da, da)
latitude_bins  = np.arange(np.floor(latitudes.min()),  np.ceil(latitudes.max())  + da, da)
bins           = (longitude_bins, latitude_bins)

print(bins[0].shape, bins[1].shape)
#
binned_means  = np.histogram2d(longitudes, latitudes, bins = bins, weights = mean_income)[0]
binned_means /= np.histogram2d(longitudes, latitudes, bins = bins)[0]

binned_means = binned_means.flatten()
longitude_bins2 = np.repeat(longitude_bins, binned_means // longitude_bins.size)
latitude_bins2 = np.repeat(latitude_bins, binned_means // latitude_bins.size)

print(binned_means.shape, latitude_bins2.shape, longitude_bins2.shape)

mask = binned_means != np.nan

binned_means = binned_means[mask]
longitude_bins2 = longitude_bins2[mask]
latitude_bins2 = latitude_bins2[mask]

x, y = np.meshgrid(np.linspace(np.floor(longitudes.min()), np.ceil(longitudes.max()), 1000), np.linspace(np.floor(latitudes.min()),  np.ceil(latitudes.max()), 1000))

f = griddata((longitude_bins, latitude_bins), binned_means, (x, y))

fig, ax = plt.subplots(subplot_kw = {"projection" : ccrs.PlateCarree()})

plt.pcolormesh(x, y, f, transform = ccrs.PlateCarree())
#
#print(x)
#
ax.coastlines()
#
plt.show()




