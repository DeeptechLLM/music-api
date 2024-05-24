from flask import current_app
from sklearn.metrics.pairwise import cosine_similarity
from utils.simple_utils import remove_duplicate_items
import json


def get_recommendation_svc(artist_ids, tracks, emotions, genres):
    """Main function to get recommendation

    Args:
        artist_ids (list): list of artist_ids
        tracks (list): list of track_ids
        emotions (list): list of emotions
        genres (list): list of genres        

    Returns:
        list: recommended track list
    """
    
    recommended_tracks = []
    try:
        
        
        # print("track: ", tracks_recommendation[0]["parent_genre_id"])  
        if (len(genres) > 0 and len(tracks)):
            for genre in genres:
                print("genre with track recommendation")
                track_genre = current_app.config['GENRE_MAP_BY_NAME'][genre]
                genre_tracks = get_tracks_with_genre_recommendation(tracks, track_genre)
                recommended_tracks = recommended_tracks + genre_tracks
        elif (len(genres) > 0 and len(tracks) == 0):
            for genre in genres:
                print("genre recommendation")
                track_genre = current_app.config['GENRE_MAP_BY_NAME'][genre]
                genre_tracks = get_genre_tracks(track_genre, 200)                                
                
                filtered_genre_tracks = [track for track in genre_tracks if track['parent_genre_name']==track_genre]
                # print("filtered_genre_tracks: ", genre_tracks[0]['parent_genre_name'])
                recommended_tracks = recommended_tracks + filtered_genre_tracks                
        elif len(tracks) > 0:
            tracks_recommendation = get_tracks_recommendation(tracks) 
            recommended_tracks = recommended_tracks + tracks_recommendation
                
        if len(emotions) > 0:
            for emotion in emotions:
                emotion_tracks = get_emotion_tracks(emotion, 200)
                
                # emotions_recommendation = get_tracks_recommendation(emotion_tracks, 2)                
                
                recommended_tracks = recommended_tracks + emotion_tracks
        
        c_recommend = remove_duplicate_items(recommended_tracks, "track_id")
        o_recommend = sorted(c_recommend, key=lambda item: item["score"], reverse=True)
        recommended_tracks = [{k: v for k, v in item.items() if k != "score"} for item in o_recommend]
        return o_recommend
    except Exception as e: 
        raise Exception(str(e))

        
def get_tracks_recommendation(tracks):
    """Function to get recommendation for track list

    Args:
        tracks (list): list of track_id        

    Returns:
        list: recommended track list
    """
    try: 
        recommended_tracks = []
        for track in tracks:
            result_model_1 = get_recommendation_base_model(track, 200)
            recommended_tracks = recommended_tracks + result_model_1

        return recommended_tracks
    except Exception as e:        
        raise Exception(str(e))
    
def get_tracks_with_genre_recommendation(tracks, genre):
    """Function to get recommendation for track list

    Args:
        tracks (list): list of track_id        

    Returns:
        list: recommended track list
    """
    
    try: 
        recommended_tracks = []
        for track in tracks:
            result_model_1 = get_recommendation_base_model(track, 200)
            print("filtering genre: ", genre)
            filtered_genre_tracks = [track for track in result_model_1 if track['parent_genre_name']==genre]
            recommended_tracks = recommended_tracks + filtered_genre_tracks
        print("result: ", recommended_tracks)
        return recommended_tracks
    except Exception as e:        
        raise Exception(str(e))

def get_recommendation_base_model(track_m_id, num_recommendations=10):
    """Function to get recommendation for single track only for normal model

    Args:
        track_id (number): Single track id
        num_recommendations (int, optional): limit number of recommended tracks. Defaults to 10.

    Returns:
        list: recommended track list
    """
    try:
        print('recommending track_m_id: ', track_m_id)
        df_tracks = current_app.config['DF_TRACKS']
        model = current_app.config['MODEL']        
        
        # Get the track index from recommendation data                
        track_index = df_tracks[df_tracks['track_m_id'] == int(track_m_id)].index[0]
        # track_genre = df_tracks.iloc[track_index]["parent_genre_name"]
        # print("tracks genre: ", track_genre)
        
        # Get the recommended tracks from model withing score using track index
        similarity_scores = cosine_similarity(model[track_index], model)

        # Get the similar tracks by sorting the similarity scores
        similar_tracks = list(enumerate(similarity_scores[0]))
        sorted_similar_tracks = sorted(similar_tracks, key=lambda x: x[1], reverse=True)[1:num_recommendations + 1]

        # # Print the top 10 similar tracks
        # for i, score in sorted_similar_tracks:
        #     print("{} - {}: {}".format(i, df_tracks.loc[i, 'artist_name'], df_tracks.loc[i, 'track_name']))

        recommendations = []

        for i, score in sorted_similar_tracks:            
            track_id = df_tracks.loc[i, 'track_id']
            track_m_id = df_tracks.loc[i, 'track_m_id']
            track_name = str(df_tracks.loc[i, 'track_name'])
            artist_name = str(df_tracks.loc[i, 'artist_name'])
            parent_gid = df_tracks.loc[i, 'parent_genre_id']
            parent_name = str(df_tracks.loc[i, 'parent_genre_name'])

            # print("{}: {}/{} {} by {} - {}".format(i, track_id, track_m_id, track_name, artist_name, score))

            track_info = {
                # "idx": i,
                "track_id": int(track_id),
                "track_m_id": int(track_m_id),
                "track_name": track_name,
                "artist_name": artist_name,                
                "parent_genre_id": int(parent_gid),
                "parent_genre_name": parent_name,
                "score": score
            }
            
            recommendations.append(track_info)
        # filtered_genre_tracks = [track for track in recommendations if track['parent_genre_name']==track_genre]
        return recommendations
    
    except TypeError:
        print("Invalid track_m_id - {}. Please ensure track_m_id can be converted to an integer.".format(track_m_id))
        return []
    except KeyError:
        print("Invalid key. Please ensure 'track_m_id - {}' is a valid key in the DataFrame of model-01.".format(track_m_id))
        return []
    except IndexError:
        print("No matching track found. Please ensure the track_m_id - {} exists in the DataFrame of model-01.".format(track_m_id))
        return []

    except Exception as e:        
        print({"error": str(e)})
        return []
    
def get_recommendation_custom_model_01(track_m_id, num_recommendations=20):
    """Function to get recommendation for single track only for zohioliin model

    Args:
        track_id (number): Single track id
        num_recommendations (int, optional): limit number of recommended tracks. Defaults to 10.

    Returns:
        list: recommended track list
    """
    try:
    
        df_tracks_zohioliin = current_app.config['DF_TRACKS_ZOHIOLIIN']
        model_zohioliin = current_app.config['MODEL_ZOHIOLIIN']        
        
        # Get the track index from recommendation data         
        track_index = df_tracks_zohioliin[df_tracks_zohioliin['track_m_id'] == int(track_m_id)].index[0]
        
        # Get the recommended tracks from model withing score using track index
        similarity_scores = cosine_similarity(model_zohioliin[track_index], model_zohioliin)
        
        # Get the similar tracks by sorting the similarity scores
        similar_tracks = list(enumerate(similarity_scores[0]))
        sorted_similar_tracks = sorted(similar_tracks, key=lambda x: x[1], reverse=True)[1:num_recommendations + 1]
        
        # # Print the top 10 similar tracks
        # for i, score in sorted_similar_tracks:
        #     print("{} - {}: {}".format(i, df_tracks_zohioliin.loc[i, 'artist_name'], df_tracks_zohioliin.loc[i, 'track_name']))

        recommendations = []

        for i, score in sorted_similar_tracks:
            track_id = df_tracks_zohioliin.loc[i, 'track_id']            
            track_name = str(df_tracks_zohioliin.loc[i, 'track_name'])
            artist_name = str(df_tracks_zohioliin.loc[i, 'artist_name'])

            # print("{}: {}/{} {} by {} - {}".format(i, track_id, track_m_id, track_name, artist_name, score))

            track_info = {
                "idx": i,
                "track_id": int(track_id),
                "track_m_id": int(track_m_id),
                "track_name": track_name,
                "artist_name": artist_name,
                "score": score
            }
            recommendations.append(track_info)

        return recommendations
    
    except TypeError:
        print("Invalid track_m_id - {}. Please ensure track_m_id can be converted to an integer.".format(track_m_id))
        return []
    except KeyError:
        print("Invalid key. Please ensure 'track_m_id - {}' is a valid key in the DataFrame.".format(track_m_id))
        return []
    except IndexError:
        print("No matching track found. Please ensure the track_m_id - {} exists in the DataFrame.".format(track_m_id))
        return []

    except Exception as e:        
        print({"error": str(e)})
        return []

def get_recommendation_custom_model_02(track_m_id, num_recommendations=20):
    """Function to get recommendation for single track only for ardiin model

    Args:
        track_id (number): Single track id
        num_recommendations (int, optional): limit number of recommended tracks. Defaults to 10.

    Returns:
        list: recommended track list
    """
    try:    
        df_tracks_ardiin = current_app.config['DF_TRACKS_ARDIIN']
        model_ardiin = current_app.config['MODEL_ARDIIN']        
        
        # Get the track index from recommendation data
        track_index = df_tracks_ardiin[df_tracks_ardiin['track_m_id'] == int(track_m_id)].index[0]
        
        # Get the recommended tracks from model withing score using track index
        similarity_scores = cosine_similarity(model_ardiin[track_index], model_ardiin)
        
        # Get the similar tracks by sorting the similarity scores
        similar_tracks = list(enumerate(similarity_scores[0]))
        sorted_similar_tracks = sorted(similar_tracks, key=lambda x: x[1], reverse=True)[1:num_recommendations + 1]
        
        # # Print the top 10 similar tracks
        # for i, score in sorted_similar_tracks:
        #     print("{} - {}: {}".format(i, df_tracks_ardiin.loc[i, 'artist_name'], df_tracks_ardiin.loc[i, 'track_name']))

        recommendations = []

        for i, score in sorted_similar_tracks:
            track_id = df_tracks_ardiin.loc[i, 'track_id']            
            track_name = str(df_tracks_ardiin.loc[i, 'track_name'])
            artist_name = str(df_tracks_ardiin.loc[i, 'artist_name'])

            # print("{}: {}/{} {} by {} - {}".format(i, track_id, track_m_id, track_name, artist_name, score))

            track_info = {
                "idx": i,
                "track_id": int(track_id),
                "track_m_id": int(track_m_id),
                "track_name": track_name,
                "artist_name": artist_name,
                "score": score
            }
            recommendations.append(track_info)

        return recommendations
    
    except TypeError:
        print("Invalid track_m_id - {}. Please ensure track_m_id can be converted to an integer.".format(track_m_id))
        return []
    except KeyError:
        print("Invalid key. Please ensure 'track_m_id - {}' is a valid key in the DataFrame.".format(track_m_id))
        return []
    except IndexError:
        print("No matching track found. Please ensure the track_m_id - {} exists in the DataFrame.".format(track_m_id))
        return []

    except Exception as e:        
        print({"error": str(e)})
        return []

def get_genre_tracks(genre, num_tracks=40):
    """Function to retrieve top tracks of given genre

    Args:
        genre (string): Give genre name
        num_tracks (int, optional): limit number of tracks. Defaults to 2.

    Returns:
        list: genre's track list
    """
    genre_tracks = []
    genres = current_app.config['DF_GENRES']
    
    genres_in_genre = current_app.config['GENRE_MAP'][genre]
    
    try:        
        
        for genre_name in genres_in_genre:
            print("genre: ", genre_name)
            # Filtering out all songs in the Genre column for non-zero or specific values
            filtered_df = genres[genres[genre_name] != 0]
            
            # Shuffling the songs of the genre(descending)
            shuffled_df = filtered_df.sample(frac=1)
            # sorted_df = filtered_df.sort_values(by=[genre_name], ascending=False)
            
            # Retrieving <num_tracks> tracks from sorted list
            ordered_genre_tracks = shuffled_df[['artist_name', 'track_id', 'track_m_id', 'track_name', 'parent_genre_id', 'parent_genre_name', genre_name]].values.tolist()        
            ordered_genre_tracks = [[artist_name, int(track_id), int(track_m_id), track_name, int(parent_genre_id), parent_genre_name, value, ] for artist_name, track_id, track_m_id, track_name, parent_genre_id, parent_genre_name, value in ordered_genre_tracks][:num_tracks]
                        
            for artist_name, track_id, track_m_id, track_name, parent_genre_id, parent_genre_name, value in ordered_genre_tracks:
                track_info = {                
                    "track_id": track_id,
                    "track_m_id": track_m_id,
                    "track_name": track_name,
                    "artist_name": artist_name,
                    "parent_genre_id": parent_genre_id,
                    "parent_genre_name": parent_genre_name,
                    "score": value
            }
                genre_tracks.append(track_info)
                print("track_id: {}, track_m_id: {}, value: {}, genre: {}".format(track_id, track_m_id, value, parent_genre_name))
    except Exception as e:
        print(e)
    return genre_tracks

def get_emotion_tracks(emotion_name, num_tracks=2):
    """Function to retrieve top tracks of given emotion

    Args:
        emotion_name (string): Given emotion name
        num_tracks (int, optional): limit number of tracks. Defaults to 2.

    Returns:
        list: emotion's track list
    """
    emotion_tracks = []
    emotions = current_app.config['DF_EMOTIONS']
    
    try:
        # Filtering out all songs in the Emotion column for non-zero or specific values
        filtered_df = emotions[emotions[emotion_name] != 0]
        
        # Shuffling the songs of the emotion
        shuffled_df = filtered_df.sample(frac=1)
        print("shuffled: ", shuffled_df)
        # Retrieving <num_tracks> tracks from sorted list
        ordered_emotion_tracks = shuffled_df[['artist_name', 'parent_genre_id', 'parent_genre_name', 'track_id', 'track_m_id', 'track_name', emotion_name]].values.tolist()
        print(ordered_emotion_tracks)
        ordered_emotion_tracks = [[artist_name, int(parent_genre_id), parent_genre_name, int(track_id), int(track_m_id), track_name, value] for artist_name, parent_genre_id, parent_genre_name, track_id, track_m_id, track_name, value in ordered_emotion_tracks][:num_tracks]

        print("Top {} {} songs:".format(num_tracks, emotion_name))
        for artist_name, parent_genre_id, parent_genre_name, track_id, track_m_id, track_name, value in ordered_emotion_tracks:
            track_info = {                
                    "track_id": track_id,
                    "track_m_id": track_m_id,
                    "track_name": track_name,
                    "artist_name": artist_name,
                    "parent_genre_id": parent_genre_id,
                    "parent_genre_name": parent_genre_name,
                    "score": value
            }
            emotion_tracks.append(track_info)
            
            print("track_id: {}, track_m_id: {}, value: {}".format(track_id, track_m_id, value))
    except Exception as e:
        print("Emotion track error: ", e)
    return emotion_tracks

