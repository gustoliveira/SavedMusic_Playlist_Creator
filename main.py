import sys
import spotipy
import spotipy.util as util
import functions

# Define variables for authentication and to get the token
username = "soueunaovc"
scope = 'user-library-read user-library-modify playlist-modify-public playlist-read-private user-read-private'
token = util.prompt_for_user_token(username, scope)

# Closing script if was can't be possible to get the token
if token:
    sp = spotipy.Spotify(auth=token)
    userID = sp.me()['id']
else:
    print("Can't get token for ", username)
    sys.exit()

# Define necessary lists
AllMusicList = []
allPlaylists = []
finalList = []

# Function to read all the playlists and their info
results = sp.current_user_playlists()

# Print all playlist names with identification number
for i in range(results['total']):
    name = results['items'][i]['name']
    allPlaylists.append(name)
    print(i, ' ', name)

# Read identification number of the playlists
qnts = int(input("How many playlists: "))
print("Press their numbers: ")
for i in range(qnts):
    msg = str(i+1) + ': '
    aux = int(input(msg))
    finalList.append(allPlaylists[aux]) # Add the playlist in the list to verify

for i in range(len(finalList)):
    aux = finalList[i]
    for j in range(results['total']):
        if results['items'][j]['name'] == aux:
            name = results['items'][j]['name']
            td = results['items'][j]['tracks']['total']
            playlistID = results['items'][j]['id']

            print("Playlist name: {} ({} Tracks)".format(name.upper(), td))

            # Get all the musics from the playlist
            allMusic = functions.user_playlist_tracks_full(sp, userID, playlistID)
            for j in range(td):
                print('\t', allMusic[j]['track']['name'], ' - ', allMusic[j]['track']['artists'][0]['name'])
                # If the music isn't a in a local file, add in the list
                if allMusic[j]['track']['is_local'] == False:
                    AllMusicList.append(allMusic[j]['track']['id'])

# Function to verify if all the musics on the AllMusicList already is a saved music, if it isn't, add
functions.current_user_saved_tracks_add_list(sp, AllMusicList)

# Function to create a playlist and add all the saved music
functions.create_playlist_with_saved_tracks(sp, userID)
