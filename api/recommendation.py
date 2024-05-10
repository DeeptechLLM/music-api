from flask import Blueprint, request, make_response
from services.recommendation_service import get_recommendation_svc
from marshmallow import Schema, fields, ValidationError

class RecommendationSchema(Schema):
    artist_ids = fields.List(fields.Integer)
    song_ids = fields.List(fields.Integer)
    emotion_ids = fields.List(fields.Integer)
    genre_ids = fields.List(fields.Integer)
    limit = fields.Integer()

recommendation_route = Blueprint('recommendation_route', __name__)

@recommendation_route.route('/api/v1/recommendations', methods=['POST'])
def get_recommendation():
    # Extract parameters from request body
    
    request_data = request.get_json()    
    schema = RecommendationSchema()
    
    try:
        data = schema.load(request_data)
    except ValidationError as e:
        return make_response({'message': str(e)}, 400)
    
    
    artist_ids = data.get('artist_ids', [])  # Handle optional parameters with defaults    
    song_ids = data.get('song_ids', [])
    emotion_ids = data.get('emotion_ids', [])
    genre_ids = data.get('genre_ids', [])
    # limit = data.get('limit', 10)  # Default limit of 10
    
    try:        
        result = get_recommendation_svc(artist_ids, song_ids, emotion_ids, genre_ids)
        return make_response({'message': 'success', 'tracks': result}, 201)
    except Exception as e:
        return make_response({'message': str(e)}, 404)    

        

