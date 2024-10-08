import pprint

PLAYER_NAME_INDEX = 0
PLAYER_POSITION_INDEX = 1

MARKET_INDEX = 0
OVER_INDEX = 1
UNDER_INDEX = 2

ODDS_INDEX = 1
LINE_INDEX = 2

# QB Modifiers
PASS_YARD_MODIFIER = 0.04
RUSH_YARD_MODIFIER = 0.1
TD_MODIFIER = 4
INT_MODIFIER = 2

# RB/WR/TE Modifiers
TOTAL_YARDS_MODIFIER = 0.1
RECEPTIONS_MODIFIER = 1

# DST Data Indices

# K Point Modifiers
FIELD_GOAL_MODIFIER = 3
PAT_MODIFIER = 1

def estimatePoints(player):
    playerName = player[PLAYER_NAME_INDEX]
    playerPosition = player[PLAYER_POSITION_INDEX]

    playerPoints = [playerName]

    if playerPosition == 'QB':
        playerPoints.append(inferQbPoints(player))
    elif playerPosition == 'RB' or playerPosition == 'WR' or playerPosition == 'TE':
        playerPoints.append(inferRbWrTePoints(player))
    elif playerPosition == 'DST':
        playerPoints.append(inferDstPoints(player))
    elif playerPosition == 'K':
        playerPoints.append(inferKPoints(player))
    else:
        print('Error: ' + playerPosition + ' is not a known player position.')
        return None
    return playerPoints
    
def inferQbPoints(player):
    totalPoints = 0.0
    for dataPoint in player[4:]:
        line = chooseLineFromOverUnder(dataPoint[OVER_INDEX], dataPoint[UNDER_INDEX])
        if dataPoint[MARKET_INDEX] == 'player_pass_yds':
            totalPoints = totalPoints + (PASS_YARD_MODIFIER * line)
        elif dataPoint[MARKET_INDEX] == 'player_rush_yds':
            totalPoints = totalPoints + (RUSH_YARD_MODIFIER * line)
        elif dataPoint[MARKET_INDEX] == 'player_pass_tds':
            totalPoints = totalPoints + (TD_MODIFIER * line)
        elif dataPoint[MARKET_INDEX] == 'player_pass_interceptions':
            totalPoints = totalPoints - (INT_MODIFIER * line)
    return totalPoints

def inferRbWrTePoints(player):
    totalPoints = 0.0
    for dataPoint in player[4:]:
        line = chooseLineFromOverUnder(dataPoint[OVER_INDEX], dataPoint[UNDER_INDEX])
        if dataPoint[MARKET_INDEX] == 'player_pass_rush_reception_yds':
            totalPoints = totalPoints + (TOTAL_YARDS_MODIFIER * line)
        elif dataPoint[MARKET_INDEX] == 'player_receptions':
            totalPoints = totalPoints + (RECEPTIONS_MODIFIER * line)
    return totalPoints

def inferDstPoints(player):
    totalPoints = 0.0
    for dataPoint in player[4:]:
        line = chooseLineFromOverUnder(dataPoint[OVER_INDEX], dataPoint[UNDER_INDEX])
        if dataPoint[MARKET_INDEX] == 'team_totals':
            if line == 0:
                totalPoints = totalPoints + 5
            elif line >=1 and line <= 6:
                totalPoints = totalPoints + 4
            elif line >= 7 and line <= 13:
                totalPoints = totalPoints + 3
            elif line >= 14 and line <= 17:
                totalPoints = totalPoints + 1
            elif line >= 28 and line <= 34:
                totalPoints = totalPoints - 1
            elif line >= 35 and line <= 45:
                totalPoints = totalPoints - 3
            elif line >= 46:
                totalPoints = totalPoints - 5
    return totalPoints

def inferKPoints(player):
    totalPoints = 0.0
    for dataPoint in player[4:]:
        line = chooseLineFromOverUnder(dataPoint[OVER_INDEX], dataPoint[UNDER_INDEX])
        if dataPoint[MARKET_INDEX] == 'player_field_goals':
            totalPoints = totalPoints + (FIELD_GOAL_MODIFIER * line)
        elif dataPoint[MARKET_INDEX] == 'player_pats':
            totalPoints = totalPoints + (PAT_MODIFIER * line)
    return totalPoints

def chooseLineFromOverUnder(over, under):
    overOdds = int(over[ODDS_INDEX])
    underOdds = int(under[ODDS_INDEX])
    if overOdds == underOdds:
        return over[LINE_INDEX] 
    elif overOdds < underOdds:
        return int(over[LINE_INDEX]) + 0.5
    elif underOdds < overOdds:
        return int(under[LINE_INDEX]) - 0.5