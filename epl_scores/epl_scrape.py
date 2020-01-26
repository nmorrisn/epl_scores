# function to scrape EPL scores given a date
# returns a json object containing matches, teams, scores, and dates
import datetime
import json
import requests
from bs4 import BeautifulSoup

def scrape(date):
    date = datetime.datetime.strptime(date_input, '%Y%M%d')

    if date is None:
        raise ValueError('Invalid date.')

    url = "https://www.espn.com/soccer/fixtures/_/date/" + date_input + "/league/eng.1"
    soup = BeautifulSoup(requests.get(url).text, 'lxml')

    # First grab the dates from the headers above the schedule tables
    schedule_dates = {}
    table_count = 0
    for header in soup.find('div', id='sched-container').find_all('h2', class_='table-caption'):
        header_date = datetime.datetime.strptime(header.text, '%A, %B %d')
        schedule_dates['table' + str(table_count)] = header_date.replace(year=date.year).date()
        table_count += 1

    table = []
    match_table = []
    i = 0
    j = 0
    k = 0
    # Loop through match tables
    for table in soup.find_all('div', class_='responsive-table-wrap'):
        # Loop through table rows
        for row in table.find('tbody').find_all('tr'):
            # Loop through teams in each row
            match = {}
            for team in row.find_all('td'):
                if k == 0:
                    match["date"] = str(schedule_dates['table' + str(i)])
                    match["team1_abbr"] = team.abbr.text
                    match["team1"] = team.span.text
                    if team.find('span', class_='record').a.text == 'v':
                        match["score"] = 'n/a'
                    else:
                        match["score"] = team.find('span', class_='record').a.text
                elif k == 1:
                    match["team2_abbr"] = team.abbr.text
                    match["team2"] = team.find('a', class_='team-name').span.text
                k += 1
            # print("This is table:", i, "row:", j, "team:", k)
            match_table.append(match)
            j += 1
            k = 0
        i += 1
        j = 0
    return json.dumps(match_table)

date_input = input("Enter a date formatted like yyyyMMdd: ")

results = scrape(date_input)

print(results)
