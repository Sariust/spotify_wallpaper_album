import json
import requests
import shutil
import os
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth


os.environ['SPOTIPY_CLIENT_ID'] = ''
os.environ['SPOTIPY_CLIENT_SECRET'] = ''
os.environ['SPOTIPY_REDIRECT_URI']='http://example.com'

BASE_URL = 'https://api.spotify.com/v1/'
SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'
scope = "user-read-playback-state"

   


def get_img_url() :

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    
    try: 
        result = sp.current_user_playing_track()

    except requests.ConnectionError:

        while True:
            try: 
                result = sp.current_user_playing_track()
                break
            except:
                time.sleep(10)
                pass

    
    if result!= None :
        return result['item']['album']['images'][0]['url']
    else: return result

def fetch_img(img_url, p1):

    res = requests.get(img_url, stream = True)


    if res.status_code == 200:
        if p1:
            with open('album_cover.jpg','wb') as f:
                shutil.copyfileobj(res.raw, f)
            return os.getcwd()+'/album_cover.jpg'
        else:
            with open('album_cover','wb') as f:
                shutil.copyfileobj(res.raw, f)
            return os.getcwd()+'/album_cover'
    else:
        print('\n\nImage Couldn\'t be retrieved\n\n')
        return None

def main():
    old_img_url= 0
    p1 = True
    i=0
    while True:
        img_url= get_img_url()
        if (img_url != None):
            if  img_url != old_img_url :
                path = fetch_img(img_url, p1)
                command = f"gsettings set org.gnome.desktop.background picture-uri-dark 'file://{path}'"  # type: ignore
                os.system( command )
                print(f'{command}')
                p1= not p1
        else: 
            print('None breaking')
            time.sleep(60)
        print(f'{i} - waiting')
        time.sleep(3)
        i+=1
        old_img_url= img_url

main()

print('ended')
