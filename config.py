import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.decomposition import TruncatedSVD
import joblib

class ProdConfig():
    # load model with configs 
    dat_file = 'data/dat_tracks.jlb'
    mod_file = 'data/mod_tracks.jlb'
    # df_tracks = pd.read_csv("data/combined_tracks.csv")
    # df_tracks['content'] = df_tracks['genres'].astype(str) + ' ' + df_tracks['emotions'].astype(str) + ' ' + df_tracks['instrumentals'] + ' ' + df_tracks['track_name'] + ' ' + df_tracks['artist_name'] + ' ' + df_tracks['album_name'].astype(str)
    # df_tracks['content'] = df_tracks['content'].fillna('')
    df_tracks = joblib.load(dat_file)
    DF_TRACKS = df_tracks
            
    # vectorizer = CountVectorizer()
    # bow = vectorizer.fit_transform(df_tracks['content'])
    # tfidf_transformer = TfidfTransformer()
    # tfidf = tfidf_transformer.fit_transform(bow)
    
    tfidf = joblib.load(mod_file)
    TFIDF = tfidf
            
    # lsa = TruncatedSVD(n_components=100, algorithm='arpack')
    # lsa.fit(tfidf)
    
    # LSA = lsa
