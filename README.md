# APA-789-Project: Abortion Access and Social Indicators
 
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

    all of the social data comes from the census! the verywell health data uses the population estimates from the 5 year american community survey population estimates from 2019 so all of the variables also come from that same 5 year acs estimate using api calls 

4. necessary downloads/systems

    geopandas - adds support to pandas for geospatial data - https://geopandas.org/en/stable/getting_started/install.html
    
    cartopy - adds support for making maps and other visuals using geospatial data - https://scitools.org.uk/cartopy/docs/latest/installing.html
   
    census api key - allows you to pull large amount of census data from census tables - https://api.census.gov/data/key_signup.html
    
    census data tables - landing page for census tables which you will pull your data from - https://data.census.gov/cedsci/

script running order:
    
1. state_rank.py
    
    this script inputs our CSV of abortion data and makes it into a ranked dataframe
    
2. api_calls.py

    this script has all of the api calls and merges into a dataframe
    
3. merged_calc.py

    this script takes some of the raw population numbers from the api calls and calculates them into rates for easier data comparison
    
4. geodata.py

    this script takes the dataframe we've been working with and merges it with a geospatial dataframe from the census and maps the results of our initial abortion data
    
5. choose your own adventure variables!

    these scripts essentially do the same thiing as geodata.py by providing the same mapping with different variables so you can visually compare the relationship of abortion access to the other social indicators

    analysis.py (template)
    
    childpov.py
    
    FeCollegeRatio.py
    
    FeEnrollRate.py
    
    MedInc18.py
    
findings

in doing this project i was aware that my results would in no way be causal, but just a way to look at the relationship between abortion access and several economic and educational indicators. in the future i hope to expand upon this project with more years of data and additional indicators to try to move more into the realm of causation. in the variables i tested i found that there is not always a strong correlation between access and certain factors and that in certain states there was. many of the results of the social indicators can be attributed to cultural factors and political ideologies that will need to be explored in a future study. for now, i can only hope that we move towards a better understanding of each other as people and that we all retain control over our bodily autonomy. 
    
#girlswhocode 
#blackwomeninstem