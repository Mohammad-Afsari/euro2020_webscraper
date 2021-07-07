#%%
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

#%%
# -------------------------------------------------------------------------------------------------------------#
# Section 1: Gather and load data
# -------------------------------------------------------------------------------------------------------------#

# URL that's being scraped
# Would work on any of the statistics web pages for any team e.g.
# url = 'https://www.uefa.com/uefaeuro-2020/{CHOSEN TEAM}/statistics/'
url = 'https://www.uefa.com/uefaeuro-2020/teams/35--denmark/statistics/'

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

# Put into string
statistics_table = team_name[0] + ": " + stats[0] + " Matches played: " + stats[1] + " Wins " + stats[2] + " Draw " + stats[3] + " Lost" 


#%%
# -------------------------------------------------------------------------------------------------------------#
# Section 2: Connect to SQL database
# -------------------------------------------------------------------------------------------------------------#

# SSMS connection
driver = 'DRIVER={ODBC Driver 17 for SQL Server}'
server = 'SERVER=tcp:im-test.database.windows.net'
port = 'PORT=1433'
database = 'DATABASE=IM-Test-Database' 
username = 'UID=client_IM' 
password = 'PWD=IM2021LearnSQL'

conn = pyodbc.connect(';'.join([driver,server,port,database,username,password]))
cursor = conn.cursor()

# Execute connection and return results in the table
cursor.execute("SELECT * FROM [IM-Test-Database].[dbo].[Table]") #Confirm SQL table name
print([d[0] for d in cursor.description])
for r in cursor.fetchall():
    print(r)
    
#%%
# -------------------------------------------------------------------------------------------------------------#
# Section 3: Append to SQL database
# -------------------------------------------------------------------------------------------------------------#
# Build SQL string to input into IM Database
author = 'Mohammad Afsari'
sql_string = f'''SET NOCOUNT ON;
IF NOT EXISTS (SELECT * FROM [IM-Test-Database].[dbo].[Table] WHERE CONVERT(varchar,[Author]) = '{author}')
BEGIN 
INSERT INTO [IM-Test-Database].[dbo].[Table] ([Author],[Data])
VALUES ('{author}','{statistics_table}');
END
ELSE
BEGIN
UPDATE [IM-Test-Database].[dbo].[Table] 
SET [Data] = '{statistics_table}'
WHERE CONVERT(varchar,[Author]) = '{author}'
END;
SELECT * FROM [IM-Test-Database].[dbo].[Table];'''
print(sql_string)

cursor.execute(sql_string)
conn.commit()

