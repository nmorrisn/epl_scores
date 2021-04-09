# function to scrape EPL scores given a date
# returns a json object containing matches, teams, scores, and dates
import requests
import datetime
from bs4 import BeautifulSoup
import json

def scrape(date_str, date):
    url = "https://www.espn.com/soccer/fixtures/_/date/" + date_str + "/league/eng.1"
    soup = BeautifulSoup(requests.get(url).text, 'lxml')

    # First grab the dates from the headers above the schedule tables
    schedule_dates = {}
    table_count = 0
    for header in soup.find('div', id='sched-container').find_all('h2', class_='table-caption'):
        header_date = datetime.datetime.strptime(header.text, '%A, %B %d')
        schedule_dates['table' + str(table_count)] = header_date.replace(year=date.year).date()
        table_count += 1

    match_table = []
    i = 0
    j = 0
    # Loop through match tables
    for table in soup.find_all('div', class_='responsive-table-wrap'):
        # Loop through table rows
        match_date = str(schedule_dates['table' + str(i)])
        for row in table.find('tbody').find_all('tr'):
            # Create our match dictionary
            match = {}
            teams = row.find_all('td')

            # Get team 1 information, based on the current html layout this will be index 0
            match["date"] = match_date
            match["team1_abbr"] = teams[0].abbr.text
            match["team1"] = teams[0].span.text
            if teams[0].find('span', class_='record').a.text == 'v':
                match["score"] = 'n/a'
            else:
                match["score"] = teams[0].find('span', class_='record').a.text
            
            # Get second team information
            match["team2_abbr"] = teams[1].abbr.text
            match["team2"] = teams[1].find('a', class_='team-name').span.text
            match_table.append(match)
            j += 1
        i += 1
        j = 0
    
    return json.dumps(match_table)