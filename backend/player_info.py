import requests
import os

def getPlayerInfo():
    url = 'https://nfl-api-data.p.rapidapi.com/nfl-ath-statistics'
    apiKey = os.environ['PLAYER_DATA_API_KEY']

    try:
        response = requests.get(
            url,
            headers = {
	            'x-rapidapi-key': apiKey,
	            'x-rapidapi-host': 'nfl-api-data.p.rapidapi.com'
            }
        )

        if response.status_code == 200:
            print('Remaining Requests: ' + response.headers['x-ratelimit-requests-remaining'])
            return response
        else:
            print('Error: ', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error: ', e)
        return None