from flask import make_response, current_app
from sklearn.metrics.pairwise import cosine_similarity
from utils.simple_utils import remove_duplicate_items

def get_trackbysimilarity_svc(track_id):
    
    try:
        result = user_recommendation(track_id, 40)
        print("result: ", result, type(result))
        return make_response({'message': 'success', 'tracks': result}, 201)
    except Exception as e: 
        return make_response({'message': str(e)}, 404)
    
def get_trackbysimilarity1_svc(track_name):
    
    try:
        result = user_recommendation_1(track_name)
        print("result: ", result, type(result))
        return make_response({'message': 'success', 'tracks': result}, 201)
    except Exception as e: 
        return make_response({'message': str(e)}, 404)
    
def user_recommendation(track_id, num_recommendations=10):
    
    # track_index = df_tracks[df_tracks['track_name'] == user_track].index[0]
    df_tracks = current_app.config['df_tracks']
    # print(df_tracks)
    tfidf = current_app.config['tfidf']
    
    track_index = df_tracks[df_tracks['track_id'] == int(track_id)].index[0]
    print("Params: ", track_id,  str(df_tracks.loc[track_index, 'track_name']), str(df_tracks.loc[track_index, 'artist_name']))
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

        print("{}: {} {} by {}".format(i, track_id, track_name, artist_name))

        recommendations.append((i, track_id, track_name, artist_name, score))

    return recommendations

def user_recommendation_1(track_name):
    sim_df_names = current_app.config['sim_df_names']
    recommended_list = []
    # Find songs most similar to another song
    series = sim_df_names[track_name].sort_values(ascending = False)
    
    # Remove cosine similarity == 1 (songs will always have the best match with themselves)
    series = series.drop(track_name)
    
    # Display the 5 top matches 
    print("\n*******\nSimilar songs to ", track_name)
    
    result_20 = series.head(20)
    print(result_20)
    print("filename: ", result_20.index)
    
    for track in result_20.index:
        print("track: {}, similarity: {}".format(track, result_20[track]))
        print(result_20[track] > 0.7)
        track_name, track_index, track_extension = track.split('.')
        print("track_name: {}, track_index: {}, track_ext: {}".format(track_name, track_index, track_extension))
        if result_20[track] > 0.69:
            recommended_list.append({
                "track_name": track_name
            })
        # Get track's full info 
        
        # print (result_20.getitem(track, i))
    unique = remove_duplicate_items(recommended_list, "track_name")
    return unique