#!/usr/bin/env python
# coding: utf-8

# In[4]:


import numpy as np
import pandas as pd
import pickle
import streamlit as st
import math
import sklearn
from sklearn.linear_model import LinearRegression


# In[ ]:


# custom function from Itlian_Similar_players notebook 
from Italian_Seria_B_Similar_players import similar_player, calculate_similarities ,Total_wage_bill


# In[ ]:


# custom function from Web_scrapper_League_Tables notebook 
from ipynb.fs.full.Web_scrapper_League_Tables import League_table_scraper


# In[ ]:


st.set_page_config(layout = "wide")


# In[6]:


# Load machine learning model
model = pickle.load(open('model_it.pkl', 'rb'))


# ####  Functions for Preproccessing

# In[7]:


def Age(age):
    """
    Function takes age as an argument and returns 
    the age range
    
    """
    age = int(float(age))
    
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


# In[ ]:


countries = ['guadeloupe', 'guinea', 'italy', 'portugal', 'ecuador', 'germany',
           'brazil', 'argentina', 'serbia', 'croatia', 'ghana', 'colombia',
           'slovenia', 'finland', "cote-d'ivoire", 'slovakia', 'france',
           'nigeria', 'sweden', 'senegal', 'switzerland', 'montenegro',
           'morocco', 'martinique', 'uruguay', 'spain', 'netherlands',
           'romania', 'libya', 'greece', 'chile', 'scotland', 'poland',
           'united-states', 'denmark', 'liechtenstein', 'czech-republic',
           'belgium', 'cyprus', 'bulgaria', 'albania', 'austria',
           'the-gambia', 'bosnia-herzegovina', 'canada', 'iceland',
           'lithuania', 'north-macedonia', 'israel', 'norway', 'hungary',
           'mali', 'australia', 'venezuela', 'tunisia', 'cote-d-ivoire',
           'turkey', 'equatorial-guinea', 'sierra-leone', 'new-zealand',
           'northern-ireland', 'honduras', 'estonia', 'moldova', 'peru',
           'angola', 'dominican-republic', 'kosovo', 'malta', 'gabon',
           'liberia', 'congo', 'guinea-bissau', 'ireland', 'england',
           'latvia', 'paraguay', 'russia', 'suriname']


# In[ ]:


#based on uk.gov website excluding Italy
EU_countries = ['Austria', 'Bulgaria','Belgium','Croatia','Cyprus', 'Czech-Republic', 
              'Denmark', 'Estonia', 'Finland', 'France', 'Greece', 'Hungary', 'Ireland', 'Germany',
              'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 'Poland', 'Portugal', 
              'Romania', 'Slovakia', 'Slovenia', 'Spain','Sweden']

EU_countries = [s.lower() for s in EU_countries]


# In[ ]:


EU = []
non_EU = []
for country in countries:
    if country in EU_countries:
        EU.append(country) 
    elif country == 'italy':
        pass
    else:
        non_EU.append(country) 


# In[ ]:


len(countries)-len(EU)-len(non_EU)


# In[8]:


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
        return 'italy'


# In[9]:


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


# In[ ]:


CODE_DICT = {'Ascoli': 'ASC',
 'Benevento': 'BEN',
 'Chievo Verona': 'CVE',
 'Cittadella': 'CIT',
 'Cosenza': 'COS',
 'Cremonese': 'CRE',
 'Crotone': 'CRO',
 'Empoli': 'EMP',
 'Frosinone': 'FRO',
 'Juve Stabia': 'JUS',
 'Livorno': 'LVN',
 'Perugia': 'PER',
 'Pescara': 'PES',
 'Pisa': 'PIS',
 'Pordenone': 'POD',
 'Salernitana': 'SAL',
 'Spezia': 'SPZ',
 'Trapani': 'TRP',
 'Venezia': 'VEN',
 'Virtus Entella': 'ENT',
 'Brescia': 'BRE',
 'Lecce': 'LEC',
 'Monza': 'MZN',
 'Reggiana': 'RGA',
 'Reggina': 'REG',
 'SPAL': 'SPA',
 'Vicenza': 'VIC',
 'Alessandria': 'ALS',
 'Como': 'COM',
 'Parma': 'PAR',
 'Ternana': 'TER',
 'Bari': 'BAR',
 'Cagliari': 'CAG',
 'Genoa': 'GEN',
 'Modena': 'MOD',
 'Palermo': 'PAL',
 'Sudtirol': 'SUD',
 'Chievo': 'CVE',
 'Südtirol': 'SUD'}


# In[10]:


# Final league standings 2019/2020
standings_2019 = League_table_scraper('https://en.wikipedia.org/wiki/2019%E2%80%9320_Serie_B',6)
standings_2019 = list(map(lambda x: CODE_DICT[x], standings_2019.club))

# Final league standings 2020/2021
standings_2020 = League_table_scraper('https://en.wikipedia.org/wiki/2020%E2%80%9321_Serie_B',6)
standings_2020 = list(map(lambda x: CODE_DICT[x], standings_2020.club))

# Final league standings 2021/2022
standings_2021 = League_table_scraper('https://en.wikipedia.org/wiki/2021%E2%80%9322_Serie_B',6)
standings_2021 = list(map(lambda x: CODE_DICT[x], standings_2021.club))

# Current league standings 2022/2023
standings_2022 = League_table_scraper('https://en.wikipedia.org/wiki/2022%E2%80%9323_Serie_B',6)
standings_2022 = list(map(lambda x: CODE_DICT[x], standings_2022.club))


# In[11]:


BIG_3_2019 = ['EMP','FRO','CVE']
SMALL_5_2019 = ['ENT','POD','JUS','PIS','TRP']

BIG_3_2020 = ['LEC','BRE','SPA']
SMALL_4_2020 = ['MZN','VIC','RGA','REG']

BIG_3_2021 = ['BEN','CRO','PAR']
SMALL_4_2021 = ['COM','PER','TER','ALS']

BIG_3_2022 = ['CAG','GEN','VEN']
SMALL_4_2022 = ['SUD','MOD','BAR','PAL']


# In[12]:


def Club_type(club):
    
    """
    Function takes club as argument and returns
    BIG_3,SMALL_4,promoted,top 6, mid-table or relegation based on the club 
    finishing position for 2022. If club  was not in 
    the league in 2022 returns default value midtable
    
    """
    if club in BIG_3_2022:
        return 'BIG_3'
    
    if club in SMALL_4_2022:
        return 'SMALL_4'
    
    else:
        if club in standings_2022[0:2] :
            return 'promoted'
   
        if club in standings_2022[2:6] :
            return 'top 6'
    
        if club in standings_2022[6:16] :
            return 'mid-table'
    
        else :
            return 'mid-table'
    
 


# In[13]:


def Starter(starter):
    
     if starter =='Yes' :
        return '1'
     else:
        return '0'


# #### Preproccessing function

# In[3]:


def Pre_processing(team,position,country,age,starter):
    """
    takes user inputs as arguments and converts data 
    from long to wide format.Returns a data frame ready to
    used in prediction
    
    """
    global df
    
    df = pd.read_csv(r"C:\Users\Ramya\X_test_it.csv")
    
    df = df.iloc[:,1:] #clean dataframe
    df = df.iloc[0:0]  #drop all data
    df = df.append(pd.Series(0, index = df.columns), ignore_index = True)  # add a row of zero
    
    
    # First catogeries are removed form the catgorical variables when creating dummies
    if team == 'ALS':
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

    if Region(country) == 'EU':
        pass
    else:
        df['region_'+str(Region(country))] = 1

    if Club_type(team) == 'BIG_4':
        pass
    else:
        df['club_level_'+ str(Club_type(team))] = 1

    if Starter(starter) == '0':
        pass
    else:
        df['high_earner_'+Starter(starter)] = 1

    return df


# #### Function for model prediction

# In[15]:


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

# In[1]:


CLUBS = ('ALS','ASC','BAR','BEN','BRE','CAG','CIT','COM','COS','CRE','CRO',
         'CVE','EMP','ENT','FRO','GEN','JUS','LEC','LVN','MOD','MZN','PAL',
         'PAR','PER','PES','PIS','POD','REG','RGA','SAL','SPA','SPZ','SUD',
         'TER','TRP','VEN','VIC')

POSITIONS = ('Defender','Midfielder','Foward','Keeper')

COUNTRIES = ('guadeloupe', 'guinea', 'italy', 'portugal', 'ecuador', 'germany',
           'brazil', 'argentina', 'serbia', 'croatia', 'ghana', 'colombia',
           'slovenia', 'finland', "cote-d'ivoire", 'slovakia', 'france',
           'nigeria', 'sweden', 'senegal', 'switzerland', 'montenegro',
           'morocco', 'martinique', 'uruguay', 'spain', 'netherlands',
           'romania', 'libya', 'greece', 'chile', 'scotland', 'poland',
           'united-states', 'denmark', 'liechtenstein', 'czech-republic',
           'belgium', 'cyprus', 'bulgaria', 'albania', 'austria',
           'the-gambia', 'bosnia-herzegovina', 'canada', 'iceland',
           'lithuania', 'north-macedonia', 'israel', 'norway', 'hungary',
           'mali', 'australia', 'venezuela', 'tunisia', 'cote-d-ivoire',
           'turkey', 'equatorial-guinea', 'sierra-leone', 'new-zealand',
           'northern-ireland', 'honduras', 'estonia', 'moldova', 'peru',
           'angola', 'dominican-republic', 'kosovo', 'malta', 'gabon',
           'liberia', 'congo', 'guinea-bissau', 'ireland', 'england',
           'latvia', 'paraguay', 'russia', 'suriname')


# #### Streamlit App

# In[17]:


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

st.write('Wage as a Precentage of '+ str(team)+'`s total wage bill:',str(round(result*100/Total_wage_bill(team),2))+'%')

st.write(table)

