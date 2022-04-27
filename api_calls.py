#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 13:15:20 2022

@author: kaylalennon
"""

import requests
import pandas as pd

pd.set_option('display.max_rows',None)

#%%

# Current College Enrollment By Gender

api = 'https://api.census.gov/data/2019/acs/acs5'

variables = ["NAME,B14004_001E,B14004_002E,B14004_003E,B14004_008E,B14004_013E,B14004_018E,B14004_019E,B14004_024E,B14004_029E"]

for_clause = 'state:*'

key_value = '06c10a6b3fcea07be8f8bfcbe0d0b1746cac5151'

payload = { 'get':variables, 'for':for_clause,'key':key_value }

response = requests.get(api,payload)

row_list = response.json()

colnames = row_list[0]

datarows = row_list[1:]

sex_by_college = pd.DataFrame(columns=colnames, data=datarows)

sex_by_college.set_index(["NAME"])

sex_by_college = sex_by_college.rename(columns={'B14004_001E':'Total Population Age 15+',
                                                'B14004_002E':'Male Population Age 15+',
                                                'B14004_003E':'Male Pop Enrolled in Public College',
                                                'B14004_008E':'Male Pop Enrolled in Private College',
                                                'B14004_013E':'Male Pop Age 15+ not Enrolled in College',
                                                'B14004_018E':'Female Population Age 15+',
                                                'B14004_019E':'Female Pop Enrolled in Public College',
                                                'B14004_024E':'Female Pop Enrolled in Private College',
                                                'B14004_029E':'Female Pop Age 15+ not Enrolled in College'})


sex_by_college = sex_by_college.drop(labels=[51], axis=0)

sex_by_college = sex_by_college.drop(columns='state')

sex_by_college.to_csv('sex_by_college.csv')


#%%

# Female Educational Attainment 

api = 'https://api.census.gov/data/2019/acs/acs5'

variables = ["NAME,B15001_043E,B15001_044E,B15001_046E,B15001_047E,B15001_050E,B15001_052E,B15001_058E"]

key_value = '06c10a6b3fcea07be8f8bfcbe0d0b1746cac5151'

for_clause = 'state:*'

payload = { 'get':variables, 'for':for_clause,'key':key_value }

response = requests.get(api,payload)

row_list = response.json()

colnames = row_list[0]

datarows = row_list[1:]

wo_edu_attain = pd.DataFrame(columns=colnames, data=datarows)

wo_edu_attain.set_index(["NAME"])

wo_edu_attain = wo_edu_attain.rename(columns={'B15001_043E':'Total Female Population',
                                              'B15001_044E':'Female Population Age 18-24',
                                              'B15001_046E':'18-24 Some HS, No Diploma',
                                              'B15001_047E':'18-24 HS Diploma/E',
                                              'B15001_050E':'18-24 Bachelors Degree',
                                              'B15001_052E':'Population 25-34',
                                              'B15001_058E':'25-34 Bachelors Degree'})

wo_edu_attain = wo_edu_attain.drop(labels=[51], axis=0)

wo_edu_attain = wo_edu_attain.drop(columns='state')

wo_edu_attain.to_csv('wo_edu_attain.csv')


#%%

# Median Income 

api = 'https://api.census.gov/data/2019/acs/acs5/subject'

variables = ["NAME,S1903_C03_002E,S1903_C03_019E,S1903_C03_020E"]

key_value = '06c10a6b3fcea07be8f8bfcbe0d0b1746cac5151'

for_clause = 'state:*'

payload = { 'get':variables, 'for':for_clause,'key':key_value }

response = requests.get(api,payload)

row_list = response.json()

colnames = row_list[0]

datarows = row_list[1:]

med_inc = pd.DataFrame(columns=colnames, data=datarows)

med_inc.set_index(["NAME"])

med_inc = med_inc.rename(columns={'S1903_C03_002E':'Median Household Income',
                                  'S1903_C03_019E':'Median Household Income of Families',
                                  'S1903_C03_020E':'Median Household Income of Families with <18'})

med_inc = med_inc.drop(labels=[51], axis=0)

med_inc = med_inc.drop(columns='state')

med_inc.to_csv('med_inc.csv')

#%%

# Poverty 

api = 'https://api.census.gov/data/2019/acs/acs5/subject'

variables = ["NAME,S1701_C03_001E,S1701_C03_003E"]

key_value = '06c10a6b3fcea07be8f8bfcbe0d0b1746cac5151'

for_clause = 'state:*'

payload = { 'get':variables, 'for':for_clause,'key':key_value }

response = requests.get(api,payload)

row_list = response.json()

colnames = row_list[0]

datarows = row_list[1:]

pov = pd.DataFrame(columns=colnames, data=datarows)

pov.set_index(["NAME"])

pov = pov.rename(columns={'S1701_C03_001E':'Total Population Below Poverty Line',
                          'S1701_C03_003E':'Population under 18 Years Below Poverty Line'})
                                
pov = pov.drop(labels=[51], axis=0)

pov = pov.drop(columns='state')

pov.to_csv('pov.csv')

#%%

# Population S0601

api = 'https://api.census.gov/data/2019/acs/acs5/subject'

variables = ["NAME,S0601_C01_001E"]

key_value = '06c10a6b3fcea07be8f8bfcbe0d0b1746cac5151'

for_clause = 'state:*'

payload = { 'get':variables, 'for':for_clause,'key':key_value }

response = requests.get(api,payload)

row_list = response.json()

colnames = row_list[0]

datarows = row_list[1:]

pop = pd.DataFrame(columns=colnames, data=datarows)

pop.set_index(["NAME"])

pop = pop.rename(columns={'S0601_C01_001E':'Total Population'})
                                
pop = pop.drop(labels=[51], axis=0)

pop = pop.drop(columns='state')

pop.to_csv('pop.csv')

#%%

state_rank = pd.read_csv("state_rank.csv")

merge = pd.merge(state_rank,pov, on='NAME', how='left')

merge = pd.merge(merge, med_inc, on='NAME', how='left')

merge = pd.merge(merge, wo_edu_attain, on='NAME', how='left')

merge = pd.merge(merge, sex_by_college, on='NAME', how='left')

merge = pd.merge(merge, pop, on='NAME', how='left')

merge.to_csv("merge.csv")
