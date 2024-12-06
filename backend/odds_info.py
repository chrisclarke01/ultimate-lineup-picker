from point_estimator import estimatePoints
from lineup_picker import createLineup
import requests
from datetime import date
import os
import json

# QB Markets
PASS_YARDS = 'player_pass_yds' 
PASS_TDS = 'player_pass_tds'
INTERCEPTIONS = 'player_pass_interceptions'
QB_RUSH_YARDS = 'player_rush_yds'

# RB/WR/TE Markets
RUSH_YARDS = 'player_rush_yds'
RECEIVING_YARDS = 'player_reception_yds'
TOTAL_TDS = 'player_anytime_td'
RECEPTIONS = 'player_receptions'

# D/ST Markets
OPPOSING_TEAM_TOTALS = 'team_totals'

# K Markets
FIELD_GOALS = 'player_field_goals'
EXTRA_POINTS = 'player_pats'

def getOdds(players):
    url = 'https://api.the-odds-api.com/'
    apiKey = os.environ['ODDS_API_KEY']
    usingTestData = players['usingTestData']

    estimatedPointsPerPlayer = {}
    estimatedPointsPerPlayer['QB'] = []
    estimatedPointsPerPlayer['RB'] = []
    estimatedPointsPerPlayer['WR'] = []
    estimatedPointsPerPlayer['TE'] = []
    estimatedPointsPerPlayer['DST'] = []
    estimatedPointsPerPlayer['K'] = []

    for player in players['players']:
        gameEventEndpoint = url + 'v4/sports/americanfootball_nfl/events?apiKey=' + apiKey
        games = hitApi(gameEventEndpoint)
        for game in games:
            if (game['home_team'] == player['team'] or game['away_team'] == player['team']) and isSoonestGame(game['commence_time']):
                player['game_id'] = game['id']

        playerProps = None
        if not usingTestData:
            propsEndPoint = url + 'v4/sports/americanfootball_nfl/events/' + player['game_id'] + '/odds?apiKey=' + apiKey + '&regions=us&oddsFormat=american&markets=' + getPropsEndpoint(player['position'])
            playerProps = hitApi(propsEndPoint)
        else:
            playerProps = json.load(open('testData.json'))

        for bookmaker in playerProps['bookmakers']:
            if bookmaker['markets']:
                playerProps = bookmaker['markets']
                break

        player['props'] = {}

        for market in playerProps:
            props = []
            for outcome in market['outcomes']:
                if player['position'] == 'DST':
                    if outcome['description'] != player['name']:
                        props.append(outcome)
                elif outcome['description'] == player['name']:
                    props.append(outcome)
            player['props'][market['key']] = props
        estimatedPointsPerPlayer[player['position']].append(estimatePoints(player))
    return {
        'player-data': createLineup(estimatedPointsPerPlayer),
        'remaining-requests': getRemainingRequests(gameEventEndpoint)
    }

def isSoonestGame(gameTime):
    ymdTime = gameTime.split('T')[0].split('-')
    currentTime = str(date.today()).split('-')
    t0 = date(int(ymdTime[0]), int(ymdTime[1]), int(ymdTime[2]))
    t1 = date(int(currentTime[0]), int(currentTime[1]), int(currentTime[2]))
    delta = t0 - t1
    return int(delta.days) <= 6
        
def hitApi(endpoint):
    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException as e:
        print('Error: ', e)
        return None
    
def getPropsEndpoint(playerPosition):
    if playerPosition == 'QB':
        return PASS_YARDS + ',' + QB_RUSH_YARDS + ',' + PASS_TDS + ',' + INTERCEPTIONS
    elif playerPosition == 'RB' or playerPosition == 'WR' or playerPosition == 'TE':
        return RUSH_YARDS + ',' + TOTAL_TDS + ',' + RECEIVING_YARDS + ',' + RECEPTIONS
    elif playerPosition == 'DST':
        return OPPOSING_TEAM_TOTALS
    elif playerPosition == 'K':
        return FIELD_GOALS + ',' + EXTRA_POINTS
    else:
        print('Error: ' + playerPosition + ' is not a known player position.')
        return None
    
def getRemainingRequests(endpoint):
    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            return response.headers['x-requests-remaining']
    except requests.exceptions.RequestException as e:
        print('Error: ', e)
        return None