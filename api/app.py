"""
File name: app.py
Author: Eddie Tapia
Date: August 5th, 2019

Purpose: Flask backend for our slackbot
"""

import flask
from flask import request, jsonify

# Create our test data
table = [
    {
        'id': 0,
        'responses': {
            'emotion': [5],
            'energy': [3],
            'timestamp': ['2019-08-05T13:49:49.684219'],
        }
    },
    {
        'id': 1,
        'responses': {
            'emotion': [5],
            'energy': [3],
            'timestamp': ['2019-08-05T13:50:23.935981'],
        }
    },
]

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
        print('TODO. Send something back')
        print(request.form)


app.run()