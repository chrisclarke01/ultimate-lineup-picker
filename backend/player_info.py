import nfl_data_py as nfl

def getPlayerInfo():
    playerData = nfl.import_weekly_rosters(2024)
    print(playerData)