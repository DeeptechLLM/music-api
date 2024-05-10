from flask import make_response, current_app
from sklearn.metrics.pairwise import cosine_similarity
from utils.simple_utils import remove_duplicate_items

def get_recommendation_svc(artist_ids, song_ids, emotions_id, genres_id):
    recommended_tracks = []
    try:
        for track in song_ids:
            result = user_recommendation(track, 40)    
            recommended_tracks = recommended_tracks + result
        
        c_recommend = remove_duplicate_items(recommended_tracks, "track_id")
        o_recommend = sorted(c_recommend, key=lambda item: item["score"], reverse=True)
        recommended_tracks = [{k: v for k, v in item.items() if k != "score"} for item in o_recommend]
        return recommended_tracks        
    except Exception as e: 
        return e
        

def user_recommendation(track_id, num_recommendations=10):
    
    # track_index = df_tracks[df_tracks['track_name'] == user_track].index[0]
    df_tracks = current_app.config['df_tracks']
    # print(df_tracks)
    tfidf = current_app.config['tfidf']
    
    track_index = df_tracks[df_tracks['track_id'] == int(track_id)].index[0]
    # print("Params: ", track_id,  str(df_tracks.loc[track_index, 'track_name']), str(df_tracks.loc[track_index, 'artist_name']))
    similarity_scores = cosine_similarity(tfidf[track_index], tfidf)

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

        # print("{}: {} {} by {}".format(i, track_id, track_name, artist_name))

        track_info = {
            "idx": i,
            "track_id": track_id,
            "track_name": track_name,
            "artist_name": artist_name,
            "score": score
        }
        recommendations.append(track_info)

    return recommendations