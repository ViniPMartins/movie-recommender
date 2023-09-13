from flask import Flask, request
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import pickle

class List_to_kmeans(BaseEstimator, TransformerMixin):

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        all_generos = ['(no genres listed)', 'Action', 'Adventure', 'Animation', 'Children',
        'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir',
        'Horror', 'IMAX', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller',
        'War', 'Western']
        dummies_generos = []
        for gen in all_generos:
            if gen in X:
                dummies_generos.append(1)
            else:
                dummies_generos.append(0)

        return [dummies_generos]

pipeline = pickle.load(open('./models-serializer/pipeline.sav', 'rb'))
kmeans = pickle.load(open('./models-serializer/kmeans_algorithm.sav', 'rb'))
movies_ratings = pd.read_csv('database-csv/movies_ratings.csv', index_col='movieId')

app = Flask(__name__)

@app.route('/')
def home():
    return "API Rodando"

@app.route('/api/recommender_movie/', methods=['POST'])
def recommender_movie():
    params = request.get_json()
    generos_pipe = pipeline.transform(params['generos'])
    group_predict = kmeans.predict(generos_pipe)

    movies_recomended = movies_ratings.query(
        f'group=={group_predict} and n_rating>{params["n_min_aval"]} and mean_rating>{params["rating_min_aval"]}'
        ).sort_values(by='mean_rating', ascending=False)
    
    return movies_recomended.to_json()

if '__main__' == __name__:
    app.run(debug=True)