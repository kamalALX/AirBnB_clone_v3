#!/usr/bin/python3
""" view for place object """
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieve list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieve a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Create a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if 'name' not in data:
        abort(400, description="Missing name")
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def places_search():
    if not request.is_json:
        abort(400, 'Not a JSON')
    all_places = storage.all(Place)
    list_places = [place.to_dict() for place in all_places]
    json_in = request.get_json(silent=True)
    if not json_in:
        return jsonify(list_places)
    states_id_list = cities_id_list = amenities_id_list = None
    try:
        states_id_list = json_in['states']
        cities_id_list = json_in['cities']
        amenities_id_list = json_in['amenities']
    except KeyError:
        pass

    if not states_id_list and not cities_id_list and not amenities_id_list:
        return jsonify(list_places)

    city_list = []
    if states_id_list:
        for state_id in states_id_list:
            state = storage.get(State, state_id)
            city_list_temp = [city for city in state.cities]
            city_list.extend(city_list_temp)
    if cities_id_list:
        for city_id in cities_id_list:
            city = storage.get(City, city_id)
            city_list.append(city)
    places_list = []
    for city in city_list:
        places_list.extend([place for place in city.places])
    if amenities_id_list:
        amenities_list = []
        for amenity_id in amenities_id_list:
            amenity = storage.get(Amenity, amenity_id)
            amenities_list.append(amenity)
        for place in places_list:
            for amenity in amenities_list:
                if amenity not in place.amenities:
                    places_list.remove(place)

    return jsonify([place.to_dict() for place in places_list])


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Update a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignored_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(place, key, value)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)
