"""
File name: app.py
Author: Eddie Tapia
Date: August 5th, 2019

Purpose: Flask backend for our slackbot
"""

import flask
import json
import datetime
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
        user_id = payload['user']['id']
        user_name = payload['user']['username']
        question_id = payload['actions'][0]['block_id']
        timestamp = float(payload['message']['ts'])
        date = str(datetime.datetime.fromtimestamp(timestamp).date())
        response_value = payload['actions'][0]['value']

        if not user_id in table:
            table[user_id] = {}
        if not question_id in table[user_id]:
            table[user_id][question_id] = {}
        table[user_id][question_id][date] = { "value": response_value }
        print(f"Updated user {user_name}'s data with response {response_value} to question {question_id} on {date}")

        # return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
        return jsonify(success=True)


if __name__ == '__main__':
    app.run()