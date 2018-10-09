
import urllib.request
from bs4 import BeautifulSoup
import lyricsgenius as genius
import re
import spotipy
import spotipy.util as util

geniusApi = genius.Genius("fOAZZL8j_hGKIWA5I0LwU5_2NvNVRYl6uuTajYPzkRUI7NUAtDgfyRWwUK0i6kkl")

username = 'matthew.d.zirbel'
scope = 'user-read-currently-playing'
client_id = '9d5a495f8b4d48c9a69b1b6782f86627'
client_secret = "820428b1d67e42fc95ab0d293dcf4c97"
redirect_uri = 'http://localhost:8888/callback/'

def getSpotipy():

    token = util.prompt_for_user_token(
            username=username,
            scope=scope,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri
    )

    global sp
    sp = spotipy.Spotify(auth=token)
    return sp

def getSongLyrics(artist, song):
    try:
        with open(formatSongNameForSaveFile(song, artist), 'r') as songFile:
            songLyrics = songFile.read()
    except FileNotFoundError:
        songLyrics = azlyrics_attempt(artist, song)
        if not songLyrics:
            songLyrics = genius_attempt(artist, song)
        if not songLyrics:
            songLyrics = "Lyrics Not Found :("
        songLyrics = "Listening to " + song + " by " + artist + "\n" + songLyrics

    return songLyrics

# The function immediately below was copy-pasted from elsewhere. Credit to Sagun Shrestha for it.
def azlyrics_attempt(artist, song_title):
    artist = artist.lower()
    song_title = song_title.lower()
    # remove all except alphanumeric characters from artist and song_title
    artist = re.sub("[^A-Za-z0-9]+", "", artist)
    song_title = re.sub("[^A-Za-z0-9]+", "", song_title)
    if artist.startswith("the"):  # remove starting 'the' from artist e.g. the who -> who
        artist = artist[3:]
    url = "http://azlyrics.com/lyrics/" + artist + "/" + song_title + ".html"

    try:
        content = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(content, 'html.parser')
        lyrics = str(soup)
        # lyrics lies between up_partition and down_partition
        up_partition = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'
        down_partition = '<!-- MxM banner -->'
        lyrics = lyrics.split(up_partition)[1]
        lyrics = lyrics.split(down_partition)[0]
        lyrics = reformatLyrics(lyrics)
        return "Lyrics by azlyrics\n\n\n" + lyrics
    except urllib.request.HTTPError:
        return False


# Thanks to johnwmillr for the LyricsGenius API. You can find the API on his github account
def genius_attempt(artist, song):
    try:
        songLyrics = geniusApi.search_song(song, artist, verbose=False).lyrics
    except AttributeError:
        return False
    songLyrics = reformatLyrics(songLyrics)
    return "Lyrics by genius\n\n\n" + songLyrics


def reformatLyrics(lyrics):
    lyrics = lyrics.replace('<br>', '').replace('</br>', '').replace('<br/>', '').replace('</div>', '').replace('<i>', '').replace('</i>', '').strip()
    return lyrics

def formatSongNameForSaveFile(songName, songArtist):
    name = songName + "-" + songArtist
    name = name.replace(" ", "_").strip()
    name = "Saved Songs\\" + name + ".txt"
    return name

def formatSongName(name):

    if name.find("(")>0:
        name = name[:name.find("(")]
        name = name.strip()
    if name.find("[")>0:
        name = name[:name.find("[")]
        name = name.strip()
    if name.find("-")>0:
        name = name[:name.find("-")]
        name = name.strip()
    name.strip()

    return name