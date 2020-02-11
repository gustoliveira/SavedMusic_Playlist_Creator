import spotipy

# Define necessary lists
AllMusicList = []
allPlaylists = []
finalList = []

# Get all the musics from one playlist
def user_playlist_tracks_full(sp, user, playlist_id, fields=None, market=None):
    # first run through also retrieves total no of songs in library
    response = sp.user_playlist_tracks(user, playlist_id, fields=fields, limit=100, market=market)
    results = response["items"]

    # subsequently runs until it hits the user-defined limit or has read all songs in the library
    while len(results) < response["total"]:
        response = sp.user_playlist_tracks(user, playlist_id, fields=fields, limit=100, offset=len(results), market=market)
        results.extend(response["items"])

    # Return a list with all the musics
    return results

# Check if all the music in the given list is a saved music
# If it isn't, add to saved musics
def current_user_saved_tracks_add_list(sp, AllMusicList):
    print("Start checking if songs are in saved songs")

    # Create a list, allIDs, and add the ID of only one ID, and check
    # Itn't the fastest way, and is possible check 50 musics at the time
    allIDs = []
    for i in range(len(AllMusicList)):
        print("Checking ", i)
        allIDs.append(AllMusicList[i])
        teste = sp.current_user_saved_tracks_contains(allIDs)
        if teste[0] == False:
            sp.current_user_saved_tracks_add(allIDs)
            print('\tAdded')
        else:
            print('\tChecked')

        allIDs.clear()

    print("All musics on Saved Tracks")

# Print all the saved musics at the console
def current_user_saved_tracks_print_all(sp):
    i = j = 0
    while True:
        results = sp.current_user_saved_tracks(limit=50, offset=i)
        for item in results['items']:
            j += 1
            print(item['track']['name'] + ' - ' + item['track']['artists'][0]['name'])
        if j < 50:
            break
        else:
            i += 50
        j = 0

# Return a list with the ID of all the saved musics
def current_user_saved_tracks_list_all(sp):
    lista = []
    i = j = 0
    while True:
        results = sp.current_user_saved_tracks(limit=50, offset=i)
        for item in results['items']:
            j += 1
            lista.append(item['track']['id'])
        if j < 50:
            break
        else:
            i += 50
        j = 0

    return lista

# Create and add all the saved musics
def create_playlist_with_saved_tracks(sp, userID, name="Saved Tracks"):
    # Create the playlist
    sp.user_playlist_create(userID, name)
    print("Created the 'Saved Tracks' playlist")

    # Find the ID of the new playlist
    results = sp.current_user_playlists()
    for i in range(results['total']):
        if results['items'][i]['name'] == name:
            playlistID = results['items'][i]['id']

    # A list with all the ID of the all saved musics
    AllMusicList = current_user_saved_tracks_list_all(sp)

    allIDs = []

    # Add all the musics, one by one
    # Is possible add 100 at once, but return HTTP ERROR 414 (URI Too Long)
    print("Start adding musics in the new playlist")
    for i in range(len(AllMusicList)):
        allIDs.append(AllMusicList[i])
        sp.user_playlist_add_tracks(userID, playlistID, allIDs)

        allIDs.clear()
        print("Added", i)

    print("Added all saved music to the new playlist")

# Print all playlist names
def show_all_playlists(results):
    for i in range(results['total']):
        name = results['items'][i]['name']
        print(i, ' ', name)

# Print all playlist names with identification number and return a list with then
def show_all_playlists_and_return_a_list(results):
    for i in range(results['total']):
        name = results['items'][i]['name']
        allPlaylists.append(name)
        print(i, ' ', name)
    return allPlaylists

# Read identification number of the playlists
def read_which_playlists(results):
    allPlaylists = show_all_playlists_and_return_a_list(results)
    qnts = int(input("How many playlists: "))
    print("Press their numbers: ")
    for i in range(qnts):
        msg = str(i+1) + ': '
        aux = int(input(msg))
        finalList.append(allPlaylists[aux]) # Add the playlist in the list to verify
    return finalList

def show_all_music_and_return_AllMusicList(results, sp, userID):
    finalList = read_which_playlists(results)
    for i in range(len(finalList)):
        aux = finalList[i]
        for j in range(results['total']):
            if results['items'][j]['name'] == aux:
                name = results['items'][j]['name']
                td = results['items'][j]['tracks']['total']
                playlistID = results['items'][j]['id']

                print("Playlist name: {} ({} Tracks)".format(name.upper(), td))

                # Get all the musics from the playlist
                allMusic = user_playlist_tracks_full(sp, userID, playlistID)
                for j in range(td):
                    print('\t', allMusic[j]['track']['name'], ' - ', allMusic[j]['track']['artists'][0]['name'])
                    # If the music isn't a in a local file, add in the list
                    if allMusic[j]['track']['is_local'] == False:
                        AllMusicList.append(allMusic[j]['track']['id'])
    return AllMusicList
