import sys
import spotipy
import spotipy.util as util
import functions

username = str(input("Press your Spotify username: "))

# Define variables for authentication and to get the token
scope = 'user-library-read user-library-modify playlist-modify-public playlist-read-private user-read-private'
token = util.prompt_for_user_token(username, scope)

# Closing script if was can't be possible to get the token
if token:
    sp = spotipy.Spotify(auth=token)
    userID = sp.me()['id']
else:
    print("Can't get token for ", username)
    sys.exit()

# Function to read all the playlists and their info
results = sp.current_user_playlists()

while True:
    print('\nOptions: ')
    print('\t0 - Quit')
    print('\t1 - Show all playlists')
    print('\t2 - Add songs from a playlist to the Saved Musics library')
    print('\t3 - Create a playlist and add songs from the Saved Musics library')
    print('\t4 - Take repeated songs from Saved Musics')
    print('\t5 - Remove all songs from a given playlist from the Saved Musics library')
    option = input('\nEnter the code of the chosen option: ')

    try:
        option = int(option)
    except ValueError:
        print('Enter a valid number for the option')
        continue

    if(option == 0):
        print("Thanks for using =)")
        sys.exit()
    elif(option == 1):
        functions.show_all_playlists(results)
    elif(option == 2):
        AllMusicsList = functions.show_all_music_and_return_AllMusicList(results, sp, userID)
        functions.current_user_saved_tracks_add_list(sp, AllMusicsList)
    elif(option == 3):
        AllMusicsList = functions.show_all_music_and_return_AllMusicList(results, sp, userID)
        functions.current_user_saved_tracks_add_list(sp, AllMusicsList)
        functions.create_playlist_with_saved_tracks(sp, userID)
    elif(option == 4):
        print('In development... \nEnter another option')
        continue
    elif(option == 5):
        AllMusicsList = functions.show_all_music_and_return_AllMusicList(results, sp, userID)
        functions.current_user_saved_tracks_remove_list(sp, AllMusicsList)
    else:
        print('The option entered is not valid... \nEnter another option')
        continue
