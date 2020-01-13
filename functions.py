def user_playlist_tracks_full(sp, user, playlist_id, fields=None, market=None):
    # first run through also retrieves total no of songs in library
    response = sp.user_playlist_tracks(user, playlist_id, fields=fields, limit=100, market=market)
    results = response["items"]

    # subsequently runs until it hits the user-defined limit or has read all songs in the library
    while len(results) < response["total"]:
        response = sp.user_playlist_tracks(user, playlist_id, fields=fields, limit=100, offset=len(results), market=market)
        results.extend(response["items"])
    return results

def current_user_saved_tracks_add_list(sp, AllMusicList):
    print("Start checking if songs are in saved songs")
    allIDs = []

    for i in range(len(AllMusicList)):
        allIDs.append(AllMusicList[i])
        teste = sp.current_user_saved_tracks_contains(allIDs)
        if teste[0] == False:
            sp.current_user_saved_tracks_add(allIDs)

        print("Checked", i)
        allIDs.clear()

    print("All musics on saved tracks")

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

def create_playlist_with_saved_tracks(sp, userID, name="Saved Tracks"):
    sp.user_playlist_create(userID, name)
    print("Created the 'Saved Tracks' playlist")

    results = sp.current_user_playlists()

    for i in range(results['total']):
        if results['items'][i]['name'] == name:
            playlistID = results['items'][i]['id']

    AllMusicList = current_user_saved_tracks_list_all(sp)

    allIDs = []

    print("Start adding musics in the new playlist")
    for i in range(len(AllMusicList)):
        allIDs.append(AllMusicList[i])
        sp.user_playlist_add_tracks(userID, playlistID, allIDs)

        allIDs.clear()
        print("Added", i)

    print("Added all saved music to the new playlist")
