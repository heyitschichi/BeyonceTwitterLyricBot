import time
from requests_oauthlib import OAuth1Session
import os
import random
import sys
from musixmatchapi import get_random_song_from_main_albums, get_lyrics

# Set your consumer key and consumer secret
consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")

# Set your existing access token and access token secret
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

# OAuth 1.0a authentication using existing tokens
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

def tweet_random_lyric():
    # Get a random song and its lyrics
    song_info = get_random_song_from_main_albums()
    if song_info is None:
        print("No songs were found.")
        return

    track_id, track_name = song_info
    lyrics = get_lyrics(track_id)
    if lyrics is None:
        print("Failed to retrieve lyrics.")
        return

    # Select a random line from the lyrics
    lines = lyrics.split("\n")
    random_line = random.choice(lines)

    tweet_text = f"{random_line}"

    # Make the request
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json={"text": tweet_text},
    )

    if response.status_code != 201:
        print("Request returned an error:", response.status_code, response.text)
        return

    print("Tweeted:", tweet_text)
    return tweet_text

def main():
    while True:
        tweet_random_lyric()
        # Wait for 30 minutes before tweeting again
        time.sleep(1 * 60)
        
        sys.exit(tweet_random_lyric())

if __name__ == "__main__":
    main()










