# playlist_generator_app.py
import streamlit as st
from user_defined_functions import song_by_lyrics,gettingspotifytracklist,getting_howifeel_playlist
from emotonalanalysis import emotional_analysis
from passwordsandkeys import password
import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyOAuth

###### Spotify API credentials
CLIENT_ID,CLIENT_SECRET,REDIRECT_URI= password('Spotify')

### Genius app credentials
Client_id,client_secret_key,client_access_token,base_url=password('Genius')

count=0
# Set up Spotify authentication
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
#                                                client_secret=CLIENT_SECRET,
#                                                redirect_uri=REDIRECT_URI,
#                                                scope="playlist-modify-public"))

# Streamlit app
st.title("Playlist Generator App")

# st.write("How do you want to create playist today?")

decider=st.selectbox("How do you want to create playlist today?",["Based on how you feel?", "Based on song lyrics"],key="key1")

if decider !="Based on how you feel?":
    if decider=="Based on song lyrics":
        song_lyrics=st.text_input("Enter the song lyrics you remembered:",key=count)
        if song_lyrics=="" or song_lyrics is None:
            st.warning("Please give input")
        else:
            the_song_name=song_by_lyrics(base_url,client_access_token,song_lyrics)
            st.write("The song name is:", the_song_name)
            satisfiedinput=st.radio("Is this your song:",['N','Y'])
            if satisfiedinput=="N":
                st.write("Give more proper name of the song or might add more details about singer")
            else:
                if type(the_song_name)==list:
                    index=st.number_input("On which song you want to get the recommendation:",  step=1,value=None)
                    if index is None or index=="":
                        st.warning("type the number associated with the song name for getting playlist")
                    else:
                        st.write(index)
                        recommendations=gettingspotifytracklist(the_song_name[index], CLIENT_ID, CLIENT_SECRET)
                        st.write("here is your recommendation")
                        for i, recommendation in enumerate(recommendations,1):
                            st.write(i," ",recommendation['name']," by",recommendation['artists'][0]['name']," here is the link: ", recommendation['external_urls']['spotify'])
                else:
                    recommendations = gettingspotifytracklist(the_song_name, CLIENT_ID, CLIENT_SECRET)
                    st.write("here is your recommendation")
                    for i, recommendation in enumerate(recommendations, 1):
                        st.write(i, " ", recommendation['name'], " by", recommendation['artists'][0]['name'],
                                 " here is the link: ", recommendation['external_urls']['spotify'])
elif decider=="Based on how you feel?":
    how_i_feel=st.text_input("enter your prompt",key=count+3)
    if how_i_feel=="" or how_i_feel is None:
        st.warning("Please give input")
    else:
        emotions=emotional_analysis(how_i_feel)
        if emotions==0:
            st.write("Sorry no recommendation i have to learn more.")
        else:
            genre_mappings = {
                'joy': ['happy', 'dance', 'pop', 'funk', 'disco', 'jazz', 'reggae', 'soul'],
                'sadness': ['acoustic', 'blues', 'emo', 'indie', 'sad', 'soul'],
                'love': ['romance', 'pop', 'indie-pop', 'R&B', 'soul', 'singer-songwriter'],
                'anger': ['metal', 'rock', 'punk', 'hardcore', 'heavy-metal'],
                'fear': ['ambient', 'electronic', 'dark', 'industrial', 'experimental']
            }
            gen=np.random.randint(0, len(genre_mappings[emotions]))
            # st.write(emotions)

            recommendations=getting_howifeel_playlist(genre_mappings[emotions][gen],CLIENT_ID, CLIENT_SECRET)
            st.write("here is your recommendation")
            for i, recommendation in enumerate(recommendations, 1):
                st.write(i, " ", recommendation['name'], " by", recommendation['artists'][0]['name'],
                         " here is the link: ", recommendation['external_urls']['spotify'])

            satisfiedinput=st.radio("Are you satisfied?",['N','Y'])
            if satisfiedinput=="N":
                st.write("Give more proper name of the song or might add more details about singer")
            else:
                st.write("Good enjoy the music.")
