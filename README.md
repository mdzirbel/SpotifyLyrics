# SpotifyLyrics
Fetches lyrics for my currently playing song on spotify

Uses the Spotify API to get the current song playing on my Spotify account

Then checks for whether there is a file already existing with the lyrics
If there is not, looks for the lyrics on azlyrics.com
If it still can't find it, looks for lyrics on genius.com

It then displays the lyrics in the GUI it creates, and periodically checks for song changes every 5 seconds.

When the song changes, it saves the old song lyrics, including any changes the user made to the lyrics and looks for the next song lyrics
