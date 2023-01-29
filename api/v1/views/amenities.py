#!/usr/bin/python3
"""Creates a RESTFul API for Amenity"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.base_model import BaseModel


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def amenity(amenity_id=None):
    """Amenity RESTFul API"""
    from models.amenity import Amenity
    amenity_obj = storage.all(Amenity)

    if request.method == 'GET':
        if amenity_id:
            ids = [key.split('.')[1] for key in amenity_obj]
            if amenity_id not in ids:
                abort(404)
            else:
                key = 'Amenity.' + amenity_id
                return (amenity_obj[key].to_dict())
        else:
            return jsonify([value.to_dict() for value in amenity_obj.values()])

    elif request.method == 'POST':
        amenity_json = request.get_json()
        if request.is_json:
            if 'name' not in amenity_json:
                abort(400)
            else:
                new_amenity = Amenity(**amenity_json)
                storage.new(new_amenity)
                storage.save()
                return (new_amenity.to_dict()), 201
        else:
            abort(400, 'Not a JSON')

    elif request.method == 'DELETE':
        ids = [key.split('.')[1] for key in amenity_obj]

        if amenity_id in ids:
            key = "Amenity." + amenity_id
            storage.delete(amenity_obj[key])
            storage.save()
            return {}, 200
        else:
            abort(404)

    elif request.method == 'PUT':
        ids = [key.split('.')[1] for key in amenity_obj]

        if amenity_id in ids:
            key = 'Amenity.' + amenity_id
            target_obj = amenity_obj[key]
            amenity_json = request.get_json()
            if not request.is_json:
                abort(400, 'Not a JSON')
            else:
                for key, value in amenity_json.items():
                    if key not in ['id', 'created_at', 'updated_at']:
                        setattr(target_obj, key, value)
                storage.save()
                return (target_obj.to_dict()), 200
        else:
            abort(404)

    else:
        abort(501)
