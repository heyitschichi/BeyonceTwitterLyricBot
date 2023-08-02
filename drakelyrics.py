import tweepy
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get API credentials from environment variables
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

# Create an OAuthHandler instance
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# Set access token and secret
auth.set_access_token(access_token, access_token_secret)

# Create the API object
api = tweepy.API(auth)
