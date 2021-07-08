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
url = 'https://www.uefa.com/uefaeuro-2020/teams/58837--czech-republic/'

# HTTP request 
html_page  = requests.get(url)

# Parse and format
html = requests.get(url).text
initial_soup = BeautifulSoup(html, 'html.parser')

# Find html class assosiated to the team
team_name = initial_soup.find_all("h1",{"class":"team-name desktop"})
team_name = [i.text for i in team_name]

# Find html class assosiated to the relvant statistics
classes = initial_soup.find("div",{"class":"team--statistics--list col-xs-12"})
stats_arr = []
for i in classes.stripped_strings:
    stats_arr.append(repr(i))

# As the last value only shows 'Cards' we need to specify yellow/red cards
stats_arr[22] = "'Yellow Cards'"
stats_arr.insert(24,"'Red Cards'")

# Split into text string and values
stats_textstr = stats_arr[0::2]
stats_values = stats_arr[1::2]

# Convert into pandas dataframe
stats_textstr = pd.DataFrame({'col': stats_textstr})
stats_values = pd.DataFrame({'col': stats_values})
stats_merge = pd.merge(stats_textstr, stats_values, left_index=True, right_index=True)

# Merge stats together
stats_merge['col_x'] = stats_merge['col_x'].str.replace("'",'')
stats_merge['col_y'] = stats_merge['col_y'].str.replace("'",'')
stats = (stats_merge['col_x'] + "=" + stats_merge['col_y'])
stats = pd.DataFrame({'Statistics':stats})

# loop through stats and add a coma
for i in stats:
    stats_format = ''
    stats_format += stats[i] + ","
    
# Convert to string
stats_list = stats_format.to_list()
stats_str = ''.join(stats_list)
limit = len(stats_str)
statistics = stats_str[:limit - 1]
statistics = team_name[0] + " Euro 2020 statistics: " + statistics


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
VALUES ('{author}','{statistics}');
END
ELSE
BEGIN
UPDATE [IM-Test-Database].[dbo].[Table] 
SET [Data] = '{statistics}'
WHERE CONVERT(varchar,[Author]) = '{author}'
END;
SELECT * FROM [IM-Test-Database].[dbo].[Table];'''
print(sql_string)

cursor.execute(sql_string)
conn.commit()
