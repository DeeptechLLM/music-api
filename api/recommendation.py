from flask import Blueprint, request, make_response
from services.recommendation_service import get_recommendation_svc
from marshmallow import Schema, fields, ValidationError

class RecommendationSchema(Schema):

    artist_ids = fields.List(fields.Integer)
    song_ids = fields.List(fields.Integer)
    emotions = fields.List(fields.String(), required=False)
    genres = fields.List(fields.String(), required=False)
    # type = fields.String()
    limit = fields.Integer()

# Route
recommendation_route = Blueprint('recommendation_route', __name__)

# /api/v1/recommendations
@recommendation_route.route('/api/v1/recommendations', methods=['POST'])
def get_recommendation():
    
    # Validate and extract parameters from request body    
    request_data = request.get_json()
    schema = RecommendationSchema()
    
    try:        
        data = schema.load(request_data)        
    except ValidationError as e:
        return make_response({'message': str(e)}, 400)    
    
    artist_ids = data.get('artist_ids', [])  # Handle optional parameters with defaults    
    song_ids = data.get('song_ids', [])
    emotions = data.get('emotions', [])
    genres = data.get('genres', [])
    # model_type = data.get('type', "normal")
    # limit = data.get('limit', 10)  # Default limit of 10
    
    try:      
        
        result = get_recommendation_svc(artist_ids, song_ids, emotions, genres)
        # print("got result", result)
        return make_response({'message': 'success', 'tracks': result}, 201)
    except Exception as e:
        return make_response({'message': str(e)}, 404)


        

