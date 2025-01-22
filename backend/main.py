from odds_info import getOdds
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/players', methods=['GET', 'POST'])
def players():
    content = request.json
    try:
        output = main(content)
    except Exception as exception:
        if hasattr(exception, 'message'):
            message = exception.message
        else:
            message = 'New and unknown error: ' + getattr(exception, 'message', repr(exception))
        print(message)
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
