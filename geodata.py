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

#%%

geodata = states.merge(pregeo,on='NAME',how='left',validate='1:1',indicator=True)

geodata = geodata.sort_values(by="RANK")

#%%

fig, ax2 = plt.subplots(dpi=300)

geodata.plot('NAME',cmap='Dark2',ax=ax2)

fig.tight_layout()

fig.savefig("initial_map.png")

#%%

def add_insetmap(axes_extent, map_extent, state_name, facecolor, edgecolor, geometry):
    # create new axes, set its projection
    use_projection = ccrs.Mercator()      # preserves shape
    #use_projection = ccrs.PlateCarree()  # large distortion in E-W, bad for for Alaska
    geodetic = ccrs.Geodetic(globe=ccrs.Globe(datum='WGS84'))
    sub_ax = plt.axes(axes_extent, projection=use_projection)  # normal units
    sub_ax.set_extent(map_extent, geodetic)  # map extents

    # option to add basic land, coastlines of the map
    # can comment out if you don't need them
    sub_ax.add_feature(cartopy.feature.LAND)
    sub_ax.coastlines()
    sub_ax.set_title(state_name)

    # add map `geometry`
    sub_ax.add_geometries([geometry], ccrs.PlateCarree(), \
                          facecolor=facecolor, edgecolor=edgecolor, lw=0.3)
    # +++ more features can be added here +++
    # plot box around the map
    extent_box = sgeom.box(map_extent[0], map_extent[2], map_extent[1], map_extent[3])
    sub_ax.add_geometries([extent_box], ccrs.PlateCarree(), color='none')



# extract parts of the whole 'newusa' geodataframe for separate plotting/manipulation
# 'usa_main': excluding non-conterminous states
usa_main = geodata[~geodata['NAME'].isin(["Alaska", "Hawaii"])] # exclude these
#  re-project usa_main to equal-area conic projection "EPSG:2163"
usa_main.crs = {'init': 'epsg:4326'}
usa_main = usa_main.to_crs(epsg=2163)

# 'usa_more': non-conterminous states, namely, Alaska and Hawaii
usa_more = geodata[geodata['NAME'].isin(["Alaska", "Hawaii"])]  # include these

#%%
# ------------ Plot --------------
# plot 1st part, using usa_main and grab its axis as 'ax2'

my_colormap = matplotlib.cm.PuBuGn

# some settings
edgecolor = "gray"

ax2 = usa_main.plot(column="PERCENT NOT ACCESS", legend=False, 
                    cmap=matplotlib.cm.PuBuGn, ec=edgecolor, lw=0.4)

# manipulate colorbar/legend
fig = ax2.get_figure()
cax = fig.add_axes([0.9, .25, 0.02, 0.5])  #[left,bottom,width,height]
sm = plt.cm.ScalarMappable(cmap=my_colormap, 
        norm=plt.Normalize(vmin=min(geodata["PERCENT NOT ACCESS"]),vmax=max(geodata["PERCENT NOT ACCESS"])))

# clear the array of the scalar mappable
sm._A = []
cb = fig.colorbar(sm, cax=cax)

# manipulate the axis seetings
ax2.set_frame_on(False)
ax2.set_xticks([])
ax2.set_yticks([])
ax2.set_xticklabels([])
ax2.set_yticklabels([])
ax2.set_title("Percent of Women Aged 15-44 who Cannot Access an Abortion")

#%%
# add more features on ax2
# plot Alaska, Hawaii as inset maps
for index,state in usa_more.iterrows():

    if state['NAME'] in ("Alaska", "Hawaii"):
        st_name = state['NAME']

        # set fill color, using normalized `sclass` on `my_colormap`
        facecolor = my_colormap( state["PERCENT NOT ACCESS"] / max(geodata["PERCENT NOT ACCESS"] ))

        if st_name == "Alaska":
            # (1) Alaska
            # Custom extent, relative size
            map_extent = (-178, -135, 46, 73)    # degrees: (lonmin,lonmax,latmin,latmax)
            axes_extent = (0.04, 0.06, 0.29, 0.275) # axes units: 0 to 1, (LLx,LLy,width,height)

        if st_name == "Hawaii":
            # (2) Hawaii
            # Custom extent, relative size
            map_extent = (-162, -152, 15, 25)
            axes_extent = (0.27, 0.06, 0.15, 0.15)

        # add inset maps
        add_insetmap(axes_extent, map_extent, st_name, \
                     facecolor, \
                     edgecolor, \
                     state["geometry"])

plt.show()

fig.savefig("AborPct.png", dpi=300)