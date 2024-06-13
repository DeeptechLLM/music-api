from flask import Blueprint, request, make_response
from services.recommendation_service import get_recommendation_svc
from marshmallow import Schema, fields, ValidationError
from datetime import datetime
import uuid

class RecommendationSchema(Schema):

    song_ids = fields.List(fields.Integer)
    emotions = fields.List(fields.String(), required=False)
    genres = fields.List(fields.String(), required=False)
    type = fields.String()
    limit = fields.Integer()

# Route
recommendation_route = Blueprint('recommendation_route', __name__)

# /api/v1/recommendations
@recommendation_route.route('/api/v1/recommendations', methods=['POST'])
def get_recommendation():
    uid = uuid.uuid4()
    # Validate and extract parameters from request body    
    request_data = request.get_json()
    schema = RecommendationSchema()
    
    try:        
        data = schema.load(request_data)        
    except ValidationError as e:
        return make_response({'message': str(e)}, 400)    
    
    # Handle optional parameters with defaults    
    song_ids = data.get('song_ids', [])
    emotions = data.get('emotions', [])
    genres = data.get('genres', [])
    limit = data.get('limit', 40)
    recc_type = data.get('type', 'home')
    
    try:      
        today = datetime.now()
        result, msg = get_recommendation_svc(song_ids, emotions, genres, limit, recc_type)
        log = {"uuid": str(uid), "request": data, "response": result, "message": msg}
        with open('logs/recommendation-' + today.strftime('%Y-%b-%d_%H-%M-%S') + '.log', 'a', encoding='utf-8') as f:
            # print("log writing: ", log)
            f.write(str(log) + '\n')
        return make_response({'statusMessage': 'success', 'tracks': result, 'message': msg, 'uuid': uid}, 201)
    except Exception as e:
        return make_response({'message': str(e)}, 404)


        

