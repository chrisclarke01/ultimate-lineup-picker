import requests
import json
import os

PLAYER_NAME_INDEX = 0
PLAYER_POSITION_INDEX = 1
PLAYER_TEAM_INDEX = 2
GAME_ID_INDEX = 3

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

def getOdds(players):
    url = 'https://api.the-odds-api.com/'
    apiKey = os.environ['ODDS_API_KEY']

    for player in players:
        # Name, position, and team of current player
        playerName = player[PLAYER_NAME_INDEX]
        playerPosition = player[PLAYER_POSITION_INDEX]
        playerTeam = player[PLAYER_TEAM_INDEX]

        gameEventEndpoint = url + '/v4/sports/americanfootball_nfl/events?apiKey=' + apiKey

        try:
            response = requests.get(gameEventEndpoint)

            if response.status_code == 200:
                print('Remaining Requests: ' + response.headers['x-requests-remaining'])
                print('Used Requests: ', response.headers['x-requests-used'])
                json = response.json()

                for game in json:
                    if game['home_team'] == playerTeam or game['away_team'] == playerTeam:
                        player.append(game['id'])
                        print(player)

            lineEndpoint = url + '/v4/sports/americanfootball_nfl/events/' + player[GAME_ID_INDEX] + '/odds?apiKey=' + apiKey + '&regions=us&markets='
            if playerPosition == 'QB':
                lineEndpoint = lineEndpoint + PASS_TDS + ',' + PASS_YARDS + ',' + INTERCEPTIONS
                response = requests.get(lineEndpoint)
                if response.status_code == 200:
                    print(response.json())
            else:
                print('Error: ', response.status_code)
                return None
        except requests.exceptions.RequestException as e:
            print('Error: ', e)
            return None