import os
import requests
import random
from dotenv import load_dotenv # Install the `python-dotenv` library 
random.seed()  # Initialize random seed to prevent repeated songs so often
load_dotenv()

API_KEY = os.getenv("MUSIXMATCH_API_KEY")
def get_api_key():
    if not API_KEY:
        print("Musixmatch API key not found. Make sure you set the MUSIXMATCH_API_KEY environment variable.")
    return API_KEY

#function assures we get the artist we want and artists who are mononymous won't get mixed up with artists of the same name but a diff last name
def get_artist_id_by_name(artist_name): 
    api_key = get_api_key()
    if not api_key:
        print("Musixmatch API key not found. Make sure you set the MUSIXMATCH_API_KEY environment variable.")
        return None

    base_url = "http://api.musixmatch.com/ws/1.1/"

    params = {
        "apikey": api_key,
        "q_artist": artist_name,
    }

    response = requests.get(base_url + "artist.search", params=params)
    data = response.json()
    #print(data)
    if "message" in data and "body" in data["message"] and "artist_list" in data["message"]["body"]:
        artist_list = data["message"]["body"]["artist_list"]

        if not artist_list:
            print(f"Artist '{artist_name}' not found.")
            return None

        #Assuming we want the first artist that matches the name, 9/10 times if its a popular artist it will be the first result
        artist_id = artist_list[0]["artist"]["artist_id"]
        return artist_id

    return None

MAIN_ALBUMS = [ #to prevent remixes/live versions of songs from showing up 
    "Dangerously in Love",
    "B'Day",
    "I Am... Sasha Fierce",
    "4",
    "Beyoncé",
    "Lemonade",
    #"The Lion King: The Gift",
    "Renaissance",
]

def get_random_song_from_main_albums():
    api_key = get_api_key()
    if not api_key:
        print("Musixmatch API key not found. Make sure you set the MUSIXMATCH_API_KEY environment variable.")
        return None

    # Retrieve f_artist_id for the artist you want
    artist_id = get_artist_id_by_name("Beyoncé")
    if not artist_id:
        print("Failed to retrieve the f_artist_id.")
        return None

    base_url = "http://api.musixmatch.com/ws/1.1/"

    # Get the track list from main albums
    params = {
        "apikey": api_key,
        "f_artist_id": artist_id,
        "page_size": 100,
        "s_track_rating": "desc",
    }

    response = requests.get(base_url + "track.search", params=params)
    data = response.json()

    if "message" in data and "body" in data["message"] and "track_list" in data["message"]["body"]:
        track_list = data["message"]["body"]["track_list"]

        if not track_list:
            return None
        
        # Filter tracks from the main albums
        main_album_tracks = [
            track for track in track_list
            if any(album in track["track"]["album_name"] for album in MAIN_ALBUMS)
        ]

        if not main_album_tracks:
            return None

        # Choose a random track from the main album tracks
        random_track = random.choice(main_album_tracks)

        return random_track["track"]["track_id"], random_track["track"]["track_name"]

    return None


def get_lyrics(track_id):
    api_key = get_api_key()
    if not api_key:
        print("Musixmatch API key not found. Make sure you set the MUSIXMATCH_API_KEY environment variable.")
        return None

    base_url = "http://api.musixmatch.com/ws/1.1/"

    params = {
        "apikey": api_key,
        "track_id": track_id,
    }

    response = requests.get(base_url + "track.lyrics.get", params=params)
    data = response.json()

    if "message" in data and "body" in data["message"] and "lyrics" in data["message"]["body"]:
        return data["message"]["body"]["lyrics"]["lyrics_body"]
    
    return None

#this is just personal prefrence, dont **need** this function, although may use it for future uses
def clean_track_name(track_name):  #Check if the track name contains "(feat." or "(With" 
    feat_index = track_name.find("(feat.")
    with_index = track_name.find("(With")

    if feat_index != -1 and with_index != -1:
        #If both "(feat." and "(With" are found, remove everything after the first occurrence
        clean_name = track_name[:min(feat_index, with_index)].strip()
    elif feat_index != -1:
        #If only "(feat." is found, remove everything after it
        clean_name = track_name[:feat_index].strip()
    elif with_index != -1:
        #If only "(With" is found, remove everything after it
        clean_name = track_name[:with_index].strip()
    else:
        #If neither "(feat." nor "(With" is found, keep the original track name
        clean_name = track_name

    return clean_name

def get_random_lyric(lyrics):  #Extract lines from the lyrics and filter out the disclaimer line and lines w/ just three words
    lines = lyrics.split("\n")
    clean_lines = [line.strip() for line in lines if line.strip() != "******* This Lyrics is NOT for Commercial use *******" and "..." not in line.strip() and len(line.strip().split()) > 3]

    if not clean_lines:
        print("No lyrics found.")
        return None

    #Choose a random line from the filtered list
    random_line = random.choice(clean_lines)
    return random_line

def main():
    api_key = get_api_key() #get API key

    if not api_key:
        print("No API key found.")
        return
    
    song_info = get_random_song_from_main_albums()

    if song_info is None:
        print("No songs were found.")
        return

    track_id, track_name = song_info

    clean_name = clean_track_name(track_name) #Clean the track name

    lyrics = get_lyrics(track_id) #Get the lyrics of the chosen song

    if lyrics is None:
        print(f"Failed to retrieve lyrics for {clean_name}.")
        return

    #print(f"Title: {clean_name}\n")  #Debugging purposes
    #print(lyrics)

    random_line = get_random_lyric(lyrics) #Choose a random lyric line (excluding disclaimer line)

    if random_line:
        print(f"{clean_name}:") #Print the name of the song from which the random lyric came
        print(random_line)

if __name__ == "__main__":
    main()