from flask import Blueprint, request
from services.track_service import get_trackbysimilarity_svc, get_trackbysimilarity1_svc
from services.recommendation_service import get_recommendation_svc
import json

import pandas as pd

track_route = Blueprint('track_route', __name__)

# @track_route.route('/api/v1/recommendations', methods=['POST'])
# def get_recommendation():
#     return get_recommendation_svc()

# @track_route.before_request
# def before_req():
#     params = request.view_args
#     track_id_param = params["track_id"]

@track_route.route('/api/v1/track/recommendbysimilarity/<track_id>', methods=['GET'])
def get_track_by_similarity(track_id):
    
    return get_trackbysimilarity_svc(track_id)

@track_route.route('/api/v1/track/recommendbysimilarity1/<track_name>', methods=['GET'])
def get_track_by_similarity1(track_name):
    
    return get_trackbysimilarity1_svc(track_name)