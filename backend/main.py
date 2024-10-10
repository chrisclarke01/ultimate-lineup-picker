from odds_info import getOdds
from flask import Flask, jsonify
import pprint

app = Flask(__name__)
@app.route('/players', methods=['GET'])

def players():
    players = {'key': 'value'}
    pprint.pprint(jsonify(players))
    return players

def main(players):
    odds = getOdds(players)
    pprint.pprint(odds)

if __name__ == '__main__':
    app.run(debug=True)
