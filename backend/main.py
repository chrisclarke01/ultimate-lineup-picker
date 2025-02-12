from odds_info import getOdds
from flask import Flask, request, jsonify
from flask_cors import CORS

import traceback

app = Flask(__name__)
CORS(app)

@app.route('/api/players', methods=['GET', 'POST'])
def players():
    content = request.json
    try:
        output = main(content)
    except Exception as exception:
        print(traceback.format_exc())
        message = str(exception)
        return {
            'message': message,
            'status': 400,
            'Error': str(exception)
            }, 400
    return output

def main(players):
    response = getOdds(players)
    jsonify(response)
    return response

if __name__ == '__main__':
    app.run(debug=True)
