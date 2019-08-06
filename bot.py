"""
File name: help_bot.py
Author: Emily Zhong, Eduardo Tapia

Purpose: Main program to run the slackbot to perform emotional and
energy check-ins at CZI
"""

import slack
import ssl as ssl_lib
import certifi
from check_in import CheckIn
import schedule
import time
from settings import SLACK_BOT_TOKEN

# TODO: Connect to actual database. For now just store data in-memory
check_in_sent = {}
def start_checkin(slack_client: slack.WebClient):
    channels = get_dms(slack_client)

    for channel in channels:
        # Create a new check-in
        check_in = CheckIn(channel)

        # Get the check-in message payload
        message = check_in.get_message_payload()

        # Post the check-in message in Slack
        response = slack_client.chat_postMessage(**message)

        # Capture the timestamp of the message we've just posted so
        # we can use it to update the message after a user
        # has completed their check-in responses
        check_in.timestamp = response["ts"]

        # Store the message sent in check_in_sent
        check_in_sent[channel] = check_in

def get_dms(slack_client):
    user_ids = []
    for channel in [{"id": "CM3K9320P"}]: # Just createathon--eebot
        members = slack_client.conversations_members(channel=channel["id"])["members"]
        user_ids.extend(members)

    all_dms = []
    for user in set(user_ids):
        try: # Bypass errors from user_ids that belong to bots
            all_dms.append(slack_client.conversations_open(users=user)["channel"]["id"])
        except:
            continue
    return all_dms

if __name__ == "__main__":
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    slack_token = SLACK_BOT_TOKEN
    slack_client = slack.WebClient(slack_token)

    # schedule.every().day.at("14:00").do(lambda: start_checkin(slack_client, "", all_dms))
    schedule.every(5).seconds.do(lambda: start_checkin(slack_client))

    print("Starting...")
    while True:
        schedule.run_pending()
        time.sleep(5)
    # rtm_client = slack.RTMClient(token=slack_token, ssl=ssl_context)
    # rtm_client.start()
