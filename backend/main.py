from odds_info import getOdds

def main(players):
    # Query odds API
    posts = getOdds(players)

    #if posts:
        #print(posts.json())
    #else:
        #print('Failed to fetch posts from API.')

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
