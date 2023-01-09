## Anaylsis of Leagues and Other Tools
The repo contains the work I have done on the Brasilerio A, Serie B, Bundesliga, Belgium first division, Wikipedia scrapping tool and the club transfer
flagging function.

## Content of Folders
Each folder contains a notebook used for modelling, linear model as a pickle file, notebook and script used to define similarity score,
notebook and script of the streamlit webpage.

Additionally if the model is stable enough for aggregate analysis, the folder includes an aggregate analyisis of players in each club of the league.

Brazil folder also contains analysis on the Vasco da Gama squad for 2023, and analysis of the Expat brazilian players in Europe.

## Usage Caveats
The modelling notebook includes a line to export the input table to the local directory, the path needs to be changed when cloned. This table is later 
called in the streamlit webpage notebook to get the schema needed for the input of the model. The path again needs to be changed.

Although the script Web_scrapper_League_table is customised to process and clean league tables from Wikipedia, the processing can be changed to scrap 
any table in Wikipedia
