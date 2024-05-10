from flask import Flask, request, jsonify
from flask_cors import CORS

import secrets  # For generating a secure secret key

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.decomposition import TruncatedSVD
from api.track import track_route
from api.recommendation import recommendation_route

from sklearn.metrics.pairwise import cosine_similarity
from sklearn import preprocessing

app = Flask(__name__)
app.register_blueprint(track_route)
app.register_blueprint(recommendation_route)

# Generate a cryptographically secure secret key (store securely outside code)
app.secret_key = secrets.token_urlsafe(32)
print(app.secret_key)

# for recommendation 
df_tracks = pd.read_csv("data/combined_tracks.csv")
df_tracks['content'] = df_tracks['genres'].astype(str) + ' ' + df_tracks['emotions'].astype(str) + ' ' + df_tracks['instrumentals'] + ' ' + df_tracks['track_name'] + ' ' + df_tracks['artist_name'] + ' ' + df_tracks['album_name'].astype(str)
df_tracks['content'] = df_tracks['content'].fillna('')
        
vectorizer = CountVectorizer()
bow = vectorizer.fit_transform(df_tracks['content'])
tfidf_transformer = TfidfTransformer()
tfidf = tfidf_transformer.fit_transform(bow)
        
lsa = TruncatedSVD(n_components=100, algorithm='arpack')
lsa.fit(tfidf)
app.config['df_tracks'] = df_tracks
app.config['tfidf'] = tfidf
app.config['lsa'] = lsa

# for recommendation-1
general_path='data'
# Read data
data = pd.read_csv(f'{general_path}/features-30sec-model1.csv', index_col='filename')

# Extract labels
labels = data[['label']]

# Drop labels from original dataframe
data = data.drop(columns=['label'])
# data.head()

# Scale the data
data_scaled=preprocessing.scale(data)
# print('Scaled data type:', type(data_scaled))

# Cosine similarity
similarity = cosine_similarity(data_scaled)
# print("Similarity shape:", similarity.shape)

# Convert into a dataframe and then set the row index and column names as labels
sim_df_labels = pd.DataFrame(similarity)
sim_df_names = sim_df_labels.set_index(labels.index)
sim_df_names.columns = labels.index

app.config['sim_df_names'] = sim_df_names

CORS(app)

# # Replace with your recommendation logic
# def recommend_track(track_id):
#     # Simulate a recommendation based on the provided track_id
#     # (You'll likely replace this with your actual recommendation engine)
#     recommended_track_id = f"1{track_id}"
#     return recommended_track_id

# @app.errorhandler(400)  # Handle bad request errors
# def bad_request(error):
#     return jsonify({'error': str(error)}), 400

# @app.errorhandler(401)  # Handle unauthorized access errors
# def unauthorized(error):
#     return jsonify({'error': str(error)}), 401

# @app.errorhandler(404)  # Handle resource not found errors
# def not_found(error):
#     return jsonify({'error': str(error)}), 404

# @app.route('/v1/recommend', methods=['GET'])
# def recommend():
#     # Validate request data
#     if request.method != 'GET' or not request.is_json:
#         return jsonify({'error': 'Invalid request'}), 400

#     # Check for the presence of the track_id field
#     data = request.get_json()
#     if 'track_id' not in data:
#         return jsonify({'error': 'Missing required field: track_id'}), 400

#     # Validate the secret key (if using client-side secret)
#     # For production environments, consider more robust authentication mechanisms
#     # like token-based authorization
#     # if 'secret_key' not in data or data['secret_key'] != app.secret_key:
#     #     return jsonify({'error': 'Invalid secret key'}), 401

#     track_id = data['track_id']
#     recommended_track_id = recommend_track(track_id)

#     return jsonify({'recommended_track_id': recommended_track_id})

if __name__ == '__main__':
    app.run(debug=True)