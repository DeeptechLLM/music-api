from flask import current_app
from sklearn.metrics.pairwise import cosine_similarity
from utils.simple_utils import remove_duplicate_items

def get_recommendation_svc(tracks, emotions, genres, limit, recc_type):
    """Main function to get recommendation

    Args        
        tracks (list): list of track_ids
        emotions (list): list of emotions
        genres (list): list of genres        

    Returns:
        list: recommended track list
    """
    
    recommended_tracks = []
    msg = []
    try: 
        if recc_type == 'home':
            track_genres = [get_tracks_genre(track) for track in tracks]
            genres_mapped = [current_app.config['GENRE_MAP_WITH_MMUSIC'][genre] for genre in genres]
            print("merging genres:",track_genres, genres_mapped)
            track_genres = track_genres + genres_mapped
            
            track_first_genre = max(set(track_genres), key=track_genres.count)                        
            tracks_recommendation_1, err = get_genre_tracks(track_first_genre, 200)            
            recommended_tracks = recommended_tracks + tracks_recommendation_1            
            
            if len(track_genres) > 1:
                track_second_genre = sorted(set(track_genres), key=track_genres.count)[-2]                        
                tracks_recommendation_2, err = get_genre_tracks(track_second_genre, 200)
                recommended_tracks = recommended_tracks + tracks_recommendation_2
            
                
        elif recc_type == 'emotion':
           
            emotion = emotions[0]
            track_emotion = current_app.config['EMOTION_MAP_WITH_MMUSIC'][emotion]
            print("tracks emotino: ", track_emotion)
            genres_mapped = [current_app.config['GENRE_MAP_WITH_MMUSIC'][genre] for genre in genres]
            emotion_tracks, err = get_tracks_by_emotion(track_emotion, genres_mapped)              
            
            recommended_tracks = emotion_tracks
        else:
            if tracks:
                if genres:
                    for genre in genres: 
                        try: 
                        
                            track_genre = current_app.config['GENRE_MAP_WITH_MMUSIC'][genre]
                            genre_tracks, err = get_tracks_with_genre_recommendation(tracks, track_genre)
                            if err:
                                msg.append(err)
                            recommended_tracks = recommended_tracks + genre_tracks
                        except KeyError:
                            print("Genre not found: ", genre)
                            msg.append("Genre not found: {}".format(genre))

                if emotions:
                    for emotion in emotions:
                        try: 
                            track_emotion = current_app.config['EMOTION_MAP_WITH_MMUSIC'][emotion]
                            emotion_tracks, err = get_tracks_with_emotion_recommendation(tracks, track_emotion)
                            # emotion_tracks, err = get_emotion_tracks(track_emotion, 200)
                            if err:
                                msg.append(err)
                            recommended_tracks = recommended_tracks + emotion_tracks
                        except KeyError:
                            print("Emotion not found: ", emotion)
                            msg.append("Emotion not found: {}".format(emotion))
                    
                if not genres and not emotions: 
                    tracks_recommendation, err = get_tracks_recommendation(tracks) 
                    if err:
                        msg.append(err)
                    recommended_tracks = recommended_tracks + tracks_recommendation
            else:
                if genres:
                    for genre in genres:                     
                        try: 
                            track_genre = current_app.config['GENRE_MAP_WITH_MMUSIC'].get(genre)                        
                            genre_tracks, err = get_genre_tracks(track_genre, 200)
                            if err: 
                                msg.append(err)                              
                        
                            # filtered_genre_tracks = [track for track in genre_tracks if track['parent_genre_name']==track_genre]
                        
                            recommended_tracks = recommended_tracks + genre_tracks
                        except KeyError:
                            print("Genre not found: ", genre)
                            msg.append("Genre not found: {}".format(genre))
                        
                    if emotions:
                        for emotion in emotions:
                            track_emotion = current_app.config['EMOTION_MAP_WITH_MMUSIC'].get(emotion)
                            emotion_tracks, err = get_emotion_tracks(track_emotion, genres, 200)
                            if err:
                                msg.append(err)
                        
                        # emotions_recommendation = get_tracks_recommendation(emotion_tracks, 2)                
                        
                            recommended_tracks = recommended_tracks + emotion_tracks             
       
        c_recommend = remove_duplicate_items(recommended_tracks, "track_id")        
        o_recommend = sorted(c_recommend, key=lambda item: item["score"], reverse=True)
        recommended_tracks = [{k: v for k, v in item.items() if k != "parent_genre_id" and k != "parent_genre_name"} for item in o_recommend]
        # recommended_tracks = [{k: v for k, v in item.items() if k != "score"} for item in o_recommend]
        return recommended_tracks[:limit], msg
    except IndexError:
        print("No second genre found.")
                
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
            result_model_1, err = get_recommendation_base_model(track, 200)
            recommended_tracks = recommended_tracks + result_model_1
        
        return recommended_tracks, err
    except Exception as e: 
        raise Exception(str(e))

    
def get_tracks_with_genre_recommendation(tracks, genre):
    """Function to get recommendation for track list

    Args:
        tracks (list): list of track_id  
        genre (string): genre name      

    Returns:
        list: recommended track list
    """
    
    try: 
        recommended_tracks = []
        for track in tracks:
            result_model_1, err = get_recommendation_base_model(track, 200)
                       
            filtered_genre_tracks = [track for track in result_model_1 if track['parent_genre_name'] == genre]
            recommended_tracks = recommended_tracks + filtered_genre_tracks
        
        return recommended_tracks, err
    except Exception as e: 
        raise Exception(str(e))

    
def get_tracks_with_emotion_recommendation(tracks, emotion):
    """Function to get recommendation for track list

    Args:
        tracks (list): list of track_id        

    Returns:
        list: recommended track list
    """
    
    try: 
        recommended_tracks = []
        for track in tracks:
            result_model_1, err = get_recommendation_base_model(track, 200)            
            recommended_tracks = recommended_tracks + result_model_1
        
        return recommended_tracks, err
    except Exception as e: 
        raise Exception(str(e))


def get_recommendation_base_model(track_m_id, num_recommendations=10):
    """Function to get recommendation for single track only for normal model

    Args:
        track_m_id (number): Single track id
        num_recommendations (int, optional): limit number of recommended tracks. Defaults to 10.

    Returns:
        list: recommended track list
    """
    try:

        df_tracks = current_app.config['DF_TRACKS']
        model = current_app.config['MODEL']        
        
        # Get the track index from recommendation data                
        track_index = df_tracks[df_tracks['track_m_id'] == int(track_m_id)].index[0]
        # track_genre = df_tracks.iloc[track_index]["parent_genre_name"]
                
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
                "track_id": int(track_id),
                "track_m_id": int(track_m_id),
                "track_name": track_name,
                "artist_name": artist_name,
                "parent_genre_id": int(parent_gid),
                "parent_genre_name": parent_name,
                "score": float(score)
            }
            
            recommendations.append(track_info)
        
        return recommendations, None
    
    except TypeError:
        print("Invalid track_m_id - {}. Please ensure track_m_id can be converted to an integer.".format(track_m_id))
        err = "Invalid track_m_id - {}. Please ensure track_m_id can be converted to an integer.".format(track_m_id)
        return [], err
    except KeyError:
        print("Invalid key. Please ensure 'track_m_id - {}' is a valid key in the DataFrame of model-01.".format(track_m_id))
        err = "Invalid key. Please ensure 'track_m_id - {}' is a valid key in the DataFrame of model-01.".format(track_m_id)
        return [], err
    except IndexError:
        print("No matching track found. Please ensure the track_m_id - {} exists in the DataFrame of model-01.".format(track_m_id))
        err = "No matching track found. Please ensure the track_m_id - {} exists in the DataFrame of model-01.".format(track_m_id)
        return [], err

    except Exception as e: 
        print({"error": str(e)})
        err = {"error": str(e)}
        return [], err

    
def get_recommendation_custom_model_01(track_m_id, num_recommendations=20):
    """Function to get recommendation for single track only for zohioliin model

    Args:
        track_m_id (number): Single track id
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
        shuffled_df = similar_tracks.sample(frac=1)
        # sorted_similar_tracks = sorted(similar_tracks, key=lambda x: x[1], reverse=True)[1:num_recommendations + 1]
        
        # # Print the top 10 similar tracks
        # for i, score in sorted_similar_tracks:
        #     print("{} - {}: {}".format(i, df_tracks_zohioliin.loc[i, 'artist_name'], df_tracks_zohioliin.loc[i, 'track_name']))

        recommendations = []

        for i, score in shuffled_df:
            track_id = df_tracks_zohioliin.loc[i, 'track_id']            
            track_name = str(df_tracks_zohioliin.loc[i, 'track_name'])
            artist_name = str(df_tracks_zohioliin.loc[i, 'artist_name'])

            # print("{}: {}/{} {} by {} - {}".format(i, track_id, track_m_id, track_name, artist_name, score))

            track_info = {
                "track_id": int(track_id),
                "track_m_id": int(track_m_id),
                "track_name": track_name,
                "artist_name": artist_name,
                "score": float(score)
            }
            recommendations.append(track_info)

        return recommendations, None
    
    except TypeError:
        print("Invalid track_m_id - {}. Please ensure track_m_id can be converted to an integer.".format(track_m_id))
        err = "Invalid track_m_id - {}. Please ensure track_m_id can be converted to an integer.".format(track_m_id)
        return [], err
    except KeyError:
        print("Invalid key. Please ensure 'track_m_id - {}' is a valid key in the DataFrame of model-01.".format(track_m_id))
        err = "Invalid key. Please ensure 'track_m_id - {}' is a valid key in the DataFrame of model-01.".format(track_m_id)
        return [], err
    except IndexError:
        print("No matching track found. Please ensure the track_m_id - {} exists in the DataFrame of model-01.".format(track_m_id))
        err = "No matching track found. Please ensure the track_m_id - {} exists in the DataFrame of model-01.".format(track_m_id)
        return [], err

    except Exception as e: 
        print({"error": str(e)})
        err = {"error": str(e)}
        return [], err


def get_recommendation_custom_model_02(track_m_id, num_recommendations=20):
    """Function to get recommendation for single track only for ardiin model

    Args:
        track_m_id (number): Single track id
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
                "track_id": int(track_id),
                "track_m_id": int(track_m_id),
                "track_name": track_name,
                "artist_name": artist_name,
                "score": float(score)
            }
            recommendations.append(track_info)

        return recommendations, None
    
    except TypeError:
        print("Invalid track_m_id - {}. Please ensure track_m_id can be converted to an integer.".format(track_m_id))
        err = "Invalid track_m_id - {}. Please ensure track_m_id can be converted to an integer.".format(track_m_id)
        return [], err
    except KeyError:
        print("Invalid key. Please ensure 'track_m_id - {}' is a valid key in the DataFrame of model-01.".format(track_m_id))
        err = "Invalid key. Please ensure 'track_m_id - {}' is a valid key in the DataFrame of model-01.".format(track_m_id)
        return [], err
    except IndexError:
        print("No matching track found. Please ensure the track_m_id - {} exists in the DataFrame of model-01.".format(track_m_id))
        err = "No matching track found. Please ensure the track_m_id - {} exists in the DataFrame of model-01.".format(track_m_id)
        return [], err

    except Exception as e: 
        print({"error": str(e)})
        err = {"error": str(e)}
        return [], err


def get_genre_tracks(genre, num_tracks=40):
    """Function to retrieve top tracks of given genre

    Args:
        genre (string): Give genre name
        num_tracks (int, optional): limit number of tracks.

    Returns:
        list: genre's track list
    """
    recommended_list = []
    genre_tracks_1 = []
    genre_tracks_2 = []
    genres = current_app.config['DF_GENRES']    
    genres_in_genre = current_app.config['GENRE_MAP'].get(genre)
    
    try: 

        for genre_name in genres_in_genre:             
            if genre_name == 'mongolian country' or genre_name == 'mongolian folk':                
                # Filtering out all songs in the Genre column for non-zero or specific values
                filtered_df = genres[genres['parent_genre_name'].str.contains(genre_name)]
                
                # Shuffling the songs of the genre(descending)
                shuffled_df = filtered_df.sample(frac=1)
                # sorted_df = filtered_df.sort_values(by=[genre_name], ascending=False)
                
                # Retrieving <num_tracks> tracks from sorted list
                ordered_genre_tracks = shuffled_df[['artist_name', 'parent_genre_id', 'parent_genre_name', 'track_id', 'track_m_id', 'track_name']].values.tolist()                
                ordered_genre_tracks = [[artist_name, int(parent_genre_id), parent_genre_name, int(track_id), int(track_m_id), track_name] for artist_name, parent_genre_id, parent_genre_name, track_id, track_m_id, track_name in ordered_genre_tracks][:num_tracks]
                                            
                for artist_name, parent_genre_id, parent_genre_name, track_id, track_m_id, track_name in ordered_genre_tracks:                    
                    track_info = {                
                        "track_id": track_id,
                        "track_m_id": track_m_id,
                        "track_name": track_name,
                        "artist_name": artist_name,
                        "parent_genre_id": parent_genre_id,
                        "parent_genre_name": parent_genre_name,
                        "score": 0.0
                }
                    genre_tracks_1.append(track_info)
                    # print("track_id: {}, track_m_id: {}, genre: {}".format(track_id, track_m_id, parent_genre_name))
            else:

                # Filtering out all songs in the Genre column for non-zero or specific values
                filtered_df = genres[genres[genre_name] != 0]

                # Shuffling the songs of the genre(descending)
                shuffled_df = filtered_df.sample(frac=1)
                # sorted_df = filtered_df.sort_values(by=[genre_name], ascending=False)
                
                # Retrieving <num_tracks> tracks from sorted list
                ordered_genre_tracks = shuffled_df[['artist_name', 'track_id', 'track_m_id', 'track_name', 'parent_genre_id', 'parent_genre_name', genre_name]].values.tolist()        
                ordered_genre_tracks = [[artist_name, int(track_id), int(track_m_id), track_name, int(parent_genre_id), parent_genre_name, value, ] for artist_name, track_id, track_m_id, track_name, parent_genre_id, parent_genre_name, value in ordered_genre_tracks][:num_tracks]
                            
                for artist_name, track_id, track_m_id, track_name, parent_genre_id, parent_genre_name, value in ordered_genre_tracks:
                    if value > 1:
                        value = value / 100
                    track_info = {                
                        "track_id": track_id,
                        "track_m_id": track_m_id,
                        "track_name": track_name,
                        "artist_name": artist_name,
                        "parent_genre_id": parent_genre_id,
                        "parent_genre_name": parent_genre_name,
                        "score": float(value)
                }
                    genre_tracks_2.append(track_info)
                    # print("track_id: {}, track_m_id: {}, value: {}, genre: {}".format(track_id, track_m_id, value, parent_genre_name))
                genre_tracks_2 = [track for track in genre_tracks_2 if track['parent_genre_name'] == genre]
        recommended_list = genre_tracks_1 + genre_tracks_2                        
    except Exception as e: 
        print({"error": str(e)})
        err = {"error": str(e)}
        return [], err    
    
    return recommended_list, None


def get_emotion_tracks(emotion, genres, num_tracks=40):
    """Function to retrieve top tracks of given emotion

    Args:
        emotion_name (string): Given emotion name
        num_tracks (int, optional): limit number of tracks.

    Returns:
        list: emotion's track list
    """
    recommended_list = []
    emotion_tracks = []
    
    emotions = current_app.config['DF_EMOTIONS']    
    
    try: 
        
        emotion_map = current_app.config['EMOTION_MAP']
        if emotion in emotion_map:            
            emotion_list = emotion_map.get(emotion)
            
            for emotion_name in emotion_list: 
                
                # Filtering out all songs in the Emotion column for non-zero or specific values
                filtered_df = emotions[emotions[emotion_name] != 0]
                
                # Shuffling the songs of the emotion
                shuffled_df = filtered_df.sample(frac=1)
                # Retrieving <num_tracks> tracks from sorted list
                ordered_emotion_tracks = shuffled_df[['artist_name', 'parent_genre_id', 'parent_genre_name', 'track_id', 'track_m_id', 'track_name', emotion_name]].values.tolist()
                ordered_emotion_tracks = [[artist_name, int(parent_genre_id), parent_genre_name, int(track_id), int(track_m_id), track_name, value] for artist_name, parent_genre_id, parent_genre_name, track_id, track_m_id, track_name, value in ordered_emotion_tracks][:num_tracks]

                # print("Top {} {} songs:".format(num_tracks, emotion_name))
                for artist_name, parent_genre_id, parent_genre_name, track_id, track_m_id, track_name, value in ordered_emotion_tracks:
                    track_info = {                
                            "track_id": track_id,
                            "track_m_id": track_m_id,
                            "track_name": track_name,
                            "artist_name": artist_name,
                            "parent_genre_id": parent_genre_id,
                            "parent_genre_name": parent_genre_name,
                            "score": float(value)
                    }

                    if parent_genre_name in genres:
                        emotion_tracks.append(track_info)
        recommended_list = recommended_list + emotion_tracks

    except Exception as e: 
        print({"error": str(e)})
        err = {"error": str(e)}
        return [], err
    return recommended_list, None

def get_tracks_by_emotion(emotion, genres, num_tracks=40):
    """Function to retrieve top tracks of given emotion

    Args:
        emotion_name (string): Given emotion name
        num_tracks (int, optional): limit number of tracks.

    Returns:
        list: emotion's track list
    """
    recommended_list = []
    emotion_tracks = []
    
    emotion_model = current_app.config['DF_EMOTIONS']    
    
    try: 
        
        # emotion_map = current_app.config['EMOTION_MAP']
        # if emotion in emotion_map:            
        #     emotion_list = emotion_map.get(emotion)
            
        #     for emotion_name in emotion_list: 
        
        # Filtering out all songs in the Emotion column for non-zero or specific values
        filtered_emotions = emotion_model[emotion_model['child'] == int(emotion)]        
                
        # Shuffling the songs of the emotion
        shuffled_emotions = filtered_emotions.sample(frac=1).reset_index(drop=True)
        
        if len(shuffled_emotions) < num_tracks:
            num_tracks = len(shuffled_emotions)
            
        selected_list = shuffled_emotions.head(num_tracks)
            
        # Retrieving <num_tracks> tracks from sorted list
        ordered_emotion_tracks = selected_list[['artist_name', 'parent_genre_id', 'parent_genre_name', 'track_id', 'track_m_id', 'track_name']].values.tolist()
        ordered_emotion_tracks = [[artist_name, int(parent_genre_id), parent_genre_name, int(track_id), int(track_m_id), track_name] for artist_name, parent_genre_id, parent_genre_name, track_id, track_m_id, track_name in ordered_emotion_tracks][:num_tracks]

        # print("Top {} {} songs:".format(num_tracks, emotion_name))
        for artist_name, parent_genre_id, parent_genre_name, track_id, track_m_id, track_name in ordered_emotion_tracks:
            track_info = {                
                "track_id": track_id,
                "track_m_id": track_m_id,
                "track_name": track_name,
                "artist_name": artist_name,
                "parent_genre_id": parent_genre_id,
                "parent_genre_name": parent_genre_name,
                "score": float(1)
            }
            
            if parent_genre_name in genres:
                emotion_tracks.append(track_info)
        recommended_list = recommended_list + emotion_tracks

    except Exception as e: 
        print({"error": str(e)})
        err = {"error": str(e)}
        return [], err
    return recommended_list, None

def get_tracks_genre(track_id):
    """Function to get genre of a track

    Args:
        track_id (number): Single track id

    Returns:
        string: genre name
    """
    try:    
        
        df_tracks = current_app.config['DF_TRACKS']
        track_genre = df_tracks[df_tracks['track_m_id'] == int(track_id)]['parent_genre_name'].values[0]
        print("found genre for track_m_id {} : {} ".format(track_id, df_tracks[df_tracks['track_m_id'] == int(track_id)]))
        return track_genre
    except IndexError as e:
        print("No genre found for track_m_id {} : {}".format(track_id, e))
    except Exception as e: 
        print({"error": str(e)})
        err = {"error": str(e)}
        return None, err