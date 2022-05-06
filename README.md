# APA-Project-Kayla-Lennon
 
hey besties! 

we finna #code

this is a project for my advanced policy analysis class at the maxwell school of citizenship and public affairs taught by the fabulous and talented dr. pete wilcoxen! (check out his repositories here (https://github.com/pjwilcoxen)

this respository looks at comparing abortion rates with different social indexes to visually see any associations. the social indexes come from api calls so you can use the ones i have presented or choose your own variables with my api call examples

data inputs:

1. abortion_access_2019.csv
    verywell health analysis from 2021 shows the amount of women who do not have access to an abortion provider in the county they live in. because they do not have a csv of the information available i manually made a file from the graphic of this article from 2021 (https://www.verywellhealth.com/abortion-access-ranking-states-5202659) 

2. cb_2019_us_state_500k.zip
    this is a shapefile of parcel data from the census! in my script i get rid of a lot of variables from this file that i don't need but feel free to keep them!
    
3. social indicator data
    all of the social data comes from the census! the verywell health data uses the population estimates from the 5 year american community survey population estimates from 2019 so all of our the variables also come from that same 5 year acs estimate using api calls 

4. necessary downloads/systems
    geopandas - adds support to pandas for geospatial data - https://geopandas.org/en/stable/getting_started/install.html
    cartopy - adds support for making maps and other visuals using geospatial data - https://scitools.org.uk/cartopy/docs/latest/installing.html
    census api key - allows you to pull large amount of census data from census tables - https://api.census.gov/data/key_signup.html

sript running order:
    
1. state_rank.py
2. api_calls.py
3. merged_calc.py
4. geodata.py
5. choose your own adventure variables!
    analysis.py (template)
    childpov.py
    FeCollegeRatio.py
    FeEnrollRate.py
    MedInc18.py
    
#girlswhocode 
#blackwomeninstem