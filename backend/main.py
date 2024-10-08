from odds_info import getOdds
import pprint

def main(players):
    odds = getOdds(players)
    pprint.pprint(odds)

if __name__ == '__main__':
    players = []

    while (True):
        playerData = []

        checkComplete = input('Enter P to input a player. Enter DST to input a Defense. Enter COMPLETE when done: ')
        if checkComplete == 'COMPLETE':
            break
        elif checkComplete == 'P':
            playerData.append(input('Enter player name: '))
            playerData.append(input('Enter player position: '))
            playerData.append(input('Enter player team: '))
            players.append(playerData)
        elif checkComplete == 'DST':
            teamName = input('Enter team name: ')
            playerData.append(teamName)
            playerData.append('DST')
            playerData.append(teamName)
            players.append(playerData)
    main(players)
