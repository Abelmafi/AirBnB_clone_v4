#!/usr/bin/python3
"""Creating restfull api"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.base_model import BaseModel


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def states(state_id=None):
    """Creates State objects that handles all default RESTFul API"""

    from models.state import State
    state_obj = storage.all(State)

    if request.method == 'GET':
        if state_id is None:
            return jsonify([obj.to_dict() for obj in state_obj.values()])
        else:
            ids = [key.split('.')[1] for key in state_obj]
            if state_id not in ids:
                abort(404)
            else:
                key = 'State.' + state_id
                return jsonify(state_obj[key].to_dict())

    elif request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            abort(400, 'Not a JSON')
        else:
            body_json = request.get_json()
            if 'name' not in body_json:
                abort(400, 'Missing name')
            else:
                new_state = State(**body_json)
                storage.new(new_state)
                storage.save()
                return jsonify(new_state.to_dict()), 201

    elif request.method == 'PUT':
        ids = [key.split('.')[1] for key in state_obj]
        if state_id not in ids:
            abort(404)
        else:
            content_type = request.headers.get('Content-Type')
            if content_type != 'application/json':
                abort(400, 'Not a JSON')
            else:
                body_json = request.get_json()
                keyy = 'State.' + state_id
                found_state = state_obj[keyy]
                for key, value in body_json.items():
                    if key not in ['created_at', 'updated_at', 'id']:
                        setattr(found_state, key, value)
                storage.save()
                return jsonify(found_state.to_dict()), 200

    elif request.method == 'DELETE':
        ids = [val.split('.')[1] for val in state_obj]
        if state_id in ids:
            key = 'State.' + state_id
            storage.delete(state_obj[key])
            storage.save()
            return jsonify({}), 200

        else:
            abort(404)

    else:
        abort(501)
