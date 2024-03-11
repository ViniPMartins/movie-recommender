import streamlit as st
import requests
import json
import os
import pandas as pd

def get_movies(data):
    data_json = json.dumps(data)
    data_auth = {
        "username": os.environ.get("BASIC_AUTH_USERNAME"),
        "password": os.environ.get("BASIC_AUTH_PASSWORD")
    }
    url = os.environ.get("API_URL") + ":" + os.environ.get("API_PORT")
    response = requests.post(url, data=data_json, auth=data_auth)
    df_movies = pd.read_json(response)
    return df_movies

st.title("RECOMMENDING MOVIES WITH AI")

st.write('''
This is an application that, through an API, consults a machine learning model called KMEANS and 
recommends movies according to your choice. You can select the genre of the movie, 
the minimum average rating, and the minimum number of reviews the movie can have received.
''')

all_genres = ['(no genres listed)', 'Action', 'Adventure', 'Animation', 'Children',
        'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir',
        'Horror', 'IMAX', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller',
        'War', 'Western']

selected_genres = st.multiselect('Select the genres of the movies:', all_genres)
min_average_rat = st.slider('Minimum Average Rating', .0, 5.0, 2.5, 0.1)
min_n_reviews = st.slider('Minimum Number of Reviews', 10, 100, 55, 1)

data = {
    "generos":selected_genres,
    "n_min_aval":min_average_rat,
    "rating_min_aval":min_n_reviews
}

with st.spinner("Getting data..."):
    generate_movies = st.button("Generate recommendations", type='primary', on_click=get_movies(data))

st.dataframe(generate_movies)
