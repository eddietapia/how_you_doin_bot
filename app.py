"""
File name: app.py
Author: Eddie Tapia
Date: August 5th, 2019

Purpose: Flask backend for our slackbot
"""

import flask
from flask import request, jsonify
import json
import datetime
import requests
from settings import SLACK_BOT_TOKEN
from update_db import add_row
from settings import SLACK_BOT_TOKEN


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
slack_token = SLACK_BOT_TOKEN

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


        if payload['actions'][0]['block_id'] == 'feedback':  # Leaving feedback
            # dialog = {
            #     "callback_id": "feedback_response",
            #     "title": "Leave Feedback",
            #     "submit_label": "Submit",
            #     "elements": [{
            #         "label": "Feedback",
            #         "name": "feedback",
            #         "type": "textarea",
            #         "hint": "Let us know how you're feeling!"
            #     }, {
            #         "label": "Associate your feedback with a channel",
            #         "name": "feedback_channel",
            #         "type": "select",
            #         "data_source": "channels"
            #     }]
            # }

            dialog = {
                "callback_id": "ryde-46e2b0",
                "title": "Request a Ride",
                "submit_label": "Request",
                "state": "Limo",
                "elements": [
                    {
                    "type": "text",
                    "label": "Pickup Location",
                    "name": "loc_origin"
                    },
                    {
                    "type": "text",
                    "label": "Dropoff Location",
                    "name": "loc_destination"
                    }
                ]
            }
            response_url = 'https://slack.com/api/dialog.open'
            response_data = { "trigger_id": payload['trigger_id'], "dialog": dialog }
            response_headers = {'Content-type': 'application/json; charset=utf-8', 'Authorization': f"Bearer {AUTH_ACCESS_TOKEN}"}
            response = requests.post(response_url, json.dumps(response_data), headers=response_headers)

        else: # Selecting emotion / energy response
            message_timestamp = float(payload['message']['ts'])
            message_datetime = datetime.datetime.fromtimestamp(message_timestamp)
            action_timestamp = float(payload['actions'][0]['action_ts'])
            action_datetime = datetime.datetime.fromtimestamp(action_timestamp)

            # Should only log event if it's within 24 hours of initial message.
            if ((action_datetime - message_datetime).total_seconds() / 3600) >= 24:
                return abort(400)

            user_id = payload['user']['id']
            question_id = payload['actions'][0]['block_id']
            response_value = payload['actions'][0]['action_id']

            if user_id not in table:
                table[user_id] = {}
            if question_id not in table[user_id]:
                table[user_id][question_id] = {}

            message_date = str(message_datetime.date())
            table[user_id][question_id][message_date] = { "value": response_value }

            user_name = payload['user']['username']
            print(f"Updated user {user_name}'s data with response {response_value} to question {question_id} on {message_date}")

            selected_text = payload['actions'][0]['text']['text']
            response_data = {'text': f':white_check_mark: Marked your response as {selected_text}. Thanks!\n\n', 'replace_original': True}
            response_url = payload['response_url']
            response_headers = {'Content-type': 'application/json'}

            response = requests.post(response_url, json=response_data, headers=response_headers)
        print(response.text)
        # return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
        return jsonify(success=True)

if __name__ == '__main__':
    app.run()
