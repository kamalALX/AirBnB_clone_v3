#!/usr/bin/python3
""" view for City objects that handles all default RESTFul API actions """
from . import app_views
from models import storage
from flask import jsonify, abort, request, make_response
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    city_list = [city.to_dict() for city in state.cities]
    return jsonify(city_list)

@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200

# @app_views.route('/states/<state_id>/cities', methods=['POST'])
# def create_city(state_id):
#     """Creates a City."""
#     state = storage.get(State, state_id)
#     if not state:
#         abort(404)
    
#     if not request.is_json:
#         return jsonify({"error": "Not a JSON"}), 400
#     data = request.get_json()
#     if 'name' not in data:
#         return jsonify({"error": "Missing name"}), 400

#     new_city = City(**data)
#     setattr(new_city, 'state_id', state_id)
#     storage.new(new_city)
#     storage.save()
#     return jsonify(new_city.to_dict()), 201

@app_views.route('/states/<string:state_id>/cities/', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """create a new city"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    kwargs = request.get_json()
    kwargs['state_id'] = state_id
    city = City(**kwargs)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)

@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Updates a City object."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()

    ignored_keys = {'id', 'state_id', 'created_at', 'updated_at'}
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(city, key, value)

    storage.save()
    return jsonify(city.to_dict()), 200
