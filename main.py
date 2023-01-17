from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# date = input("Which date would you like to travel to (YYYY-MM-DD): ")
date = "1987-08-28"
URL = (f"https://www.billboard.com/charts/hot-100/{date}")

SPOTIFY_ID = "YOUR-SPOTIFY-ID"
SPOTIFY_SECRET = "YOUR.SPOTIFY-SECRET"
REDIRECT_URI = "http://example.com"
SCOPE = "playlist-modify-public"

response = requests.get(URL)
webpage = response.text

soup = BeautifulSoup(webpage, "html.parser")

song_names = soup.find_all(name="h3", id="title-of-a-story", class_="a-no-trucate")
song_list = [song.getText().strip() for song in song_names]

artist_names = soup.find_all(class_="a-no-trucate", name="span")
artist_list = [artist.getText().strip() for artist in artist_names]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=SCOPE,
        redirect_uri=REDIRECT_URI,
        client_id=SPOTIFY_ID,
        client_secret=SPOTIFY_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]

year = (int(date.split("-")[0]))
song_uris = []

for song in song_list:
    song_uri = sp.search(q=f"track: {song} year: {year}", type="track", limit=1)
    try:
        track_uris = song_uri["tracks"]["items"][0]["uri"]
        song_uris.append(track_uris)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")





playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=True)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
