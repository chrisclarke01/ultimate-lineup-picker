# Player amounts
QB_LIMIT = 1
WR_LIMIT = 2
RB_LIMIT = 2
TE_LIMIT = 1
FLEX_LIMIT = 1
DST_LIMIT = 1
K_LIMIT = 1

def createLineup(estimatedPointsPerPlayer):
    sortedLineUp = []
    
    for i in range(QB_LIMIT):
        sortedLineUp.append(getLargest(estimatedPointsPerPlayer['QB']))
    for i in range(WR_LIMIT):
        sortedLineUp.append(getLargest(estimatedPointsPerPlayer['WR']))
    for i in range(RB_LIMIT):
        sortedLineUp.append(getLargest(estimatedPointsPerPlayer['RB']))
    for i in range(TE_LIMIT):
        sortedLineUp.append(getLargest(estimatedPointsPerPlayer['TE']))
    for i in range(FLEX_LIMIT):
        sortedLineUp.append(getLargest(estimatedPointsPerPlayer['WR'] + estimatedPointsPerPlayer['RB'] + estimatedPointsPerPlayer['TE']))
    for i in range(DST_LIMIT):
        sortedLineUp.append(getLargest(estimatedPointsPerPlayer['DST']))
    for i in range(K_LIMIT):
        sortedLineUp.append(getLargest(estimatedPointsPerPlayer['K']))
    return sortedLineUp

def getLargest(players):
    bestPick = players[0]
    for player in players:
        if player['points'] > bestPick['points']:
            bestPick = player
    players.remove(bestPick)
    return bestPick