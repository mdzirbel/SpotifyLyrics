# SpotifyLyrics
Fetches lyrics for my currently playing song on spotify and displays it using Tkinter.
The GUI is a simple scroll with the text of the song. It also has a button which toggles between forcing the window to the top and allowing it to be behind other windows.

Uses the Spotify API to get the current song playing on my Spotify account

Then checks for whether there is a file already existing with the lyrics
If there is not, looks for the lyrics on azlyrics.com
If it still can't find it, looks for lyrics on genius.com

It then displays the lyrics in the GUI it creates, and periodically checks for song changes every 5 seconds.

When the song changes, it saves the old song lyrics, including any changes the user made to the lyrics and looks for the next song lyrics

It's not really designed to be used by other people, and it contains my account name hardcoded into it.

![Example screenshot with Stairway to Heaven lyrics](/SpotifyLyrics.png?raw=true "Screenshot")
