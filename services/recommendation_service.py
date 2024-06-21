from flask import current_app
from sklearn.metrics.pairwise import cosine_similarity
from utils.simple_utils import remove_duplicate_items
from collections import Counter
from math import ceil


def get_recommendation_svc(tracks, emotions, genres, limit, recc_type):
    """Main function to get recommendation

    Args        
        tracks (list): list of track_ids
        emotions (list): list of emotions
        genres (list): list of genres       
        limit (int): limit number of recommended tracks
        recc_type (string): type of recommendation 

    Returns:
        list: recommended track list
    """
    
    recommended_tracks = []
    msg = []
    try: 
        if recc_type == 'home': 
            
            # Get the genres of the tracks
            track_genres = [get_tracks_genre(track) for track in tracks if get_tracks_genre(track) != None]
            # genres_mapped = [current_app.config['GENRE_MAP_WITH_MMUSIC'][genre] for genre in genres]
            # genres_mapped.extend(genres_mapped)
            
            track_genres = track_genres + genres
            
            # Count the occurence of each genre
            genre_counts = Counter(track_genres)
            
            # Calculate the total number of genres
            total_genres = len(track_genres)
            
            # Calculate the percentage of each genre which is more than 10%
            genre_percentages = {genre: count / total_genres for genre, count in genre_counts.items() if count / total_genres >= 0.1}
            
            # increase all genre percentages until all percentages sum up to 1
            while sum(genre_percentages.values()) < 1:
                for genre in genre_percentages.keys():
                    genre_percentages[genre] += 0.01
            
            sorted_genre_percentages = sorted(genre_percentages.items(), key=lambda x: x[1], reverse=True)
            # track based recommendation
            tracks_recommendation, err = get_tracks_with_genre_recommendation(tracks)
            for genre, percentage in sorted_genre_percentages: 
                        try:                             
                            # track_genre = current_app.config['GENRE_MAP_WITH_MMUSIC'][genre]
                            # genre_tracks, err = get_tracks_with_genre_recommendation(tracks, genre)
                            filtered_genre_tracks = [track for track in tracks_recommendation if track['m_genre'] == genre] 
                            if err:
                                msg.append(err)
                            recommended_tracks = recommended_tracks + filtered_genre_tracks
                        except KeyError:
                            print("Genre not found: ", genre)
                            msg.append("Genre not found: {}".format(genre))
            recommended_tracks = [track for track in recommended_tracks if track['track_m_id'] not in tracks]                
            # genre based recommendation
            # for genre, percentage in sorted_genre_percentages:                
            #     genre_percentage = int(ceil(percentage * 100) * (limit/100))
            #     print("percentage of {}: {}".format(limit, genre_percentage))
            #     tracks_recommendation, err = get_genre_tracks(genre, genre_percentage)    
            #     recommended_tracks = recommended_tracks + tracks_recommendation     
                
            c_recommend = remove_duplicate_items(recommended_tracks, "track_id")        
            o_recommend = sorted(c_recommend, key=lambda item: item["score"], reverse=True)
            recommended_tracks = [{k: v for k, v in item.items() if k != "m_genre_id" and k != "m_genre"} for item in o_recommend]
            # recommended_tracks = [{k: v for k, v in item.items() if k != "score"} for item in o_recommend]
            return recommended_tracks, msg
                
        elif recc_type == 'emotion':
           
            emotion = emotions[0]
            track_emotion = current_app.config['EMOTION_MAP_WITH_MMUSIC'][emotion]
            
            # genres_mapped = [current_app.config['GENRE_MAP_WITH_MMUSIC'][genre] for genre in genres]
            emotion_tracks, err = get_tracks_by_emotion(track_emotion, genres)              
            
            recommended_tracks = emotion_tracks
            
        elif recc_type == 'player':            
            tracks_recommendation, err = get_tracks_with_genre_recommendation(tracks)
            
            for genre in genres: 
                        try:                                             
                            # track_genre = current_app.config['GENRE_MAP_WITH_MMUSIC'][genre]                            
                            filtered_genre_tracks = [track for track in tracks_recommendation if track['m_genre'] == genre]                            
                            if err:
                                msg.append(err)
                            recommended_tracks = recommended_tracks + filtered_genre_tracks
                        except KeyError:
                            print("Genre not found: ", genre)
                            msg.append("Genre not found: {}".format(genre))
            recommended_tracks = [track for track in recommended_tracks if track['track_m_id'] not in tracks]
        elif recc_type == 'search': 
            tracks_recommendation, err = get_recommendation_base_model(tracks[0], 200)
            
            if genres:
                filtered_genre_tracks = [track for track in tracks_recommendation if track['m_genre'] == genres[0]] 
                recommended_tracks = recommended_tracks + filtered_genre_tracks
            else:
                track_genre = get_tracks_genre(tracks[0])
                # mapped_genre = current_app.config['GENRE_MAP_WITH_MMUSIC'][track_genre]                
                filtered_genre_tracks = [track for track in tracks_recommendation if track['m_genre'] == track_genre]  
                recommended_tracks = recommended_tracks + filtered_genre_tracks
            
        else:
            if tracks:
                tracks_recommendation, err = get_tracks_with_genre_recommendation(tracks)
                if genres:
                    for genre in genres: 
                        try:                         
                            track_genre = current_app.config['GENRE_MAP_WITH_MMUSIC'][genre]
                            filtered_genre_tracks = [track for track in tracks_recommendation if track['m_genre'] == track_genre]   
                            # genre_tracks, err = get_tracks_with_genre_recommendation(tracks, track_genre)
                            if err:
                                msg.append(err)
                            recommended_tracks = recommended_tracks + filtered_genre_tracks
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
                    
                recommended_tracks = [track for track in recommended_tracks if track['track_m_id'] not in tracks]
            else:
                if genres:
                    for genre in genres: 
                        try: 
                            track_genre = current_app.config['GENRE_MAP_WITH_MMUSIC'].get(genre)                        
                            genre_tracks, err = get_genre_tracks(track_genre, 200)
                            if err: 
                                msg.append(err)                              
                        
                            # filtered_genre_tracks = [track for track in genre_tracks if track['m_genre']==track_genre]
                        
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
        recommended_tracks = [{k: v for k, v in item.items() if k != "m_genre_id" and k != "m_genre_id"} for item in o_recommend]
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

    
def get_tracks_with_genre_recommendation(tracks):
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
        o_recommend = sorted(recommended_tracks, key=lambda item: item["score"], reverse=True)
        return o_recommend, err
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
    
    err = []
    recommendations = []
    missing_indices = []
    try:

        df_tracks = current_app.config['DF_TRACKS']
        model = current_app.config['MODEL']        
        
        # Get the track index from recommendation data  
        track = df_tracks[df_tracks['track_m_id'] == int(track_m_id)]
        track_index = track.index[0]
                
        # Get the recommended tracks from model withing score using track index
        similarity_scores = cosine_similarity(model[track_index], model)        

        # Get the similar tracks by sorting the similarity scores
        similar_tracks = list(enumerate(similarity_scores[0]))        
        sorted_similar_tracks = sorted(similar_tracks, key=lambda x: x[1], reverse=True)[1:num_recommendations + 1]        
        
        # # Print the top 10 similar tracks
        # for i, score in sorted_similar_tracks:            
        #     print("{} - {}: {}".format(i, df_tracks.loc[i, 'artist_name'], df_tracks.loc[i, 'track_name']))
        
        for i, score in sorted_similar_tracks: 
            try:                
                if i in df_tracks.index:
                    
                    track_id = df_tracks.loc[int(i), 'track_id']
                    track_m_id = df_tracks.loc[i, 'track_m_id']
                    track_name = str(df_tracks.loc[i, 'track_name'])
                    artist_name = str(df_tracks.loc[i, 'artist_name'])
                    parent_gid = df_tracks.loc[i, 'm_genre_id']
                    parent_name = str(df_tracks.loc[i, 'm_genre'])
                    
                    track_info = {
                        "track_id": int(track_id),
                        "track_m_id": int(track_m_id),
                        "track_name": track_name,
                        "artist_name": artist_name,
                        "m_genre_id": int(parent_gid),
                        "m_genre": parent_name,
                        "score": float(score)
                    }

                    recommendations.append(track_info)
                else:
                    missing_indices.append(i)
                # print("{}: {}/{} {} by {}({}/{}) - {}".format(i, track_id, track_m_id, track_name, artist_name, parent_gid, parent_name, score))
                if missing_indices:
                    print(f"Warning: The following indices were not found in the tracks DataFrame: {missing_indices}")                
                
            except TypeError:
                print("Invalid track_m_id - {}. Please ensure track_m_id can be converted to an integer.".format(track_m_id))
                err.append("Invalid track_m_id - {}. Please ensure track_m_id can be converted to an integer.".format(track_m_id))
                pass
                
            except KeyError:
                print("Invalid key. Please ensure 'key - {} ' is a valid key in the DataFrame of model-01.".format(i))
                # err.append("Invalid key. Please ensure 'key - {}' is a valid key in the DataFrame of model-01.".format(i))
                pass
                
            except IndexError:
                print("No matching track found. Please ensure the track_m_id - {} exists in the DataFrame of model-01.".format(track_m_id))
                err.append("No matching track found. Please ensure the track_m_id - {} exists in the DataFrame of model-01.".format(track_m_id))
                pass
    
    except Exception as e: 
        print("Error: track - {} does not found. {}".format(track_m_id, str(e)))
        err.append({"error": str(e)})
        pass
    
    return recommendations, err

    
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
    
    recommendations = []
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
            if genre_name == 'niitiin' or genre_name == 'ardiin': 
                # Filtering out all songs in the Genre column for non-zero or specific values
                filtered_df = genres[genres['m_genre'] == genre_name]
                
                # Shuffling the songs of the genre(descending)
                # shuffled_df = filtered_df.sample(frac=1)
                # sorted_df = filtered_df.sort_values(by=[genre_name], ascending=False)
                
                # Retrieving <num_tracks> tracks from sorted list
                ordered_genre_tracks = filtered_df[['artist_name', 'm_genre_id', 'm_genre', 'track_id', 'track_m_id', 'track_name']].values.tolist()                
                ordered_genre_tracks = [[artist_name, int(m_genre_id), m_genre, int(track_id), int(track_m_id), track_name] for artist_name, m_genre_id, m_genre, track_id, track_m_id, track_name in ordered_genre_tracks][:num_tracks]
                                            
                for artist_name, m_genre_id, m_genre, track_id, track_m_id, track_name in ordered_genre_tracks: 
                    track_info = {                
                        "track_id": track_id,
                        "track_m_id": track_m_id,
                        "track_name": track_name,
                        "artist_name": artist_name,
                        "m_genre_id": m_genre_id,
                        "m_genre": m_genre,
                        "score": 0.0
                }
                    genre_tracks_1.append(track_info)
                    # print("track_id: {}, track_m_id: {}, genre: {}".format(track_id, track_m_id, m_genre))
            else:

                # Filtering out all songs in the Genre column for non-zero or specific values
                filtered_df = genres[genres[genre_name] != 0]

                # Shuffling the songs of the genre(descending)
                # shuffled_df = filtered_df.sample(frac=1)
                sorted_df = filtered_df.sort_values(by=[genre_name], ascending=False)
                
                # Retrieving <num_tracks> tracks from sorted list
                ordered_genre_tracks = sorted_df[['artist_name', 'track_id', 'track_m_id', 'track_name', 'm_genre_id', 'm_genre', genre_name]].values.tolist()        
                ordered_genre_tracks = [[artist_name, int(track_id), int(track_m_id), track_name, int(m_genre_id), m_genre, value, ] for artist_name, track_id, track_m_id, track_name, m_genre_id, m_genre, value in ordered_genre_tracks][:num_tracks]
                            
                for artist_name, track_id, track_m_id, track_name, m_genre_id, m_genre, value in ordered_genre_tracks:
                    if value > 1:
                        value = value / 100
                    track_info = {                
                        "track_id": track_id,
                        "track_m_id": track_m_id,
                        "track_name": track_name,
                        "artist_name": artist_name,
                        "m_genre_id": m_genre_id,
                        "m_genre": m_genre,
                        "score": float(value)
                }
                    genre_tracks_2.append(track_info)
                    print("track_id: {}, track_m_id: {}, value: {}, genre: {}".format(track_id, track_m_id, value, m_genre))
                genre_tracks_2 = [track for track in genre_tracks_2 if track['m_genre'] == genre]
        recommended_list = genre_tracks_1 + genre_tracks_2                        
    except Exception as e: 
        print({"error": str(e)})
        err = {"error": str(e)}
        return [], err    
    o_recommend = sorted(recommended_list, key=lambda item: item["score"], reverse=True)
    return o_recommend[:num_tracks], None


def get_emotion_tracks(emotion, genres, num_tracks=40):
    """Function to retrieve recommended tracks of given emotion

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
                ordered_emotion_tracks = shuffled_df[['artist_name', 'm_genre_id', 'm_genre', 'track_id', 'track_m_id', 'track_name', emotion_name]].values.tolist()
                ordered_emotion_tracks = [[artist_name, int(m_genre_id), m_genre, int(track_id), int(track_m_id), track_name, value] for artist_name, m_genre_id, m_genre, track_id, track_m_id, track_name, value in ordered_emotion_tracks][:num_tracks]

                # print("Top {} {} songs:".format(num_tracks, emotion_name))
                for artist_name, m_genre_id, m_genre, track_id, track_m_id, track_name, value in ordered_emotion_tracks:
                    track_info = {                
                            "track_id": track_id,
                            "track_m_id": track_m_id,
                            "track_name": track_name,
                            "artist_name": artist_name,
                            "m_genre_id": m_genre_id,
                            "m_genre": m_genre,
                            "score": float(value)
                    }

                    if m_genre in genres:
                        emotion_tracks.append(track_info)
        recommended_list = recommended_list + emotion_tracks

    except Exception as e: 
        print({"error": str(e)})
        err = {"error": str(e)}
        return [], err
    return recommended_list, None


def get_tracks_by_emotion(emotion, genres, num_tracks=40):
    """Function to retrieve recommended tracks of given emotion

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
        ordered_emotion_tracks = selected_list[['artist_name', 'm_genre_id', 'm_genre', 'track_id', 'track_m_id', 'track_name']].values.tolist()
        ordered_emotion_tracks = [[artist_name, int(m_genre_id), m_genre, int(track_id), int(track_m_id), track_name] for artist_name, m_genre_id, m_genre, track_id, track_m_id, track_name in ordered_emotion_tracks][:num_tracks]

        # print("Top {} {} songs:".format(num_tracks, emotion_name))
        for artist_name, m_genre_id, m_genre, track_id, track_m_id, track_name in ordered_emotion_tracks:
            track_info = {                
                "track_id": track_id,
                "track_m_id": track_m_id,
                "track_name": track_name,
                "artist_name": artist_name,
                "m_genre_id": m_genre_id,
                "m_genre": m_genre,
                "score": float(1)
            }
            
            if m_genre in genres:
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
        track_genre = df_tracks[df_tracks['track_m_id'] == int(track_id)]['m_genre'].values[0]
        # print("found genre for track_m_id {} : {} ".format(track_id, df_tracks[df_tracks['track_m_id'] == int(track_id)]))
        if track_genre == None:
            raise IndexError("No genre found for track_m_id {}".format(track_id))
        return track_genre
    except IndexError as e:
        print("No genre found for track_m_id {} : {}".format(track_id, e))
    except Exception as e: 
        print({"error": str(e)})
        err = {"error": str(e)}
        raise err
