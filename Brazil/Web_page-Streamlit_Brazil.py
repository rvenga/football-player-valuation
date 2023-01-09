#!/usr/bin/env python
# coding: utf-8

# In[7]:


import numpy as np
import pandas as pd
import pickle
import streamlit as st
import math
import sklearn
from sklearn.linear_model import LinearRegression


# In[8]:


# custom function from Brazil_Similar_players notebook 
from Brazil_Similar_players  import similar_player, calculate_similarities ,Total_wage_bill


# In[9]:


# custom function from Web_scrapper_League_Tables notebook 
from ipynb.fs.full.Web_scrapper_League_Tables import League_table_scraper


# In[10]:


st.set_page_config(layout = "wide")


# In[11]:


# Load machine learning model
model = pickle.load(open('model_br.pkl', 'rb'))


# ####  Functions for Preproccessing

# In[12]:


def Age(age):
    """
    Function takes age as an argument and returns 
    the age range
    
    """
    age= int(age)
    
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


# In[13]:


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


# In[14]:


def Position(position):
    """
    Function takes position as an argument and returns 
    the code of the position
    
    """
    if position == 'Defender':
        return 'D'
    
    if position == 'Midfielder':
        return 'M'
    
    if position == 'Foward':
        return 'F'
    
    if position == 'Keeper':
        return 'K'
    
    else:
        return 'not in data'


# In[15]:


#Updating coding dicitionary as capology has differnt naming convention to Wikipedia
CODE_DICT = {'Athletico Paranaense': 'CAP',
 'Atletico Mineiro': 'CAM',
 'Botafogo': 'BOT',
 'Ceara Sporting Club': 'CEA',
 'Corinthians': 'CRS',
 'Coritiba': 'CRB',
 'Esporte Clube Bahia': 'ECB',
 'Flamengo': 'FLA',
 'Fluminense': 'FLU',
 'Fortaleza': 'FOR',
 'Goianiense': 'GOE',
 'Goias': 'GOI',
 'Gremio': 'GRM',
 'Internacional': 'INR',
 'Palmeiras': 'PLM',
 'Red Bull Bragantino': 'RED',
 'Santos': 'SAN',
 'Sao Paulo': 'SAP',
 'Sport Club do Recife': 'SCR',
 'Vasco da Gama': 'VAS',
 'America FC': 'AMG',
 'Avai': 'AVI',
 'Cuiaba': 'CUI',
 'Juventude': 'JUD',
 'Chapecoense': 'CPE',
 'Grêmio': 'GRM',
 'São Paulo': 'SAP',
 'Goiás': 'GOI',
 'Bahia': 'ECB',
 'Ceará': 'CEA',
 'Atlético Mineiro': 'CAM',
 'Atlético Goianiense': 'GOE',
 'Sport': 'SCR',
 'América Mineiro': 'AMG',
 'Cuiabá': 'CUI',
 'Avaí': 'AVI'}


# In[16]:


# Final league standings 2020
standings_2020 = League_table_scraper('https://en.wikipedia.org/wiki/2020_Campeonato_Brasileiro_S%C3%A9rie_A',9)
standings_2020 = list(map(lambda x: CODE_DICT[x], standings_2020.club))

# Final league standings 2021
standings_2021 = League_table_scraper('https://en.wikipedia.org/wiki/2021_Campeonato_Brasileiro_S%C3%A9rie_A',9)
standings_2021 = list(map(lambda x: CODE_DICT[x], standings_2021.club))

# Final league standings 2022
standings_2022 = League_table_scraper('https://en.wikipedia.org/wiki/2022_Campeonato_Brasileiro_S%C3%A9rie_A',9)
standings_2022 = list(map(lambda x: CODE_DICT[x], standings_2022.club))


# In[17]:


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


# In[18]:


def Starter(starter):
    
     if starter =='Yes' :
        return '1'
     else:
        return '0'


# #### Preproccessing function

# In[20]:


def Pre_processing(team,position,country,age,starter):
    """
    takes user inputs as arguments and converts data 
    from long to wide format.Returns a data frame ready to
    used in prediction
    
    """
    global df
    
    df = pd.read_csv(r"C:\Users\Ramya\X_test_br.csv")
    
    df = df.iloc[:,1:] #clean dataframe
    df = df.iloc[0:0]  #drop all data
    df = df.append(pd.Series(0, index=df.columns), ignore_index=True)  # add a row of zero
    
    # First catogeries are removed form the catgorical variables when creating dummies
    if team == 'AMG':
         pass    
    else:
        df['club_code_' + str(team)] = 1
        
    if position == 'Defender':
        pass
    else:
        df['player_group_code_' + str(Position(position))] = 1
    
    if Age(age) == 'U18' :
        pass
    else:
        df['Age_'+ str(Age(age))] = 1
        
    if Region(country) == 'brazil':
        pass
    else:
        df['region_'+str(Region(country))] = 1
        
    if Club_type(team) == '6-10':
        pass
    else:
        df['club_level_'+ str(Club_type(team))] = 1
        
    if Starter(starter) == '0':
        pass
    else:
        df['high_earner_'+Starter(starter)] = 1
    
    return df
    


# #### Function for model prediction

# In[10]:


def Predict(team,position,country,age,starter):
    """
    Takes input from user , runs pre_processing function
    to prepare the data, runs the model and returns
    the model prediction
    
    """
    
    # Preprocess the user input
    input_data = Pre_processing(team,position,country,age,starter)
    
    # Make a prediction using the model
    prediction = math.exp(model.predict(input_data))
    
    return prediction


# #### List Valid inputs

# In[11]:


CLUBS = ('CAP', 'CAM', 'BOT', 'CEA', 'CRS', 'CRB', 'ECB', 'FLA', 'FLU','FOR', 
         'GOE', 'GOI', 'GRM', 'INR', 'PLM', 'RED', 'SAN', 'SAP','SCR', 'VAS', 
         'AMG', 'AVI', 'CUI', 'JUD', 'CPE')

POSITIONS = ('Defender','Midfielder','Foward','Keeper')

COUNTRIES = ('brazil', 'colombia', 'uruguay', 'argentina', 'ecuador','venezuela',
             'paraguay', 'peru', 'japan', 'cote-d-ivoire', 'chile','south-korea', 
             'bolivia', 'italy', 'united-states', 'spain','china', 'ukraine', 'finland',
             'portugal', 'belarus')


# #### Streamlit App

# In[142]:


# Create a Streamlit app
st.title('Wage Estimate')

# Get user input using Streamlit widgets
team = st.selectbox('Enter player team?',(CLUBS))

position = st.selectbox('Enter player position?',(POSITIONS))

country = st.selectbox('Enter player country?',(COUNTRIES))

age = st.number_input('Enter age :',step=1)
age = int(age)

starter = st.selectbox('Is player starter?',(('Yes','No')))


# In[ ]:


# Call the function with the user input as arguments and display the result
result = round(Predict(team,position,country,age,starter))

table = similar_player([team,Position(position),country,age,Starter(starter)])

st.write('Wage Estimate:', f'{result:,}')

st.write('Wage as a Precentage of ' + str(team) + '`s total wage bill:',str(round(result*100/Total_wage_bill(team),2))+'%')

st.write(table)

