import joblib

class ProdConfig():
    # load model with configs 
    track_file = 'data/dat_tracks_without_ardiin_and_zohioliin_and_karaoke.jlb'
    genre_file = 'data/dat_genres_without_ardiin_and_zohioliin_and_karaoke.jlb'
    emotion_file = 'data/dat_emotions_without_ardiin_and_zohioliin_and_karaoke.jlb'
    model_file = 'data/mod_tracks_without_ardiin_and_zohioliin_and_karaoke.jlb'   
    
    # Only tracks and model for Zohioliin genre
    track_zohioliin = 'data/dat_tracks_zohioliin_without_karaoke.jlb'
    model_zohioliin = 'data/mod_tracks_zohioliin_without_karaoke.jlb'
    
    # Only tracks and model for Ardiin genre
    track_ardiin = 'data/dat_tracks_ardiin_without_karaoke.jlb'
    model_ardiin = 'data/mod_tracks_ardiin_without_karaoke.jlb'
        
    DF_TRACKS = joblib.load(track_file)    
    DF_GENRES = joblib.load(genre_file)
    DF_EMOTIONS = joblib.load(emotion_file)
    
    DF_TRACKS_ZOHIOLIIN = joblib.load(track_zohioliin)
    DF_GENRES_ZOHIOLIIN = joblib.load(genre_file)
    DF_EMOTIONS_ZOHIOLIIN = joblib.load(emotion_file)
    
    DF_TRACKS_ARDIIN = joblib.load(track_ardiin)
    DF_GENRES_ARDIIN = joblib.load(genre_file)
    DF_EMOTIONS_ARDIIN = joblib.load(emotion_file)
    
    MODEL = joblib.load(model_file)
    MODEL_ZOHIOLIIN = joblib.load(model_zohioliin)
    MODEL_ARDIIN = joblib.load(model_ardiin)

