## __Description__

A simple _Python_ script that runs with _Spotipy_, that read a set of a choosen playlists in Spotify, add all the musics in the Saved Tracks Library and create a Playlist with all the musics included in Saved Tracks.

## __Motivation__

I found [spotify-downloader](https://github.com/ritiek/spotify-downloader) on Github, a program that takes a link from a song on Spotify, downloads it from YouTube and applies metadata and album art. for the information given by the API. There is an option, by linking a playlist, to create a .txt file with all links to the songs in the playlist, and to download all.
But the Saved Tracks library doesn't contain a proper link, so it's impossible to use the program easily without creating and adding all the songs manually, so I made this script to automate this task.

## __Requirements__

* Python3
* Pip3
* Spotipy
* Spotify credentials

### Spotipy

```{bash}
pip3 install spotipy
```

### Spotify credentials

* __Step 1__: Go to the [Spotify for developers site](https://developer.spotify.com/) and log in with your account in the Dashboard area.

* __Step 2__: In the same area, go to the __CREATE CLIENTE ID__, and create the ID. Note this is not for commercial integration.

* __Step 3__: You will be lead to your aplication area, go to __EDIT SETTING__ and in __Redirect URIs__ add __https://google.com/__ and save.

* __Step 4__: Copy the __Client ID__ and __Client Scret__

## __Settings__

As stated in the Spotipy documentation, all methods require user authorization.
Spotipy offers the ```util.prompt_for_user_token ```method for authentication and there are two ways to use it:

* __Putting your credentials directly into the method as arguments:__

```
util.prompt_for_user_token(username,scope,client_id='your-spotify-client-id',client_secret='your-spotify-client-secret',redirect_uri='your-app-redirect-url')
```

* __Set environment variables:__

```{bash}
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='https://google.com/'
```

## __Running__

* __Step 1__: Run _main.py_:
```{bash}
python3 main.py
```

* __Step 2__: Print in the terminal your Spotify username

* __Step 3__: You will be lead to your browser,give the permition and copy the link

* __Step 4__: Paste the link as said in the terminal and the program will start
