#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 11:21:13 2022

@author: kaylalennon
"""

import pandas as pd
import matplotlib.pyplot as plt 

# Importing the modules we need 

#%%

rank_numbers = pd.DataFrame(range(1,52))

rank_numbers.index = rank_numbers.index + 1
                                   
state_rank = pd.read_csv("abortion_access_2019.csv")

state_rank = state_rank.sort_values("PERCENT")

state_rank = state_rank.rename(columns={"PERCENT":"PERCENT NOT ACCESS"})

state_rank.index = rank_numbers.index

state_rank.index = state_rank.index.rename('RANK')

state_rank.to_csv("state_rank.csv")

# Creating a dataframe that lists numbers 1-51, setting the index to start with 
# 1 instead of zero for clarity in discussing state access ranks, reading in the
# abortion data CSV (input file), sorting that dataframe by the percent not access 
# and renaming the column for clarity, changing the state rank dataframe to have
# the same index as the rank numbers dataframe and renaming the index rank
# saving to CSV for future analysis

#%%

state_rank.iloc[ 0:10 ].plot.bar()
plt.show()
plt.savefig("first10.png", dpi=300)

state_rank.iloc[ -10: ].plot.bar()
plt.show()
plt.savefig("last10.png", dpi=300)

state_rank.plot.bar()
plt.show()
plt.savefig("barchart.png")

# These are just some initial plots of the data before adding the geospatial data,
# which aren't very good visualizations of the data, but do show the values 
# of the 10 best and 10 worst states for abortion access