"""
File name: settings.py
Author: Eddie Tapia
Date: August 2nd, 2019

Purpose: used to load the environment variables from our .env file
"""


import os
from dotenv import load_dotenv
load_dotenv(verbose=True)

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
AUTH_ACCESS_TOKEN = os.getenv("0AUTH_ACCESS_TOKEN")