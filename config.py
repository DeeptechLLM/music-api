import joblib

class ProdConfig():
    # load model with configs 
    track_file = 'data/dat_tracks.jlb'
    genre_file = 'data/dat_genres.jlb'
    emotion_file = 'data/dat_emotions.jlb'
    model_file = 'data/mod_tracks.jlb'
    
    DF_TRACKS = joblib.load(track_file)    
    DF_GENRES = joblib.load(genre_file)
    DF_EMOTIONS = joblib.load(emotion_file)
    
    MODEL = joblib.load(model_file)
