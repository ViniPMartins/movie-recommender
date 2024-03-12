from flask import Flask, request
from flask_basicauth import BasicAuth
from scripts import pipeline_data
import pandas as pd
import pickle
import os
import json
from dotenv import load_dotenv

load_dotenv()

# pipeline = pickle.load(open('models/pipeline.sav', 'rb'))
kmeans = pickle.load(open('models/kmeans_algorithm.sav', 'rb'))
movies_ratings = pd.read_csv('data/processed/movies_ratings.csv', index_col='movieId')

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')

basic_auth = BasicAuth(app)

@app.route('/')
@basic_auth.required
def home():
    return "API Rodando"

@app.route('/api/recommender_movie/', methods=['POST'])
@basic_auth.required
def recommender_movie():
    params = json.loads(request.get_json())
    generos_pipe = pipeline_data(params['generos'])
    group_predict = kmeans.predict(generos_pipe)

    print("n_min_aval", params['n_min_aval'], type(params['n_min_aval']))
    print("rating_min_aval", params['rating_min_aval'], type(params['rating_min_aval']))

    movies_recomended = movies_ratings.query(
        f'group=={group_predict} and n_rating>{params["n_min_aval"]} and mean_rating>{params["rating_min_aval"]}'
        ).sort_values(by='mean_rating', ascending=False).reset_index(drop=True)

    return movies_recomended.to_json()

if '__main__' == __name__:
    app.run(host='0.0.0.0')
