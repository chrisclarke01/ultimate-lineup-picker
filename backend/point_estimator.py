import pprint

# QB Modifiers
PASS_YARD_MODIFIER = 0.04
RUSH_YARD_MODIFIER = 0.1
PASS_TD_MODIFIER = 4
INT_MODIFIER = 2

# RB/WR/TE Modifiers
TOTAL_YARDS_MODIFIER = 0.1
RECEPTIONS_MODIFIER = 1
TD_MODIFIER = 6

# DST Point Modifiers

# K Point Modifiers
FIELD_GOAL_MODIFIER = 3
PAT_MODIFIER = 1

def estimatePoints(player):
    playerPoints = {'name':player['name'], 'position':player['position']}

    if player['position'] == 'QB':
        playerPoints['points'] = inferQbPoints(player)
    elif player['position'] == 'RB' or player['position'] == 'WR' or player['position'] == 'TE':
        playerPoints['points'] = inferRbWrTePoints(player)
    elif player['position'] == 'DST':
        playerPoints['points'] = inferDstPoints(player)
    elif player['position'] == 'K':
        playerPoints['points'] = inferKPoints(player)
    else:
        print('Error: ' + player['name'] + ' is not a known player position.')
        return None
    return playerPoints
    
def inferQbPoints(player):
    totalPoints = 0.0
    for prop, dataPoint in player['props'].items():
        if prop == 'player_pass_yds' or prop == 'player_pass_yds' or prop == 'player_pass_tds' or prop == 'player_pass_interceptions':
            line = chooseLineFromOverUnder(dataPoint)
            if prop == 'player_pass_yds':
                totalPoints = totalPoints + (PASS_YARD_MODIFIER * line)
            elif prop == 'player_rush_yds':
                totalPoints = totalPoints + (RUSH_YARD_MODIFIER * line)
            elif prop == 'player_pass_tds':
                totalPoints = totalPoints + (PASS_TD_MODIFIER * line)
            elif prop == 'player_pass_interceptions':
                totalPoints = totalPoints - (INT_MODIFIER * line)
    return totalPoints

def inferRbWrTePoints(player):
    totalPoints = 0.0
    for prop, dataPoint in player['props'].items():
        if prop == 'player_anytime_td':
            line = chooseLineFromAnyTimeTd(dataPoint)
            totalPoints = totalPoints + (TD_MODIFIER * line)
        elif prop == 'player_reception_yds' or prop == 'player_rush_yds' or prop == 'player_receptions':
            line = chooseLineFromOverUnder(dataPoint)
            if prop == 'player_reception_yds' or prop == 'player_rush_yds':
                totalPoints = totalPoints + (TOTAL_YARDS_MODIFIER * line)
            elif prop == 'player_receptions':
                totalPoints = totalPoints + (RECEPTIONS_MODIFIER * line)
    return totalPoints

def inferDstPoints(player):
    totalPoints = 0.0
    for prop, dataPoint in player['props'].items():
        if prop == 'team_totals':
            line = chooseLineFromTeamTotals(dataPoint)
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
    for prop, dataPoint in player['props'].items():
        if prop == 'player_field_goals' or prop == 'player_pats':
            line = chooseLineFromOverUnder(dataPoint)
            if prop == 'player_field_goals':
                totalPoints = totalPoints + (FIELD_GOAL_MODIFIER * line)
            elif prop == 'player_pats':
                totalPoints = totalPoints + (PAT_MODIFIER * line)
    return totalPoints

def chooseLineFromOverUnder(dataPoint):
    if dataPoint == None or not dataPoint:
        return 0
    else:
        over = None
        under = None
        for line in dataPoint:
            if line['name'] == 'Over':
                over = line
            elif line['name'] == 'Under':
                under = line
        
        if over['price'] == under['price']:
            return float(over['point'])
        elif over['price'] < under['price']:
            return float(over['point']) + 0.5
        elif under['price'] < over['price']:
            return float(under['point']) - 0.5
    
def chooseLineFromAnyTimeTd(dataPoint):
    if dataPoint == None or not dataPoint:
        return 0
    else:
        if float(dataPoint[0]['price']) < 135:
            return 1
        else:
            return 0
        
def chooseLineFromTeamTotals(dataPoint):
    if dataPoint == None or not dataPoint:
        return 0
    else:
        closestLine = None
        prices = []
        for line in dataPoint:
            prices.append(line['price'])
        def difference(givenList):
            return abs(givenList - 100)
        closestLine = min(prices, key=difference)
        for line in dataPoint:
            if line['price'] == closestLine:
                if line['name'] == 'Under':
                    return float(line['point']) - 0.5
                elif line['name'] == 'Over':
                    return float(line['point']) + 0.5