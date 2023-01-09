#!/usr/bin/env python
# coding: utf-8

# In[57]:


import pandas as pd 
# default='warn', Used here to supress warning when slicing and creating high earners column
pd.options.mode.chained_assignment = None 


# In[58]:


import requests
import json
import pandas as pd 
import numpy as np
import math


# In[59]:


# custom function from Web_scrapper_League_Tables notebook 
from ipynb.fs.full.Web_scrapper_League_Tables import League_table_scraper


# #### Get data from API

# In[60]:


API_key='d15f7132973d404d9d046934398ee9e3'


# In[61]:


# API authorization
headers = {'x-api-key':'d15f7132973d404d9d046934398ee9e3', 'accept': 'application/json', 'accept': 'text/csv'}

# Choose endpoint
endpoint = 'https://www.capology.com/api/v2/soccer/salaries/de/1-bundesliga/2019-2020/'

# Retrieve json
json1 = requests.get(endpoint, headers = headers).text

#Data for 2019/2020
df1 = pd.read_json(json1)


df1 = df1[df1["season_term"] == "combined"]


# In[62]:


# API authorization
headers = {'x-api-key':'d15f7132973d404d9d046934398ee9e3', 'accept': 'application/json', 'accept': 'text/csv'}

# Choose endpoint
endpoint = 'https://www.capology.com/api/v2/soccer/salaries/de/1-bundesliga/2020-2021/'

# Retrieve json
json2 = requests.get(endpoint, headers=headers).text

#Data for 2020/2021
df2 = pd.read_json(json2)


df2 = df2[df2["season_term"] == "combined"]


# In[63]:


# API authorization
headers = {'x-api-key':'d15f7132973d404d9d046934398ee9e3', 'accept': 'application/json', 'accept': 'text/csv'}

# Choose endpoint
endpoint = 'https://www.capology.com/api/v2/soccer/salaries/de/1-bundesliga/2021-2022/'

# Retrieve json
json3 = requests.get(endpoint, headers=headers).text

#Data for 2021/2022
df3 = pd.read_json(json3)


df3 = df3[df3["season_term"] == "combined"]


# In[64]:


# API authorization
headers = {'x-api-key':'d15f7132973d404d9d046934398ee9e3', 'accept': 'application/json', 'accept': 'text/csv'}

# Choose endpoint
endpoint = 'https://www.capology.com/api/v2/soccer/salaries/de/1-bundesliga/2022-2023/'

# Retrieve json
json4 = requests.get(endpoint, headers=headers).text

#Data for 2022/2023
df4 = pd.read_json(json4)

#Capology has defined the seson as summer
df4 = df4[df4["season_term"] == "summer"]


# In[65]:


df = pd.concat([df1,df2,df3,df4],axis=0).drop_duplicates()


# #### Clean dataframe

# In[66]:


df = df[df['salary_gross_eur'] != 0]


# In[67]:


df = df.drop_duplicates().reset_index(drop = True)


# In[69]:


#Required columns
LIST = ['season_id','club_code','player_age','player_country_id','player_group_code','salary_gross_eur']


# In[70]:


df_salary = df[LIST].reset_index(drop = True)


# In[71]:


df_salary.head()


# #### Define needed features
# 

# In[72]:


# Group the data by 'club' and 'position'
groups = df_salary.groupby(['club_code', 'player_group_code','season_id'])
# Find the highest two values of column 'salary_gross_eur' for each group
top_two = groups['salary_gross_eur'].nlargest(2).reset_index()

# get needed indexes
index = list(top_two['level_3'])

# Add the result to the data frame as a new column
df_salary['high_earner'] = 0
for i in index:
    df_salary.loc[i, 'high_earner'] = 1


# In[73]:


# Add the result to the data frame as a new column
df['high_earner'] = 0
for i in index:
    df.loc[i, 'high_earner'] = 1


# In[74]:


# Required columns for related players
LIST2 = ['season_id','player_name','club_code','player_age','player_country_id','player_group_code','salary_gross_eur','high_earner']


# In[75]:


df_similar = df[LIST2]


# In[76]:


countries = df_salary.player_country_id.unique()

#based on uk.gov website excluding Germany
EU_countries = ['Austria', 'Bulgaria','Belgium', 'Croatia','Cyprus', 'Czech-Republic', 
              'Denmark', 'Estonia', 'Finland', 'France', 'Greece', 'Hungary', 'Ireland', 'Italy',
              'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 'Poland', 'Portugal', 
              'Romania', 'Slovakia', 'Slovenia', 'Spain','Sweden']

EU_countries = [s.lower() for s in EU_countries]


# In[77]:


countries


# In[78]:


EU = []
non_EU = []
for country in countries:
    if country in EU_countries:
        EU.append(country) 
    elif country == 'germany':
        0
    else:
        non_EU.append(country) 


# In[79]:


def set_region(row):
    """
    Function takes each row as argument and returns the region 
    based on the player_country_id.
    """

    if row['player_country_id'] in non_EU:
        return 'non_EU'
    
    elif row['player_country_id'] in EU:
        return 'EU'
    
    else:
        return 'germany'


# In[ ]:


#Updating coding dicitionary as capology has differnt naming convention to Wikipedia
CODE_DICT = pd.Series(df.club_code.values,index=df.club_name).to_dict()

CODE_DICT['1. FC Köln'] = 'CGN'
CODE_DICT['Borussia Mönchengladbach'] = 'BMG'
CODE_DICT['RB Leipzig'] = 'RBL'
CODE_DICT['1899 Hoffenheim'] = 'TSG'
CODE_DICT['VfL Wolfsburg'] = 'WOB'
CODE_DICT['SC Freiburg'] = 'SCF'
CODE_DICT['Hertha BSC'] = 'BSC'
CODE_DICT['Mainz 05'] = 'MAI'
CODE_DICT['FC Augsburg'] = 'AUG'
CODE_DICT['Fortuna Düsseldorf'] = 'F95'
CODE_DICT['SC Paderborn'] = 'PAD'
CODE_DICT['VfB Stuttgart'] = 'STU'
CODE_DICT['VfL Bochum'] = 'BCM'
CODE_DICT['Greuther Fürth'] = 'FUR'
CODE_DICT['Borussia Mönchengladbach'] = 'BMG'


# In[80]:


# Final league standings 2019/2020
standings_2019 = League_table_scraper('https://en.wikipedia.org/wiki/2019%E2%80%9320_Bundesliga',6)
standings_2019 = list(map(lambda x: CODE_DICT[x], standings_2019.club))

# Final league standings 2020/2021
standings_2020 = League_table_scraper('https://en.wikipedia.org/wiki/2020%E2%80%9321_Bundesliga',6)
standings_2020 = list(map(lambda x: CODE_DICT[x], standings_2020.club))

# Final league standings 2021/2022
standings_2021 = League_table_scraper('https://en.wikipedia.org/wiki/2021%E2%80%9322_Bundesliga',5)
standings_2021 = list(map(lambda x: CODE_DICT[x], standings_2021.club))

# Current league standings 2022/2023
standings_2022 = League_table_scraper('https://en.wikipedia.org/wiki/2022%E2%80%9323_Bundesliga',5)
standings_2022 = list(map(lambda x: CODE_DICT[x], standings_2022.club))


# In[98]:


set(df.club_code)


# In[83]:


def set_club_type(row):
    
    """
    Function takes each row as argument and returns
    top 4,top 6,mid-table, relagation based on the club 
    finishing position for the year
    
    """

    if (row['club_code'] in standings_2019[:4] and row['season_id']== '2019-2020') or (row['club_code'] in standings_2020[0:4] and row['season_id']=='2020-2021') or (row['club_code'] in standings_2021[0:4] and row['season_id']=='2021-2022') or (row['club_code'] in standings_2022[0:4] and row['season_id']=='2022-2023'):
        return 'top 4'
   
    if (row['club_code'] in standings_2019[4:6] and row['season_id']== '2019-2020') or (row['club_code'] in standings_2020[4:6] and row['season_id']=='2020-2021') or (row['club_code'] in standings_2021[4:6] and row['season_id']=='2021-2022') or (row['club_code'] in standings_2022[4:6] and row['season_id']=='2022-2023'):
        return 'top 6'
    
    if (row['club_code'] in standings_2019[6:15] and row['season_id']== '2019-2020') or (row['club_code'] in standings_2020[6:15] and row['season_id']=='2020-2021') or (row['club_code'] in standings_2021[6:15] and row['season_id']=='2021-2022') or (row['club_code'] in standings_2022[6:15] and row['season_id']=='2022-2023'):
        return 'mid-table'
    
    else :
        return 'relegation'


# In[84]:


X = df_salary[['club_code', 'player_age', 'player_country_id', 'player_group_code','season_id','high_earner']]

X = X.assign(Age = pd.cut(X['player_age'], 
                               bins = [0, 17, 21,23, 27, 32,99], 
                               labels = ['U18', '18-21', '21-23','23-27','27-32','32+']))

X = X.assign(region = X.apply(set_region, axis = 1)).astype('category')

X = X.assign(club_level = X.apply(set_club_type,axis = 1)).astype('category')

X = X.drop('player_age',axis=1)
X = X.drop('season_id',axis=1)


# In[85]:


def Club_type(club):
    
    """
    Function takes club as argument and returns
    top 4 ,top 6 ,mid-table, relagation based on the club 
    finishing position for 2022. If club  was not in 
    the league in 2022 returns default value midtable
    
    """

    if club in standings_2022[0:4] :
        return 'top 4'
   
    if club in standings_2022[4:6] :
        return 'top 6'
    
    if club in standings_2022[6:15] :
        return 'mid-table'
    
    else :
        return 'mid-table'
    
 


# In[86]:


def Region(country):
    
    """
    Function takes country as an argument and returns 
    the region of the country
    
    """

    if country in non_EU:
        return 'non_EU'
    
    elif country in EU:
        return 'EU'
    
    else:
        return 'germany'


# In[87]:


def Age(age):
    """
    Function takes age as an argument and returns 
    the age range
    
    """
    if age <= 18:
        return 'U18'
    if age in range(18, 22):
        return '18-21'
    if age in range(22, 24):
        return '21-23'
    if age in range(24, 28):
        return '23-27'
    if age in range(28, 33):
        return '27-32'
    return '32+'


# In[88]:


def Starter(starter):
    
     if starter == 'Yes' :
        return '1'
     else:
        return '0'


# In[89]:


def calculate_similarities(row,input_data):
    s = 0
    
    if row['club_code'] == input_data[0]:   # Check for same club
        s += 1
    
    if row['club_level'] == Club_type(input_data[0]):  # Check for simlar level club
        s += 0.5
    
    if row['player_group_code'] == input_data[1]:
        s += 4
    
    if row['player_country_id'] == input_data[2]:  # Check for same country
        s += 1
    
    if row['region'] == Region(input_data[2]):   # Check for same region
        s += 0.5
    
    if row['Age'] == Age(input_data[3]):
        s += 1
    
    if row['high_earner'] == Starter(input_data[4]):
        s += 8
    
    return s


# In[90]:


def similar_player(data):
    
    X['similarities'] = X.apply(calculate_similarities, axis = 1,input_data = data)
    X_sorted = X.sort_values(by = 'similarities', ascending = False)
    top_5 = X_sorted.head(5)
    indexes = top_5.index

    
    return df_similar.loc[indexes]


# In[91]:


similar_player(['BMG','M','germany',25,'Yes'])


# #### Additional function to get % spend on player

# In[92]:


def Total_wage_bill(club):
    """
    function takes in club as argument and 
    returns the the total wage bill of the club
    
    """
    df_filtered = df_salary.loc[df_salary['club_code'] == club]
    
    #Number of seasons for which data is available for the club
    n = len(df_filtered.season_id.unique())
    
    #Assuming club has simlar squad sizes each season
    total = df_filtered['salary_gross_eur'].sum()/n
    
    return total


# In[93]:


Total_wage_bill('BAY')


# In[95]:


# Convert notebook to script
# jupyter nbconvert --to script Germany_Bundesliga_Similar_players.ipynb

