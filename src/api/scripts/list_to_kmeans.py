from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
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


def pipeline_data(data):

    scaler = pickle.load(open('models/scaler.sav', 'rb'))
    all_pipe = Pipeline([('transform_list', List_to_kmeans()), ('scaller', scaler)])
    return all_pipe.transform(data)