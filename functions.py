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
    # But at a 'random' point, the script broke
    allIDs = []
    for i in range(len(AllMusicList)):
        allIDs.append(AllMusicList[i])
        teste = sp.current_user_saved_tracks_contains(allIDs)
        if teste[0] == False:
            sp.current_user_saved_tracks_add(allIDs)

        print("Checked", i)
        allIDs.clear()

    print("All musics on saved tracks")

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
