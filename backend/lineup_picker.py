def createLineup(playerLimits, estimatedPointsPerPlayer):    
    QB_LIMIT = int(playerLimits['qb'])
    WR_LIMIT = int(playerLimits['rb'])
    RB_LIMIT = int(playerLimits['wr'])
    TE_LIMIT = int(playerLimits['te'])
    FLEX_LIMIT = int(playerLimits['flex'])
    DST_LIMIT = int(playerLimits['dst'])
    K_LIMIT = int(playerLimits['k'])
    
    sortedLineUp = []
    
    for i in range(QB_LIMIT):
        sortedLineUp.append(getLargest(estimatedPointsPerPlayer['QB']))
    for i in range(WR_LIMIT):
        sortedLineUp.append(getLargest(estimatedPointsPerPlayer['WR']))
    for i in range(RB_LIMIT):
        sortedLineUp.append(getLargest(estimatedPointsPerPlayer['RB']))
    for i in range(TE_LIMIT):
        sortedLineUp.append(getLargest(estimatedPointsPerPlayer['TE']))
    flexPlayers = estimatedPointsPerPlayer['WR'] + estimatedPointsPerPlayer['RB'] + estimatedPointsPerPlayer['TE']
    for i in range(FLEX_LIMIT):
        sortedLineUp.append(getLargest(flexPlayers))
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