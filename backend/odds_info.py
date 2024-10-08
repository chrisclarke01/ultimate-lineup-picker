from point_estimator import estimatePoints
import requests
import pprint
import os

PLAYER_NAME_INDEX = 0
PLAYER_POSITION_INDEX = 1
PLAYER_TEAM_INDEX = 2
GAME_ID_INDEX = 3

# QB Markets
PASS_YARDS = 'player_pass_yds'
PASS_TDS = 'player_pass_tds'
INTERCEPTIONS = 'player_pass_interceptions'
RUSH_YARDS = 'player_rush_yds'

# RB/WR/TE Markets
TOTAL_YARDS = 'player_pass_rush_reception_yds'
RECEPTIONS = 'player_receptions'

# D/ST Markets
OPPOSING_TEAM_TOTALS = 'team_totals'

# K Markets
FIELD_GOALS = 'player_field_goals'
EXTRA_POINTS = 'player_pats'

def getOdds(players):
    url = 'https://api.the-odds-api.com/'
    apiKey = os.environ['ODDS_API_KEY']
    estimatedPointsPerPlayer = []

    for player in players:
        # Name, position, and team of current player
        playerName = player[PLAYER_NAME_INDEX]
        playerPosition = player[PLAYER_POSITION_INDEX]
        playerTeam = player[PLAYER_TEAM_INDEX]

        gameEventEndpoint = url + '/v4/sports/americanfootball_nfl/events?apiKey=' + apiKey
        games = hitApi(gameEventEndpoint)
        for game in games:
            if game['home_team'] == playerTeam or game['away_team'] == playerTeam:
                player.append(game['id'])

        propsEndPoint = url + '/v4/sports/americanfootball_nfl/events/' + player[GAME_ID_INDEX] + '/odds?apiKey=' + apiKey + '&regions=us&oddsFormat=american&markets=' + getPropsEndpoint(playerPosition)
        playerProps = hitApi(propsEndPoint)
        playerProps = playerProps['bookmakers'][0]['markets']
        for market in playerProps:
            props = []
            props.append(market['key'])
            for outcome in market['outcomes']:
                pointAndOdds = []
                if playerPosition == 'DST':
                    if outcome['description'] != playerName:
                        pointAndOdds.append(outcome['name'])
                        pointAndOdds.append(outcome['price'])
                        pointAndOdds.append(outcome['point'])
                        props.append(pointAndOdds)
                elif outcome['description'] == playerName:
                    pointAndOdds.append(outcome['name'])
                    pointAndOdds.append(outcome['price'])
                    pointAndOdds.append(outcome['point'])
                    props.append(pointAndOdds)
            player.append(props)
        estimatedPointsPerPlayer.append(estimatePoints(player))
    return estimatedPointsPerPlayer
        
def hitApi(endpoint):
    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            print('Remaining Requests: ' + response.headers['x-requests-remaining'])
            print('Used Requests: ', response.headers['x-requests-used'])
            return response.json()
    except requests.exceptions.RequestException as e:
        print('Error: ', e)
        return None
    
def getPropsEndpoint(playerPosition):
    if playerPosition == 'QB':
        return PASS_YARDS + ',' + RUSH_YARDS + ',' + PASS_TDS + ',' + INTERCEPTIONS
    elif playerPosition == 'RB' or playerPosition == 'WR' or playerPosition == 'TE':
        return TOTAL_YARDS + ',' + RECEPTIONS
    elif playerPosition == 'DST':
        return OPPOSING_TEAM_TOTALS
    elif playerPosition == 'K':
        return FIELD_GOALS + ',' + EXTRA_POINTS
    else:
        print('Error: ' + playerPosition + ' is not a known player position.')
        return None