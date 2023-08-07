import os
import schedule
import time
from dotenv import load_dotenv
import tweepy
from musixmatchapi import get_random_song, clean_track_name, get_lyrics, get_random_lyric

load_dotenv()

def get_twitter_api(): #Get Twitter API keys and access tokens from environment variables
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
    
    client = tweepy.Client(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)
    return client

def post_lyrics_as_tweet():
    Client = get_twitter_api()

    song_info = get_random_song()
    if song_info is None:
        print("No songs were found.")
        return

    track_id, track_name = song_info
    clean_name = clean_track_name(track_name)
    lyrics = get_lyrics(track_id)

    if lyrics is None:
        print(f"Failed to retrieve lyrics for {clean_name}.")
        return

    random_line = get_random_lyric(lyrics)
    if random_line:
        tweet = f"{random_line}"
        try:
            response = Client.create_tweet(text=tweet)
            print(response) 
            print("Tweet posted successfully!")
        except tweepy.error.TweepError as e:  
            print(f"Error posting tweet: {e}")

#due to limited tweets of 1500/month of the free version twitter api, this number should NOT go below 20 minutes
def main():
    schedule.every(30).minutes.do(post_lyrics_as_tweet) 
    while True:
        schedule.run_pending()
        time.sleep(30) #sleep for 30 sec to avoid exceeding rate limits

if __name__ == "__main__":
    main()




