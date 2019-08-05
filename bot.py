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
from settings import SLACK_BOT_TOKEN

# TODO: Connect to actual database. For now just store data in-memory
check_in_sent = {}


def start_onboarding(web_client: slack.WebClient, user_id: str, channel: str):
    # Create a new check-in
    check_in = CheckIn(channel)

    # Get the check-in message payload
    message = check_in.get_message_payload()

    # Post the check-in message in Slack
    response = web_client.chat_postMessage(**message)

    # Capture the timestamp of the message we've just posted so
    # we can use it to update the message after a user
    # has completed their check-in responses
    check_in.timestamp = response["ts"]

    # Store the message sent in check_in_sent
    if channel not in check_in_sent:
        check_in_sent[channel] = {}
    check_in_sent[channel][user_id] = check_in

# ============== Message Events ============= #
# When a user sends a DM, the event type will be 'message'.
# Here we'll link the update_share callback to the 'message' event.
@slack.RTMClient.run_on(event="message")
def message(**payload):
    """Display the check-in message after receiving a message
    that contains "hello".
    """
    data = payload["data"]
    web_client = payload["web_client"]
    channel_id = data.get("channel")
    user_id = data.get("user")
    text = data.get("text")
    print("Entering message!!!!!!!")
    print('Text', text)
    if text and "hello" in text.lower():
        print("HELLO")
        return start_onboarding(web_client, user_id, channel_id)


if __name__ == "__main__":
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    slack_token = SLACK_BOT_TOKEN
    rtm_client = slack.RTMClient(token=slack_token, ssl=ssl_context)
    print("Starting to listen to messages...")
    rtm_client.start()
