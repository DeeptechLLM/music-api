from flask import Blueprint, request
from services.track_service import get_trackbysimilarity_svc, get_trackbysimilarity1_svc

import pandas as pd

track_route = Blueprint('track_route', __name__)

@track_route.route('/api/v1/track/recommendbysimilarity/<track_id>', methods=['GET'])
def get_track_by_similarity(track_id):
    
    return get_trackbysimilarity_svc(track_id)

@track_route.route('/api/v1/track/recommendbysimilarity1/<track_name>', methods=['GET'])
def get_track_by_similarity1(track_name):
    
    return get_trackbysimilarity1_svc(track_name)