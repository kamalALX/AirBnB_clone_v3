from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['Get'])
def get_status():
    """Endpoint to check the status of the API"""
    status = {"status": "OK"}
    return jsonify(status)
