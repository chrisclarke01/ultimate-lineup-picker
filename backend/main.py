from odds_info import getOdds
from player_info import getPlayerInfo

def main():
    # Query odds API
    posts = getOdds()

    # If successful, print results, and request information
    # Later, this is where algorithm execution will begin
    if posts:
        print(posts.json())
    else:
        print('Failed to fetch posts from API.')

if __name__ == '__main__':
    # Intake players from command line.
    # Later, this will be passed in from the frontend
    players = []
    while (True):
        player = input("Input players on team. Type COMPLETE when all players are entered: ")
        if (player == "COMPLETE"):
            break
        else:
            players.append(player)

    print('\nYour team:')
    for player in players:
            print(player)
    #main()
