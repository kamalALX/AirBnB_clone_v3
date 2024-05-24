#!/usr/bin/python3
"""  """
from flask import jsonify
from . import app_views


@app_views.route('/status', methods=['Get'])
def get_status():
    """Endpoint to check the status of the API"""
    status = {"status": "OK"}
    return jsonify(status)
