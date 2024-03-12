import streamlit as st
import requests
import json
import os
import pandas as pd

def get_movies(data):
    # data_json = json.dumps(data)
    data_auth =(st.secrets["BASIC_AUTH_USERNAME"],st.secrets["BASIC_AUTH_PASSWORD"])
    url = st.secrets["API_URL"] + ":" + st.secrets["API_PORT"] + st.secrets["API_PATH"]
    response = requests.post(url, json=data, auth=data_auth)
    df_movies = pd.read_json(response.text)
    return df_movies

st.set_page_config(
   page_title="Movie Recommender",
   page_icon="🎞️",
   layout="wide",
)

st.title("RECOMMENDING MOVIES WITH AI")

st.write('''
This is an application that, through an API, consults a machine learning model called KMEANS and 
recommends movies according to your choice. You can select the genre of the movie, 
the minimum average rating, and the minimum number of reviews the movie can have received.
''')

all_genres = ['Action', 'Adventure', 'Animation', 'Children',
        'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir',
        'Horror', 'IMAX', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller',
        'War', 'Western']

selected_genres = st.multiselect('Select the genres of the movies:', all_genres)
min_average_rat = st.slider('Minimum Average Rating', .0, 5.0, 2.5, 0.1)
min_n_reviews = st.slider('Minimum Number of Reviews', 10, 100, 55, 1)

data = {
    "generos":selected_genres,
    "rating_min_aval":min_average_rat,
    "n_min_aval":min_n_reviews
}

if st.button("Generate recommendations", type="primary"):
    with st.spinner("Getting data..."):
        try:
            generate_movies = get_movies(data)
            map_column_names = {
                'title':'Movie Title',
                'genres':'Movie Genres',
                'mean_rating':'Average Rating',
                'n_rating':'Total Reviews'
            }
            generate_movies = generate_movies[map_column_names.keys()]
            generate_movies = generate_movies.rename(columns=map_column_names)
            st.dataframe(generate_movies, use_container_width=True)
        except:
            st.error("Unable to obtain data")
