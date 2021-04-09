# EPL Score WebScraper
Designed as a python API for scraping current and historical scores from the English Premier League, as well as the future schedule. 

epl_scrape.py can be utilized on its own as a webscraper. The scrape function accepts two parameters, the date in plain text (formatted YYYYmmdd) and a date object. Date validation is handled at the api code level, return an HTTP status of 400 if the date is not valid in the requested format.

The scrape function, places a request to espn.com using the input date and utilizes the BeautifulSoup library to parse the response. It returns a jsonified python list of dictionaries, where each dictionary is a match. An example of a match dictionary is below:

    {
        "date": "2020-02-02",
        "team1_abbr": "TOT",
        "team1": "Tottenham Hotspur",
        "score": "2 - 0",
        "team2_abbr": "MNC",
        "team2": "Manchester City"
    }
    
The score of the match is displayed in the same order as the teams, from left to right. Due to the nature of how ESPN formats their online EPL schedules, the request will always show the requested date and the next 2-3 matchdays. If there are no matches on the requested day, the response will begin with the next matchday.

The web scraper is designed to be utilized with this API to return the results as a JSON object, however it could be used on its own to return EPL score data ad hoc. Constructing this as an API exposes this functionality to be utilized in other open source projects to pull back live and/or historical score data.
