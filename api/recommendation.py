from flask import Blueprint, request, make_response
from services.recommendation_service import get_recommendation_svc
import json

import pandas as pd

recommendation_route = Blueprint('recommendation_route', __name__)

@recommendation_route.route('/api/v1/recommendations', methods=['POST'])
def get_recommendation():
    # Extract parameters from request body
    
    data = request.get_json()    
    artist_ids = data.get('artists_ids', [])  # Handle optional parameters with defaults    
    song_ids = data.get('songs_ids', [])
    emotions_id = data.get('emotions_ids', [])
    genres_id = data.get('genres_ids', [])
    # limit = data.get('limit', 10)  # Default limit of 10
    
    # Validation
    
    try:        
        result = get_recommendation_svc(artist_ids, song_ids, emotions_id, genres_id)
        return make_response({'message': 'success', 'tracks': result}, 201)
    except Exception as e:
        return make_response({'message': str(e)}, 404)
    

# @track_route.before_request
# def before_req():
#     params = request.view_args
#     track_id_param = params["track_id"]

