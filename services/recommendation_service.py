from flask import make_response, current_app
from sklearn.metrics.pairwise import cosine_similarity
from utils.simple_utils import remove_duplicate_items

def get_recommendation_svc(artist_ids, tracks, emotions, genres):
    
    recommended_tracks = []
    try:
        tracks_recommendation = get_tracks_recommendation(tracks)
        recommended_tracks = recommended_tracks + tracks_recommendation
        
        if len(genres) > 0:
            for genre in genres:
                genre_tracks = get_genre_tracks(genre, 5)
                
                genres_recommendation = get_tracks_recommendation(genre_tracks)
                recommended_tracks = recommended_tracks + genres_recommendation
                
        if len(emotions) > 0:
            for emotion in emotions:
                emotion_tracks = get_emotion_tracks(emotion, 5)
                emotions_recommendation = get_tracks_recommendation(emotion_tracks)
                recommended_tracks = recommended_tracks + emotions_recommendation
        
        c_recommend = remove_duplicate_items(recommended_tracks, "track_id")
        o_recommend = sorted(c_recommend, key=lambda item: item["score"], reverse=True)
        recommended_tracks = [{k: v for k, v in item.items() if k != "score"} for item in o_recommend]
        return recommended_tracks        
    except Exception as e: 
        return e
        
def get_tracks_recommendation(tracks):
    recommended_tracks = []
    for track in tracks:
        result = get_recommendation(track, 40)    
        recommended_tracks = recommended_tracks + result
    return recommended_tracks

def get_recommendation(track_id, num_recommendations=10):
    
    # track_index = df_tracks[df_tracks['track_name'] == user_track].index[0]
    df_tracks = current_app.config['DF_TRACKS']    
    model = current_app.config['MODEL']
    
    track_index = df_tracks[df_tracks['track_id'] == int(track_id)].index[0]
    # print("Params: ", track_id,  str(df_tracks.loc[track_index, 'track_name']), str(df_tracks.loc[track_index, 'artist_name']))
    similarity_scores = cosine_similarity(model[track_index], model)

    similar_tracks = list(enumerate(similarity_scores[0]))
    sorted_similar_tracks = sorted(similar_tracks, key=lambda x: x[1], reverse=True)[1:num_recommendations + 1]

    # # Print the top 10 similar tracks
    # for i, score in sorted_similar_tracks:
    #     print("{}: {}".format(i, df_tracks.loc[i, 'track_name']))

    recommendations = []

    for i, score in sorted_similar_tracks:
        track_id = str(df_tracks.loc[i, 'track_id'])
        track_name = str(df_tracks.loc[i, 'track_name'])
        artist_name = str(df_tracks.loc[i, 'artist_name'])

        print("{}: {} {} by {}".format(i, track_id, track_name, artist_name))

        track_info = {
            "idx": i,
            "track_id": track_id,
            "track_name": track_name,
            "artist_name": artist_name,
            "score": score
        }
        recommendations.append(track_info)

    return recommendations

def get_genre_tracks(genre_name, num_tracks=2):
    genre_tracks = []
    genres = current_app.config['DF_GENRES']
    
    try:
        # Filtering out all songs in the Genre column for non-zero or specific values
        filtered_df = genres[genres[genre_name] != 0]        
        
        # Sorting the songs of the genre(descending)
        sorted_df = filtered_df.sort_values(by=genre_name, ascending=False)
        
        # Retrieving <num_tracks> tracks from sorted list
        ordered_genre_tracks = sorted_df[['track_id', genre_name]].values.tolist()
        ordered_genre_tracks = [[int(track_id), value] for track_id, value in ordered_genre_tracks][:num_tracks]

        # print("Top {} {} songs:".format(num_tracks, genre_name))
        for track_id, value in ordered_genre_tracks:
            genre_tracks.append(track_id)
            # print("track_id: {}, value: {}".format(track_id, value))
    except Exception as e:
        print(e)
    return genre_tracks

def get_emotion_tracks(emotion_name, num_tracks=2):
    emotion_tracks = []
    emotions = current_app.config['DF_EMOTIONS']
    
    try:
        # Filtering out all songs in the Genre column for non-zero or specific values
        filtered_df = emotions[emotions[emotion_name] != 0]
        
        # Sorting the songs of the genre(descending)
        sorted_df = filtered_df.sort_values(by=emotion_name, ascending=False)
        
        # Retrieving <num_tracks> tracks from sorted list
        ordered_emotion_tracks = sorted_df[['track_id', emotion_name]].values.tolist()
        ordered_emotion_tracks = [[int(track_id), value] for track_id, value in ordered_emotion_tracks][:num_tracks]

        # print("Top {} {} songs:".format(num_tracks, emotion_name))
        for track_id, value in ordered_emotion_tracks:
            emotion_tracks.append(track_id)
            # print("track_id: {}, value: {}".format(track_id, value))
    except Exception as e:
        print(e)
    return emotion_tracks