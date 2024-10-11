from odds_info import getOdds
from flask import Flask, request
from flask_cors import CORS
import pprint

app = Flask(__name__)
CORS(app)
@app.route('/players', methods=['GET', 'POST'])
def players():
    players = request.data
    pprint.pprint(players)
    return players

def main(players):
    odds = getOdds(players)
    pprint.pprint(odds)

if __name__ == '__main__':
    app.run(debug=True)
