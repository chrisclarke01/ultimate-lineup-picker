import requests
import os

# Passing Markets
PASS_YARDS = 'player_pass_yds'
PASS_TDS = 'player_pass_tds'
INTERCEPTIONS = 'player_pass_interceptions'

# Rushing Markets
RUSH_YARDS = 'player_rush_yds'

# Receiving Markets
RECEIVING_YARDS = 'player_reception_yds'
RECEPTIONS = 'player_receptions'

# Defensive Markets
OPPOSING_QB_SACKS = 'player_sacks'
OPPOSING_TEAM_TOTALS = 'team_totals'

# Kicking Markets
EXTRA_POINTS = 'player_pats'
FIELD_GOALS = 'player_kicking_points'

# Miscellaneous Markets
TOTAL_TDS = 'player_rush_reception_tds'

def getOdds():
    apiKey = os.environ['ODDS_API_KEY']
    url = 'https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds?apiKey=' + apiKey

    try:
        response = requests.get(url)

        if response.status_code == 200:
            print('Remaining Requests: ' + response.headers['x-requests-remaining'])
            print('Used Requests: ', response.headers['x-requests-used'])
            return response
        else:
            print('Error: ', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error: ', e)
        return None