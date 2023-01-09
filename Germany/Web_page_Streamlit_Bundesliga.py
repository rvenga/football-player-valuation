#!/usr/bin/env python
# coding: utf-8

# In[13]:


import numpy as np
import pandas as pd
import pickle
import streamlit as st
import math
import sklearn
from sklearn.linear_model import LinearRegression


# In[15]:


# custom function from Germany_Bundesliga_Similar_players notebook 
from Germany_Bundesliga_Similar_players import similar_player, calculate_similarities ,Total_wage_bill


# In[16]:


# custom function from Web_scrapper_League_Tables notebook 
from ipynb.fs.full.Web_scrapper_League_Tables import League_table_scraper


# In[17]:


st.set_page_config(layout="wide")


# In[19]:


# Load machine learning model
model = pickle.load(open('model_de.pkl', 'rb'))


# ####  Functions for Preproccessing

# In[20]:


def Age(age):
    """
    Function takes age as an argument and returns 
    the age range
    
    """
    age= int(float(age))
    
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


# In[21]:


countries = ['iceland', 'germany', 'ecuador', 'finland', 'austria', 'brazil',
            'czech-republic', 'netherlands', 'croatia', 'denmark', 'nigeria',
            'england', 'switzerland', 'south-korea', 'venezuela', 'poland',
            'chile', 'burkina-faso', 'argentina', 'jamaica', 'france',
            'greece', 'canada', 'spain', 'new-zealand', 'morocco', 'belgium',
            'norway', 'united-states', 'portugal', 'ghana', 'turkey', 'japan',
            'kosovo', 'serbia', 'bosnia-herzegovina', 'guinea', 'albania',
            'australia', 'hungary', 'italy', 'slovakia', 'cote-d-ivoire',
            'mali', 'togo', 'israel', 'algeria', 'armenia', 'north-macedonia',
            'tunisia', 'colombia', 'sweden', 'wales', 'slovenia', 'uruguay',
            'romania', 'luxembourg', 'cameroon', 'paraguay', 'senegal',
            'bulgaria', 'democratic-republic-of-congo', 'angola', 'benin',
            'faroe-islands', 'latvia', 'democratic-republic-of-the-congo',
            'egypt', 'panama', 'russia', 'iran', 'costa-rica', 'philippines',
            'congo', 'cyprus', 'montenegro', 'ireland', 'suriname', 'ukraine',
            'the-gambia', 'scotland']


# In[22]:


#based on uk.gov website excluding Germany
EU_countries = ['Austria', 'Bulgaria','Belgium', 'Croatia','Cyprus', 'Czech-Republic', 
              'Denmark', 'Estonia', 'Finland', 'France', 'Greece', 'Hungary', 'Ireland', 'Italy',
              'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 'Poland', 'Portugal', 
              'Romania', 'Slovakia', 'Slovenia', 'Spain','Sweden']

EU_countries = [s.lower() for s in EU_countries]


# In[23]:


EU=[]
non_EU=[]
for country in countries:
    if country in EU_countries:
        EU.append(country) 
    elif country == 'germany':
        pass
    else:
        non_EU.append(country) 


# In[24]:


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


# In[25]:


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


# In[27]:


#Updating coding dicitionary as capology has differnt naming convention to Wikipedia
CODE_DICT = {'Augsburg': 'AUG',
 'Bayer Leverkusen': 'B04',
 'Bayern Munich': 'BAY',
 'Borussia Dortmund': 'BVB',
 'Dusseldorf': 'F95',
 'Eintracht Frankfurt': 'SGE',
 'Freiburg': 'SCF',
 'Hertha Berlin': 'BSC',
 'Hoffenheim': 'TSG',
 'Koln': 'CGN',
 'Leipzig': 'RBL',
 'Mainz': 'MAI',
 'Monchengladbach': 'BMG',
 'Paderborn': 'PAD',
 'Schalke 04': 'S04',
 'Union Berlin': 'UBE',
 'Werder Bremen': 'SVW',
 'Wolfsburg': 'WOB',
 'Arminia Bielefeld': 'ARB',
 'Stuttgart': 'STU',
 'Bochum': 'BCM',
 'Furth': 'FUR',
 '1. FC Köln': 'CGN',
 'Borussia Mönchengladbach': 'BMG',
 'RB Leipzig': 'RBL',
 '1899 Hoffenheim': 'TSG',
 'VfL Wolfsburg': 'WOB',
 'SC Freiburg': 'SCF',
 'Hertha BSC': 'BSC',
 'Mainz 05': 'MAI',
 'FC Augsburg': 'AUG',
 'Fortuna Düsseldorf': 'F95',
 'SC Paderborn': 'PAD',
 'VfB Stuttgart': 'STU',
 'VfL Bochum': 'BCM',
 'Greuther Fürth': 'FUR'}


# In[28]:


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


# In[29]:


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
    
 


# In[30]:


def Starter(starter):
    
     if starter =='Yes' :
        return '1'
     else:
        return '0'


# #### Preproccessing function

# In[31]:


def Pre_processing(team,position,country,age,starter):
    """
    takes user inputs as arguments and converts data 
    from long to wide format.Returns a data frame ready to
    used in prediction
    
    """
    global df
    
    df = pd.read_csv(r"C:\Users\Ramya\X_test_de.csv")
    
    df = df.iloc[:,1:] #clean dataframe
    df = df.iloc[0:0]  #drop all data
    df = df.append(pd.Series(0, index=df.columns), ignore_index=True)  # add a row of zero
    
    
    # First catogeries are removed form the catgorical variables when creating dummies
    if team == 'ARB':
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

    if Club_type(team) == 'mid-table':
        pass
    else:
        df['club_level_'+ str(Club_type(team))] = 1

    if Starter(starter) == '0':
        pass
    else:
        df['high_earner_'+Starter(starter)] = 1

    return df


# #### Function for model prediction

# In[32]:


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

# In[33]:


CLUBS = ('ARB','AUG','B04','BAY','BCM','BMG','BSC','BVB','CGN','F95','FUR','MAI','PAD','RBL','S04','SCF','SGE','STU','SVW','TSG','UBE','WOB')

POSITIONS = ('Defender','Midfielder','Foward','Keeper')

COUNTRIES = ('iceland', 'germany', 'ecuador', 'finland', 'austria', 'brazil',
            'czech-republic', 'netherlands', 'croatia', 'denmark', 'nigeria',
            'england', 'switzerland', 'south-korea', 'venezuela', 'poland',
            'chile', 'burkina-faso', 'argentina', 'jamaica', 'france',
            'greece', 'canada', 'spain', 'new-zealand', 'morocco', 'belgium',
            'norway', 'united-states', 'portugal', 'ghana', 'turkey', 'japan',
            'kosovo', 'serbia', 'bosnia-herzegovina', 'guinea', 'albania',
            'australia', 'hungary', 'italy', 'slovakia', 'cote-d-ivoire',
            'mali', 'togo', 'israel', 'algeria', 'armenia', 'north-macedonia',
            'tunisia', 'colombia', 'sweden', 'wales', 'slovenia', 'uruguay',
            'romania', 'luxembourg', 'cameroon', 'paraguay', 'senegal',
            'bulgaria', 'democratic-republic-of-congo', 'angola', 'benin',
            'faroe-islands', 'latvia', 'democratic-republic-of-the-congo',
            'egypt', 'panama', 'russia', 'iran', 'costa-rica', 'philippines',
            'congo', 'cyprus', 'montenegro', 'ireland', 'suriname', 'ukraine',
            'the-gambia', 'scotland')


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

st.write('Wage as a Precentage of ' + str(team) + '`s total wage bill:',str(round(result*100/Total_wage_bill(team),2)) + '%')

st.write(table)

