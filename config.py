import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.decomposition import TruncatedSVD
import joblib

class ProdConfig():
    # load model with configs 
    track_file = 'data/dat_tracks.jlb'
    genre_file = 'data/dat_genres.jlb'
    emotion_file = 'data/dat_emotions.jlb'
    model_file = 'data/mod_tracks.jlb'
    # df_tracks = pd.read_csv("data/combined_tracks.csv")
    # df_tracks['content'] = df_tracks['genres'].astype(str) + ' ' + df_tracks['emotions'].astype(str) + ' ' + df_tracks['instrumentals'] + ' ' + df_tracks['track_name'] + ' ' + df_tracks['artist_name'] + ' ' + df_tracks['album_name'].astype(str)
    # df_tracks['content'] = df_tracks['content'].fillna('')
    
    DF_TRACKS = joblib.load(track_file)    
    DF_GENRES = joblib.load(genre_file)
    DF_EMOTIONS = joblib.load(emotion_file)
    
            
    # vectorizer = CountVectorizer()
    # bow = vectorizer.fit_transform(df_tracks['content'])
    # tfidf_transformer = TfidfTransformer()
    # tfidf = tfidf_transformer.fit_transform(bow)
    
    MODEL = joblib.load(model_file)
    # TFIDF = tfidf
            
    # lsa = TruncatedSVD(n_components=100, algorithm='arpack')
    # lsa.fit(tfidf)
    
    # LSA = lsa
