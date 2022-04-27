#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 14:48:07 2022

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

usa_main = geodata[~geodata['NAME'].isin(["Alaska", "Hawaii"])] 

usa_main.crs = {'init': 'epsg:4326'}

usa_main = usa_main.to_crs(epsg=2163)


usa_more = geodata[geodata['NAME'].isin(["Alaska", "Hawaii"])] 

#%%

my_colormap = matplotlib.cm.pink

edgecolor = "gray"

ax2 = usa_main.plot(column="Median Household Income of Families with <18", legend=False, 
                    cmap=matplotlib.cm.pink, ec=edgecolor, lw=0.4)

fig = ax2.get_figure()
cax = fig.add_axes([0.9, .25, 0.02, 0.5]) 
sm = plt.cm.ScalarMappable(cmap=my_colormap, 
        norm=plt.Normalize(vmin=min(geodata["Median Household Income of Families with <18"]),vmax=max(geodata["Median Household Income of Families with <18"])))

sm._A = []
cb = fig.colorbar(sm, cax=cax)

ax2.set_frame_on(False)
ax2.set_xticks([])
ax2.set_yticks([])
ax2.set_xticklabels([])
ax2.set_yticklabels([])
ax2.set_title("Median Household Income of Families with Kids Younger than 18")

#%%

for index,state in usa_more.iterrows():

    if state['NAME'] in ("Alaska", "Hawaii"):
        st_name = state['NAME']
        facecolor = my_colormap( state["Median Household Income of Families with <18"] / max(geodata["Median Household Income of Families with <18"] ))

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

fig.savefig("MedInc18.png", dpi=300)