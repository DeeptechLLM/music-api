import joblib

class ProdConfig():
    # load model with configs 
    track_file = 'data/v2/dat_tracks_without_karaoke.jlb'
    genre_file = 'data/v2/dat_genres7_without_karaoke.jlb'
    emotion_file = 'data/v2/dat_emotions3_without_karaoke.jlb'
    model_file = 'data/v2/mod_tracks_without_karaoke.jlb'   
    
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
    
    GENRE_MAP_BY_NAME = {
        "hiphop_rap": "hiphop",
        "trap": "hiphop",
        "jazz": "jazz",
        "instrumentals": "pop",
        "movie_songs": "pop",
        "pop": "pop",
        "electronics": "pop",
        "r_and_b": "pop",
        "reggae": "pop",
        "pop_opera": "pop",
        "country": "pop",
        "rock_alternative": "rock",
        "metal": "rock",
        "ardiin": "mongol_folk",
        "mongol_country": "mongol_country",
        "zohioliin": "mongol_country",
        "long": "mongol_country",
        "children": "kids",
        "ethnic": "ethnic",
        "classic": "classic",
        "orchestral": "classic",
        "kids": "kids"
    }
    GENRE_MAP = {
        "hiphop": ["hiphop", "rap", "triphop"],
        "jazz": ["jazz", "acidjazz","improvisation","jazzfunk","jazzfusion"],
        "pop": ["pop","ambient","atmospheric","blues","breakbeat","chanson", "chillout","club","dance","darkambient", "darkwave", "deephouse", "disco", "drumnbass", "dubstep", "easylistening", "experimental","folk", "electropop", "funk", "house", "idm", "instrumentalpop", "lounge", "minimal", "newwave", "popfolk", "poprock","rnb","reggae","country", "singersongwriter", "ska", "soul", "synthpop", "techno", "trance" ],
        "rock": ["alternative", "classicrock", "ethnicrock", "gothic", "grunge", "hardrock", "heavymetal", "indie", "industrial", "instrumentalrock", "metal", "postrock", "progressive", "psychedelic", "punkrock", "rock", "rocknroll"],
        "ethnic": ["african", "bossanova", "ethnicrock", "ethno", "folk", "latin", "newage", "oriental", "world"],
        "classic": ["classical", "orchestral", "soundtrack"],        
        "mongol_country": ["mongolian country"],
        "mongol_folk": ["mongolian folk"],
        "kids": ["kids"]
    }

