# Player amounts
QB_LIMIT = 1
WR_LIMIT = 2
RB_LIMIT = 2
TE_LIMIT = 1
FLEX_LIMIT = 1
DST_LIMIT = 1
K_LIMIT = 1

def createLineup(estimatedPointsPerPlayer):
    sortedLineUp = {}
    sortedLineUp['QB'] = []
    sortedLineUp['RB'] = []
    sortedLineUp['WR'] = []
    sortedLineUp['TE'] = []
    sortedLineUp['FLEX'] = []
    sortedLineUp['DST'] = []
    sortedLineUp['K'] = []

    for i in range(QB_LIMIT):
        sortedLineUp['QB'].append(getLargest(estimatedPointsPerPlayer['QB']))
    for i in range(WR_LIMIT):
        sortedLineUp['WR'].append(getLargest(estimatedPointsPerPlayer['WR']))
    for i in range(RB_LIMIT):
        sortedLineUp['RB'].append(getLargest(estimatedPointsPerPlayer['RB']))
    for i in range(TE_LIMIT):
        sortedLineUp['TE'].append(getLargest(estimatedPointsPerPlayer['TE']))
    for i in range(FLEX_LIMIT):
        sortedLineUp['FLEX'].append(getLargest(estimatedPointsPerPlayer['WR'] + estimatedPointsPerPlayer['RB'] + estimatedPointsPerPlayer['TE']))
    for i in range(DST_LIMIT):
        sortedLineUp['DST'].append(getLargest(estimatedPointsPerPlayer['DST']))
    for i in range(K_LIMIT):
        sortedLineUp['K'].append(getLargest(estimatedPointsPerPlayer['K']))
    return sortedLineUp

def getLargest(players):
    bestPick = players[0]
    for player in players:
        if player[1] > bestPick[1]:
            bestPick = player
    players.remove(bestPick)
    return bestPick