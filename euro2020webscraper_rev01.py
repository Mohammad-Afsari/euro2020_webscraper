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

# -------------------------------------------------------------------------------------------------------------#
# Section 1: Gather and load data
# -------------------------------------------------------------------------------------------------------------#

# URL that's being scraped
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








