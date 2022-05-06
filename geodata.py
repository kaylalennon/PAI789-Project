#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 10:41:06 2022

@author: kaylalennon
"""

import pandas as pd 
import geopandas as gpd
import matplotlib.pyplot as plt 
import matplotlib
import cartopy
import cartopy.crs as ccrs
import shapely.geometry as sgeom

# Importing the necessary modules for utilizing our geodataframe and our advanced plots
#%%

pregeo = pd.read_csv("merged.csv")

pregeo = pregeo.iloc[: , 1:]

states = gpd.read_file("cb_2019_us_state_500k.zip")

states = states.set_index('STUSPS',drop=False)

not_state = ['AS','GU','MP','PR','VI']

states = states.drop(not_state)

states = states.set_index('GEOID',drop=False)

print(states.columns)

states = states.drop(columns={'STATEFP', 'STATENS', 'STUSPS'})

states.to_csv("states.csv")

# Reading the csv of our abortion ranked data and the social indicators, getting 
# rid of the empty first column that is there when the CSV is read, reading a 
# shapfile that contains the projection of the USA we will use, dropping the 
# areas included that are not states, setting the index to the GEOID, checking
# the drop, dropping the columns of data that we do not need, saving to CSV
# for future use (optional)

#%%

geodata = states.merge(pregeo,on='NAME',how='left',validate='1:1',indicator=True)

geodata = geodata.sort_values(by="RANK")

# Merging the aboriton and social indicator data onto the 

#%%

fig, ax2 = plt.subplots(dpi=300)

geodata.plot('NAME',cmap='Dark2',ax=ax2)

fig.tight_layout()

fig.savefig("initial_map.png")


# Setting up a plot with the geodata to try the projection
# This cell is unecessary and just was my first attempt at a base map

#%%

def add_insetmap(axes_extent, map_extent, state_name, facecolor, edgecolor, geometry):

    use_projection = ccrs.Mercator()      
    geodetic = ccrs.Geodetic(globe=ccrs.Globe(datum='WGS84'))
    sub_ax = plt.axes(axes_extent, projection=use_projection) 
    sub_ax.set_extent(map_extent, geodetic) 

    sub_ax.add_feature(cartopy.feature.LAND)
    sub_ax.coastlines()
    sub_ax.set_title(state_name)

    sub_ax.add_geometries([geometry], ccrs.PlateCarree(), \
                          facecolor=facecolor, edgecolor=edgecolor, lw=0.3)
  
    extent_box = sgeom.box(map_extent[0], map_extent[2], map_extent[1], map_extent[3])
    sub_ax.add_geometries([extent_box], ccrs.PlateCarree(), color='none')

# Defining a function to inset the maps, choosing the map projection, setting the
# axes to our projection, setting the extent to the geodetic projection set earlier. 

# Adding land polygons, coastlines, and setting the axis title, adding the geometry
# map with the same projection and setting colors and size.
# Creating a box around the inset map with the size color and projection


lower = geodata[~geodata['NAME'].isin(["Alaska", "Hawaii"])]
lower.crs = {'init': 'epsg:4326'}
lower = lower.to_crs(epsg=2163)

akhi = geodata[geodata['NAME'].isin(["Alaska", "Hawaii"])] 

# Pulling the groups of states we want to plot seperately (contiguous and AK,HI),
# setting the contiguous to the the map projection

#%%
my_colormap = matplotlib.cm.PuBuGn
edgecolor = "gray"

ax2 = lower.plot(column="PERCENT NOT ACCESS", legend=False, 
                    cmap=matplotlib.cm.PuBuGn, ec=edgecolor, lw=0.4)

fig = ax2.get_figure()
cax = fig.add_axes([0.9, .25, 0.02, 0.5]) 
sm = plt.cm.ScalarMappable(cmap=my_colormap, 
        norm=plt.Normalize(vmin=min(geodata["PERCENT NOT ACCESS"]),vmax=max(geodata["PERCENT NOT ACCESS"])))

sm._A = []
cb = fig.colorbar(sm, cax=cax)

ax2.set_frame_on(False)
ax2.set_xticks([])
ax2.set_yticks([])
ax2.set_xticklabels([])
ax2.set_yticklabels([])
ax2.set_title("Percent of Women Aged 15-44 who Cannot Access an Abortion")

# Setting the colors, plotting the contiguous map as normal, setting the colorbar/legend,
# clearing the array of the scalar mappable, changing the axis settings
#%%
for index,state in akhi.iterrows():

    if state['NAME'] in ("Alaska", "Hawaii"):
        st_name = state['NAME']
        facecolor = my_colormap( state["PERCENT NOT ACCESS"] / max(geodata["PERCENT NOT ACCESS"] ))

        if st_name == "Alaska":
            map_extent = (-178, -135, 46, 73)
            axes_extent = (0.04, 0.06, 0.29, 0.275) 

        if st_name == "Hawaii":
            map_extent = (-162, -152, 15, 25)
            axes_extent = (0.27, 0.06, 0.15, 0.15)

        add_insetmap(axes_extent, map_extent, st_name, \
                     facecolor, \
                     edgecolor, \
                     state["geometry"])
plt.show()

fig.savefig("AborPct.png", dpi=300)

# Ploting AKHI as inset using a loop, setting the fill color according to our input 
# geodata, setting the size of the map and axes according the the state, adding the maps and plotting and saving