#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 11:21:13 2022

@author: kaylalennon
"""

import pandas as pd

#%%

rank_numbers = pd.DataFrame(range(1,52))

rank_numbers.index = rank_numbers.index + 1
                                   
state_rank = pd.read_csv("abortion_access_2019.csv")

state_rank = state_rank.sort_values("PERCENT")

state_rank = state_rank.rename(columns={"PERCENT":"PERCENT NOT ACCESS"})

state_rank.index = rank_numbers.index

state_rank.index = state_rank.index.rename('RANK')

state_rank.to_csv("state_rank.csv")


