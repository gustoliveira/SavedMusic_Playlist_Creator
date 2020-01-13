import spotipy
import spotipy.util as util
import functions

# export SPOTIPY_CLIENT_ID=''
# export SPOTIPY_CLIENT_SECRET=''
# export SPOTIPY_REDIRECT_URI='https://google.com/'

username = "soueunaovc"
token = util.prompt_for_user_token(username, 'user-library-read user-library-modify playlist-modify-public playlist-read-private user-read-private')
AllMusicList = []

if token:
    sp = spotipy.Spotify(auth=token)

    userID = sp.me()['id']
    results = sp.current_user_playlists()

    allPlaylists = []
    finalList = []

    for i in range(results['total']):
        name = results['items'][i]['name']
        allPlaylists.append(name)
        print(i, ' ', name)

    qnts = int(input("How many playlists: "))
    print("Press their numbers: ")
    for i in range(qnts):
        msg = str(i+1) + ': '
        aux = int(input(msg))
        finalList.append(allPlaylists[aux])

    for i in range(len(finalList)):
        aux = finalList[i]
        for j in range(results['total']):
            if results['items'][j]['name'] == aux:
                name = results['items'][j]['name']
                td = results['items'][j]['tracks']['total']
                playlistID = results['items'][j]['id']

                print("Playlist name: {} ({} Tracks)".format(name.upper(), td))

                allMusic = functions.user_playlist_tracks_full(sp, userID, playlistID)
                for j in range(td):
                    print('\t', allMusic[j]['track']['name'], ' - ', allMusic[j]['track']['artists'][0]['name'])
                    if allMusic[j]['track']['is_local'] == False:
                        AllMusicList.append(allMusic[j]['track']['id'])

    functions.current_user_saved_tracks_add_list(sp, AllMusicList)
    functions.create_playlist_with_saved_tracks(sp, userID)

else:
    print("Can't get token for ", username)

