
import tkinter as tk
from songUtils import getSongLyrics, formatSongName, getSpotipy, formatSongNameForSaveFile
import spotipy

screenSize = (800,600)

config = {
    "forceTop": True
}

def forceTopButtonCallback():

    config["forceTop"] = not config["forceTop"]

    if config["forceTop"]:
        root.wm_attributes("-topmost", True)
        forceTopButton.config(relief=tk.SUNKEN, text="Forcing Top")
    else:
        root.wm_attributes('-topmost', False)
        forceTopButton.config(relief=tk.RAISED, text="Allowing Behind")

def setLyrics(songLyrics):
    global listeningSong, listeningArtist
    lyricsTextBox.delete(1.0, tk.END)
    lyricsTextBox.insert(tk.END, songLyrics)

def getEditedLyrics():
    return lyricsTextBox.get("1.0", tk.END)

def writeLyricsToFile(filename, lyrics):
    file = open(filename, "w")
    file.write(lyrics)

root = tk.Tk()
root.title = "Spotify Lyrics"
root.resizable(0,0)

root.wm_attributes("-topmost", 1)

forceTopButton = tk.Button(root, text="Allow Behind", command=forceTopButtonCallback)
forceTopButton.pack(expand=1,fill=tk.BOTH)

# Add text box and scroll
scrollbar = tk.Scrollbar(root)
lyricsTextBox = tk.Text(root, height=53,width=65)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
lyricsTextBox.pack(side=tk.LEFT, fill=tk.Y)
scrollbar.config(command=lyricsTextBox.yview)
lyricsTextBox.config(yscrollcommand=scrollbar.set)

stillGoing = True

listeningArtist = None
listeningSong = None

sp = getSpotipy()

def main():

    global listeningSong, listeningArtist, prevSong, prevArtist, sp

    try:

        prevSong = listeningSong
        prevArtist = listeningArtist

        userInfo = sp.currently_playing()

        listeningArtist = userInfo["item"]["album"]["artists"][0]["name"]
        listeningSong = userInfo["item"]["name"]

        listeningSong = formatSongName(listeningSong)

    # except TypeError as e:
    #     print(e)
    #     print("problem")
    except spotipy.client.SpotifyException:
        print("Re-Initializing token")
        sp = getSpotipy() # When the access token runs out re-initialize it

    if prevSong != listeningSong and listeningSong: # When the song changes and we are playing a song

        if prevSong:
            filename = formatSongNameForSaveFile(prevSong, prevArtist)
            getNewLyrics = getEditedLyrics()
            writeLyricsToFile(filename, getNewLyrics)

        songLyrics = getSongLyrics(listeningArtist, listeningSong)

        setLyrics(songLyrics)

    root.after(5000, main)

main()
root.mainloop()