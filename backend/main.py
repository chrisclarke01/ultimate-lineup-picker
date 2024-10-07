from odds_info import getOdds

def main(players):
    getOdds(players)

if __name__ == '__main__':
    players = []

    while (True):
        playerData = []

        checkComplete = input('Enter anything to continue. Enter COMPLETE when done: ')
        if (checkComplete == "COMPLETE"):
            break
        else:
            playerData.append(input('Enter player name: '))
            playerData.append(input('Enter player position: '))
            playerData.append(input('Enter player team: '))
            players.append(playerData)
    main(players)
