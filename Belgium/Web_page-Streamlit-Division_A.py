#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import pickle
import streamlit as st
import math
import sklearn
from sklearn.linear_model import LinearRegression


# In[ ]:


#custom function from Web_scrapper_League_Tables notebook 
from ipynb.fs.full.Web_scrapper_League_Tables import League_table_scraper


# In[ ]:


#custom Belgium_Division_A_Similar_player 
from Belgium_Division_A_Similar_players import similar_player, calculate_similarities ,Total_wage_bill


# In[ ]:


st.set_page_config(layout="wide")


# In[2]:


# Load machine learning model
model = pickle.load(open('model_be.pkl', 'rb'))


# ####  Functions for Preproccessing

# In[3]:


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


# In[4]:


countries = ['france', 'belgium', 'honduras', 'serbia', 'netherlands',
           'democratic-republic-of-the-congo', 'jamaica', 'united-states',
           'croatia', 'panama', 'austria', 'costa-rica', 'germany',
           'montenegro', 'albania', 'rwanda', 'ghana', 'poland',
           'cote-d-ivoire', 'senegal', 'finland', 'japan', 'mali', 'bulgaria',
           'greece', 'bosnia-herzegovina', 'congo', 'algeria', 'wales',
           'kenya', 'england', 'south-africa', 'hungary', 'tunisia', 'brazil',
           'canada', 'iran', 'togo', 'north-macedonia', 'sweden',
           'madagascar', 'angola', 'nigeria', 'colombia', 'ukraine',
           'uruguay', 'czech-republic', 'guinea-bissau', 'argentina', 'spain',
           'zimbabwe', 'portugal', 'benin', 'cameroon', 'italy', 'australia',
           'denmark', 'norway', 'slovakia', 'georgia', 'the-gambia',
           'comoros', 'scotland', 'burkina-faso', 'trinidad-and-tobago',
           'iceland', 'zambia', 'turkey', 'guinea', 'venezuela', 'israel',
           'haiti', 'sierra-leone', 'south-korea', 'romania', 'cyprus',
           'morocco', 'kosovo', 'switzerland', 'mexico', 'burundi', 'ireland',
           'kazakhstan', 'luxembourg', 'curacao', 'peru', 'Canada',
           'cape-verde', 'ecuador', 'malaysia', 'slovenia', 'jordan',
           'northern-ireland', 'new-zealand', 'bolivia', 'lithuania',
           'armenia', 'thailand', 'tanzania', 'chad', 'malta', 'mauritania',
           'grenada', 'chile', 'guadeloupe', 'russia', 'estonia']


# In[5]:



#based on uk.gov website excluding Belgium
EU_countries=['Austria', 'Bulgaria', 'Croatia','Cyprus', 'Czech-Republic', 
              'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Ireland', 'Italy',
              'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 'Poland', 'Portugal', 
              'Romania', 'Slovakia', 'Slovenia', 'Spain','Sweden']

EU_countries=[s.lower() for s in EU_countries]


# In[6]:


EU=[]
non_EU=[]
for country in countries:
    if country in EU_countries:
        EU.append(country) 
    elif country == 'belgium':
        pass
    else:
        non_EU.append(country) 


# In[7]:


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
        return 'belgium'


# In[8]:


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


CODE_DICT = {'Anderlecht': 'AND',
 'Beveren': 'BEV',
 'Cercle Brugges': 'CER',
 'Charleroi': 'CHL',
 'Club Brugges': 'BRU',
 'Eupen': 'EUP',
 'Excel Mouscron': 'EXM',
 'Genk': 'GEK',
 'Gent': 'GNT',
 'Kortrijk': 'KOR',
 'Mechelen': 'MEC',
 'Oostende': 'OOS',
 'Royal Antwerp': 'ATW',
 'Sint-Truidense': 'SIT',
 'Standard Liege': 'STL',
 'Zulte Waregem': 'ZUW',
 'Beerschot VA': 'BEE',
 'Leuven': 'LEU',
 'Seraing': 'SER',
 'Union SG': 'USG',
 'Westerlo': 'WES',
 'Club Brugge': 'BRU',
 'Antwerp': 'ATW',
 'Standard Liège': 'STL',
 'Sint-Truiden': 'SIT',
 'Cercle Brugge': 'CER',
 'Waasland-Beveren': 'BEV',
 'Beerschot': 'BEE',
 'OH Leuven': 'LEU'}


# In[ ]:


# Final league standings 2019/2020
standings_2019 = League_table_scraper('https://en.wikipedia.org/wiki/2019%E2%80%9320_Belgian_First_Division_A',4)
standings_2019 = list(map(lambda x: CODE_DICT[x], standings_2019.club))

# Final league standings 2020/2021
standings_2020= League_table_scraper('https://en.wikipedia.org/wiki/2020%E2%80%9321_Belgian_First_Division_A',5)
standings_2020 = list(map(lambda x: CODE_DICT[x], standings_2020.club))

# Final league standings 2021/2022
standings_2021 = League_table_scraper('https://en.wikipedia.org/wiki/2021%E2%80%9322_Belgian_First_Division_A',5)
standings_2021 = list(map(lambda x: CODE_DICT[x], standings_2021.club))

# Current league standings 2022/2023
standings_2022 = League_table_scraper('https://en.wikipedia.org/wiki/2022%E2%80%9323_Belgian_Pro_League',5)
standings_2022 = list(map(lambda x: CODE_DICT[x], standings_2022.club))


# In[10]:


def Club_type(club):
    
    """
    Function takes club as argument and returns
    top 2,top 6 ,mid-table, relagation based on the club 
    finishing position for 2022. If club  was not in 
    the league in 2022 returns default value midtable
    
    """

    if club in standings_2022[0:2] :
        return 'top 2'
   
    if club in standings_2022[2:5] :
        return 'top 6'
    
    if club in standings_2022[5:16] :
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

# In[14]:


def Pre_processing(team,position,country,age,starter):
    """
    takes user inputs as arguments and converts data 
    from long to wide format.Returns a data frame ready to
    used in prediction
    
    """
    global df
    
    df = pd.read_csv(r"C:\Users\Ramya\X_test_be.csv")
    
    df = df.iloc[:,1:] #clean dataframe
    df = df.iloc[0:0]  #drop all data
    df = df.append(pd.Series(0, index=df.columns), ignore_index=True)  # add a row of zero
    
    
    # First catogeries are removed form the catgorical variables when creating dummies
    if team == 'AND':
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

# In[ ]:


CLUBS = ('AND','ATW','BEE','BEV','BRU','CER','CHL','EUP','EXM','GEK','GNT',
         'KOR','LEU','MEC','OOS','SER','SIT','STL','USG','WES','ZUW')

POSITIONS = ('Defender','Midfielder','Foward','Keeper')

COUNTRIES = ('france', 'belgium', 'honduras', 'serbia', 'netherlands',
           'democratic-republic-of-the-congo', 'jamaica', 'united-states',
           'croatia', 'panama', 'austria', 'costa-rica', 'germany',
           'montenegro', 'albania', 'rwanda', 'ghana', 'poland',
           'cote-d-ivoire', 'senegal', 'finland', 'japan', 'mali', 'bulgaria',
           'greece', 'bosnia-herzegovina', 'congo', 'algeria', 'wales',
           'kenya', 'england', 'south-africa', 'hungary', 'tunisia', 'brazil',
           'canada', 'iran', 'togo', 'north-macedonia', 'sweden',
           'madagascar', 'angola', 'nigeria', 'colombia', 'ukraine',
           'uruguay', 'czech-republic', 'guinea-bissau', 'argentina', 'spain',
           'zimbabwe', 'portugal', 'benin', 'cameroon', 'italy', 'australia',
           'denmark', 'norway', 'slovakia', 'georgia', 'the-gambia',
           'comoros', 'scotland', 'burkina-faso', 'trinidad-and-tobago',
           'iceland', 'zambia', 'turkey', 'guinea', 'venezuela', 'israel',
           'haiti', 'sierra-leone', 'south-korea', 'romania', 'cyprus',
           'morocco', 'kosovo', 'switzerland', 'mexico', 'burundi', 'ireland',
           'kazakhstan', 'luxembourg', 'curacao', 'peru', 'Canada',
           'cape-verde', 'ecuador', 'malaysia', 'slovenia', 'jordan',
           'northern-ireland', 'new-zealand', 'bolivia', 'lithuania',
           'armenia', 'thailand', 'tanzania', 'chad', 'malta', 'mauritania',
           'grenada', 'chile', 'guadeloupe', 'russia', 'estonia')


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

