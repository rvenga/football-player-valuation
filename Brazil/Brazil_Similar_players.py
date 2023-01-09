#!/usr/bin/env python
# coding: utf-8

# In[22]:


import pandas as pd 
# default='warn', Used here to supress warning when slicing and creating high earners column
pd.options.mode.chained_assignment = None 


# In[23]:


import requests
import json
import pandas as pd 
import numpy as np
import math


# In[24]:


# custom function from Web_scrapper_League_Tables notebook 
from ipynb.fs.full.Web_scrapper_League_Tables import League_table_scraper


# #### Get data from API

# In[25]:


API_key='d15f7132973d404d9d046934398ee9e3'


# In[26]:


# API authorization
headers = {'x-api-key':'d15f7132973d404d9d046934398ee9e3', 'accept': 'application/json', 'accept': 'text/csv'}

# Choose endpoint
endpoint = 'https://www.capology.com/api/v2/soccer/salaries/br/brasileiro/2020/'

# Retrieve json
json = requests.get(endpoint, headers=headers).text

#Data for 2021
df1 = pd.read_json(json)

df1 = df1[df1["season_term"] == "combined"].reset_index(drop = True)


# In[27]:


# API authorization
headers = {'x-api-key':'d15f7132973d404d9d046934398ee9e3', 'accept': 'application/json', 'accept': 'text/csv'}

# Choose endpoint
endpoint = 'https://www.capology.com/api/v2/soccer/salaries/br/brasileiro/2021/'

# Retrieve json
json2 = requests.get(endpoint, headers=headers).text

#Data for 2021
df2 = pd.read_json(json2)

df2 = df2[df2["season_term"] == "summer"]


# In[28]:


# API authorization
headers = {'x-api-key':'d15f7132973d404d9d046934398ee9e3', 'accept': 'application/json', 'accept': 'text/csv'}

# Choose endpoint
endpoint = 'https://www.capology.com/api/v2/soccer/salaries/br/brasileiro/2022/'

# Retrieve json
json3 = requests.get(endpoint, headers=headers).text

#Data for 2022
df3 = pd.read_json(json3)

df3 = df3[df3["season_term"] == "summer"]


# In[29]:


df = pd.concat([df1,df3,df2],axis=0).drop_duplicates()


# #### Clean dataframe

# In[30]:


df= df[df['salary_gross_eur'] != 0]


# In[31]:


df=df.drop_duplicates().reset_index(drop = True)


# In[32]:


CODE_DICT=pd.Series(df.club_code.values,index=df.club_name).to_dict()


# In[33]:


#Required columns
LIST=['season_id','club_code','player_age','player_country_id','player_group_code','salary_gross_eur']


# In[34]:


df_salary=df[LIST]


# #### Add needed features
# 

# In[35]:


# Group the data by 'club' and 'position'
groups = df_salary.groupby(['club_code', 'player_group_code','season_id'])
# Find the highest two values of column 'salary_gross_eur' for each group
top_two = groups['salary_gross_eur'].nlargest(2).reset_index()

# get needed indexes
index=list(top_two['level_3'])

# Add the result to the data frame as a new column
df_salary['high_earner'] = 0
for i in index:
    df_salary.loc[i, 'high_earner'] = 1


# In[36]:


# Add the result to the data frame as a new column
df['high_earner'] = 0
for i in index:
    df.loc[i, 'high_earner'] = 1


# In[37]:


df_salary.head()


# In[38]:


# Required columns for related players
LIST2=['season_id','player_name','club_code','player_age','player_country_id','player_group_code','salary_gross_eur','high_earner']


# In[39]:


df_similar=df[LIST2]


# In[40]:


def set_region(row):
    """
    Function takes each row as argument and returns the region 
    based on the player_country_id.
    """
    
    south_america = {'uruguay', 'colombia', 'argentina', 'ecuador','chile', 'venezuela', 'paraguay','peru','bolivia'}
    europe = {'spain','italy','belarus','portugal','finland','ukraine','finland'}
    rest_of_world = {'south-korea','united-states','china','japan','cote-d-ivoire'}
    
    if row['player_country_id'] in south_america:
        return 'south america'
    
    elif row['player_country_id'] in europe:
        return 'europe'
    
    elif row['player_country_id'] in rest_of_world:
        return 'rest of the world'
    
    else:
        return 'brazil'


# In[41]:


CODE_DICT


# In[42]:


# Update dictonary by running the map function and checking the mising keys 
CODE_DICT['Grêmio'] = 'GRM'
CODE_DICT['São Paulo'] = 'SAP'
CODE_DICT['Goiás'] = 'GOI'
CODE_DICT['Bahia'] = 'ECB'
CODE_DICT['Ceará'] ='CEA'
CODE_DICT['Atlético Mineiro'] ='CAM'
CODE_DICT['Atlético Goianiense'] ='GOE'
CODE_DICT['Sport'] = 'SCR'
CODE_DICT['América Mineiro'] = 'AMG'
CODE_DICT['Cuiabá'] = 'CUI'
CODE_DICT['Avaí'] = 'AVI'


# In[43]:


# Final league standings 2020
standings_2020 = League_table_scraper('https://en.wikipedia.org/wiki/2020_Campeonato_Brasileiro_S%C3%A9rie_A',9)
standings_2020 = list(map(lambda x: CODE_DICT[x], standings_2020.club))

# Final league standings 2021
standings_2021 = League_table_scraper('https://en.wikipedia.org/wiki/2021_Campeonato_Brasileiro_S%C3%A9rie_A',9)
standings_2021 = list(map(lambda x: CODE_DICT[x], standings_2021.club))

# Final league standings 2022
standings_2022 = League_table_scraper('https://en.wikipedia.org/wiki/2022_Campeonato_Brasileiro_S%C3%A9rie_A',9)
standings_2022 = list(map(lambda x: CODE_DICT[x], standings_2022.club))


# In[44]:


def set_club_type(row):
    
    """
    Function takes each row as argument and returns
    top 6,6-10,mid-table, relagation based on the club 
    finishing position for the year
    
    """
    if (row['club_code'] in standings_2020[:6] and row['season_id']==2020) or (row['club_code'] in standings_2021[0:6] and row['season_id']==2021) or (row['club_code'] in standings_2022[0:6] and row['season_id']==2022):
        return 'top 6'
   
    elif (row['club_code'] in standings_2020[6:11] and row['season_id']==2020) or (row['club_code'] in standings_2021[6:11] and row['season_id']==2021) or (row['club_code'] in standings_2022[6:11] and row['season_id']==2022):
        return '6-10'
    
    elif (row['club_code'] in standings_2020[11:16] and row['season_id']==2020) or (row['club_code'] in standings_2021[11:16] and row['season_id']==2021) or (row['club_code'] in standings_2022[11:16] and row['season_id']==2022):
        return 'mid-table'
    
    else :
        return 'relegation'


# In[45]:


X = df_salary[['club_code', 'player_age', 'player_country_id', 'player_group_code','season_id','high_earner']]

X = X.assign(Age=pd.cut(X['player_age'], 
                               bins=[0, 17, 21,23, 27, 32,99], 
                               labels=['U18', '18-21', '21-23','23-27','27-32','32+']))

X = X.assign(region=X.apply(set_region, axis=1)).astype('category')

X = X.assign(club_level=X.apply(set_club_type,axis=1)).astype('category')

X = X.drop('player_age',axis=1)
 
X = X.drop('season_id',axis=1)


# In[46]:


X.head()


# In[47]:


def Club_type(club):
    
    """
    Function takes club as argument and returns
    top 6,6-10,mid-table, relagation based on the club 
    finishing position for 2022. If club  was not in 
    the league in 2022 returns default value midtable
    
    """
    if club in standings_2022[:6]:
        return 'top 6'
   
    if club in standings_2022[6:11]:
        return '6-10'
    
    if club in standings_2022[11:16]:
        return 'mid-table'
    
    if club in standings_2022[16:] :
        return 'relegation'
    
    else:
        return 'mid-table'


# In[48]:


def Region(country):
    
    """
    Function takes country as an argument and returns 
    the region of the country
    
    """
    
    south_america = {'uruguay', 'colombia', 'argentina', 'ecuador','chile', 'venezuela', 'paraguay','peru','bolivia'}
    europe = {'spain','italy','belarus','portugal','finland','ukraine','finland'}
    rest_of_world = {'south-korea','united-states','china','japan','cote-d-ivoire'}
    brazil={'brazil'}
    
    if country in south_america:
        return 'south america'
    
    elif country in europe:
        return 'europe'
    
    elif country in rest_of_world:
        return 'rest of the world'
    
    elif country in brazil:
        return 'brazil'
    
    else:
        return 'not in data'


# In[49]:


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


# In[50]:


def Starter(starter):
    
     if starter =='Yes' :
        return '1'
     else:
        return '0'


# In[51]:


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


# In[52]:


def similar_player(data):
    
    X['similarities'] = X.apply(calculate_similarities, axis = 1,input_data = data)
    X_sorted = X.sort_values(by = 'similarities', ascending = False)
    top_5 = X_sorted.head(5)
    indexes = top_5.index

    
    return df_similar.loc[indexes]


# In[53]:


similar_player(['AMG','D','brazil',34,'Yes'])


# #### Additional function to get % spend on player

# In[54]:


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


# In[55]:


Total_wage_bill('AMG')


# In[ ]:


# Convert notebook to script run in terminal
# jupyter nbconvert --to script Brazil_Similar_players.ipynb


# In[ ]:




