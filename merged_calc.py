#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 08:53:53 2022

@author: kaylalennon
"""

import pandas as pd 

#%%

merged = pd.read_csv("merge.csv")

merged = merged.iloc[: , 1:]

merged['No Diploma Pct'] = (merged['18-24 Some HS, No Diploma'] / merged['Female Population Age 18-24']).round(2)

merged['Diploma Pct'] = (merged['18-24 HS Diploma/E'] / merged['Female Population Age 18-24']).round(2)

merged['Degree Pct'] = (merged['18-24 Bachelors Degree'] / merged['Female Population Age 18-24']).round(2)

merged['Upper Degree Pct'] = (merged['25-34 Bachelors Degree'] / merged['Population 25-34']).round(2)

#%%

merged['Male College'] = merged['Male Pop Enrolled in Public College'] + merged['Male Pop Enrolled in Private College']

merged['Male Enrollment Rate'] = (merged['Male College'] / merged['Male Population Age 15+']).round(2)

merged['Male College Ratio'] = (merged['Male College'] / merged['Male Pop Age 15+ not Enrolled in College']).round(2)

merged['Female College'] = merged['Female Pop Enrolled in Public College'] + merged['Female Pop Enrolled in Private College']

merged['Female Enrollment Rate'] = (merged['Female College'] / merged['Female Population Age 15+']).round(2)

merged['Female College Ratio'] = (merged['Female College'] / merged['Female Pop Age 15+ not Enrolled in College']).round(2)

merged.to_csv("merged.csv")

pregeo = pd.read_csv("merged.csv")