"""
File name: app.py
Author: Eddie Tapia
Date: August 5th, 2019

Purpose: Flask backend for our slackbot
"""

import flask
import json
from flask import request, jsonify

# Create our test data
table = {
    # Emily
    'UJKQZ1J4R': {
        'emotion': {
            '08-03-2019': {
                'value': 3,
            },
            '08-04-2019': {
                'value': 5,
            }
        },
        'energy': {
           '08-03-2019': {
                'value': 2,
            },
            '08-04-2019': {
                'value': 3,
            } 
        }
    },
    # Eddie
    'UJENTFZ7C': {
        'emotion': {
            '08-03-2019': {
                'value': 3,
            },
            '08-04-2019': {
                'value': 5,
            }
        },
        'energy': {
           '08-03-2019': {
                'value': 3,
            },
            '08-04-2019': {
                'value': 1,
            } 
        }
    }
}

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>How you doin' slackbot!</h1>"

@app.route('/api/v1/users', methods=['GET', 'POST'])
def api_all():
    if request.method == 'GET':
        # Check if an ID was provided as part of the URL
        if 'id' in request.args:
            id = int(request.args['id'])
        else:
            return "Error: No id field provided. Please specify an id."
        # Create an empty list for our results
        results = []
        for user in table:
            if user['id'] == id:
                results.append(user)
        return jsonify(results)
    elif request.method == 'POST':
        payload = json.loads(request.form['payload'])
        print(payload)
        # return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
        return jsonify(success=True)


if __name__ == '__main__':
    app.run()