# -------------------------------------------------------------------------------------------------------------#
# Introduction: Euro 2020 statistics scraper
# -------------------------------------------------------------------------------------------------------------#
# Designer: Mohammad Afsari
# Checker:
# Description: - Scrape data for a team in the Euro 2020 championship
#              - Push data into relevant database
# -------------------------------------------------------------------------------------------------------------#
# Section 0: Import Libraries
# -------------------------------------------------------------------------------------------------------------#

from bs4 import BeautifulSoup
import requests
import pandas as pd
import pyodbc

# -------------------------------------------------------------------------------------------------------------#
# Section 1: Gather and load data
# -------------------------------------------------------------------------------------------------------------#

# URL that's being scraped
# Would work on any of the statistics web pages for any team e.g.
# url = 'https://www.uefa.com/uefaeuro-2020/{CHOSEN TEAM}/statistics/'
url = 'https://www.uefa.com/uefaeuro-2020/teams/58837--czech-republic/statistics/'

# HTTP request 
html_page  = requests.get(url)

# Parse and format
html = requests.get(url).text
initial_soup = BeautifulSoup(html, 'html.parser')

# Find html class assosiated to the team
team_name = initial_soup.find_all("h1",{"class":"team-name desktop"})
team_name = [i.text for i in team_name]

# Find html class assosiated to the relvant statistics and push to pandas dataframe
classes = initial_soup.find_all("div",{"class":"statistics--list--data"})
classes = [i.text for i in classes]

# Extract relevant statistics
matches_played = pd.Series(classes[0]).to_frame()
won = pd.Series(classes[1]).to_frame()
drawn = pd.Series(classes[2]).to_frame()
lost = pd.Series(classes[3]).to_frame()

# Combine statis into an array
stats = [matches_played[0][0], won[0][0], drawn[0][0], lost[0][0]]

# Put into dictionary
statistics_table = {
        team_name[0]: stats[0] + " Matches: " + stats[1] + " Wins " + stats[2] + " Draw " + stats[3] + " Lost"
        }

# -------------------------------------------------------------------------------------------------------------#
# Section 2: Connect to SQL database
# -------------------------------------------------------------------------------------------------------------#

# SSMS connection
SERVER = 'tcp:im-test.database.windows.net'
DB = 'IM-Test-Database'
UID = 'client-IM'
PWD = 'IM2021LearnSQL'
# Create connection to SSMS
sql_conn = pyodbc.connect(("Trusted_Connection=yes;" +
                            "DRIVER={ODBC Driver 17 for SQL Server};" +
                           "SERVER="+SERVER+";" +
                           "Port=1433" +
                           "DATABASE="+DB+";" +
                           "UID="+UID+";" +
                           "PWD="+PWD
                           ))


# Create an empty array to append into and execute table required from SSMS
rawData = []
cursor = sql_conn.cursor()
cursor.execute("SELECT * FROM [dbo].[Table]") #Confirm SQL table name

# -------------------------------------------------------------------------------------------------------------#
# Section 3: Append to SQL database
# -------------------------------------------------------------------------------------------------------------#







