import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def song_by_lyrics(base_url,access_token,lyrics='hello'):

    endpoint='search'
    param={
        'q':lyrics,
        'access_token':access_token
    }
    response=requests.get(base_url+endpoint, params=param)
    data=response.json()
    if 'response' in data and 'hits' in data['response']:
        hits=data['response']['hits']
        if hits:
            lenofhits=len(hits)
            if lenofhits>2:
                top3songs=[]
                for i in range(3):
                    song = hits[i]['result']
                    complete_song_name=song['title']+" by "+song['primary_artist']['name']
                    top3songs.append(complete_song_name)
                return top3songs
            else:
                song = hits[0]['result']
                complete_song_name = song['title'] + " by " + song['primary_artist']['name']
                return complete_song_name
        else:
            complete_song_name='songnotfound'
            return complete_song_name
    else:
        error_message="API error"
        return error_message

def gettingspotifytracklist(song_name,client_id,client_secret):
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    result=sp.search(song_name,type="track", limit=1)
    if result['tracks']['items']:
        track_id=result['tracks']['items'][0]['id']
    else:
        return None
    track_feature=sp.audio_features([track_id])[0] ### what kind of song is this? whether danceable or not
    recommendation=sp.recommendations(seed_tracks=[track_id],limit=5, **track_feature)
    return recommendation['tracks']


