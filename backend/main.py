from odds_info import getOdds
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/players', methods=['GET', 'POST'])
def players():
    content = request.json
    return main(content)

def main(players):
    response = getOdds(players)
    jsonify(response)
    return response

if __name__ == '__main__':
    app.run(debug=True)
