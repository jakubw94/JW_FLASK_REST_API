from flask import request, jsonify
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from database import get_user_role

### DECORATORS FOR ENDPOINTS ###########################################################################################
########################################################################################################################

def check_if_json():
    """ Checking if valid json body in POST and PATCH requests """
    if request.method in ("POST", "PATCH"):
        if not request.is_json:
            return jsonify({"error": "Request header Content-Type must be application/json"}), 415
        try:
            data = request.get_json()
            if data is None:
                return jsonify({"error": "Ivalid or empty JSON body"}), 400
        except Exception:
            return jsonify({"error": "Invalid JSON"}), 400

def admin_required(func):
    """ Validates if user is admin - jwt_required before """
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        role = get_user_role(user_id)
        if role == "admin":
            return func(*args, **kwargs)
        return jsonify({"status": False, "data": None}), 403
    return wrapper

def validate_json(validator_func, add_user_id=False):
    """ Adding validation data fuctions as decorators """
    def decorator(endpoint_func):
        @wraps(endpoint_func)
        def wrapper(*args, **kwargs):
            if request.method in ("POST", "PATCH"):
                data = request.get_json()
                if add_user_id:
                    data["user_id"] = get_jwt_identity()
                validated = validator_func(data)
                if validated:
                    return endpoint_func(data, *args, **kwargs)
                else:
                    return jsonify({"status": False, "data": None}), 400
        return wrapper
    return decorator

def validate_query_args(validator_func, add_user_id=False):
    """ Adding validation data fuctions as decorators """
    def decorator(endpoint_func):
        @wraps(endpoint_func)
        def wrapper(*args, **kwargs):
            if request.method == "GET":
                data = request.args.to_dict()
                if add_user_id:
                    data["user_id"] = get_jwt_identity()
                validated = validator_func(data)
                if validated:
                    return endpoint_func(data, *args, **kwargs)
                else:
                    return jsonify({"status": False, "data": None}), 400
        return wrapper
    return decorator

def no_query_args(func):
    """ Not allowing query parameters """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.args.to_dict():
            return jsonify({"status": False, "data": None}), 400
        else:
            return func(*args, **kwargs)
    return wrapper

def no_json(func):
    """ Not allowing json data """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.is_json:
            return jsonify({"status": False, "data": None}), 400
        else:
            return func(*args, **kwargs)
    return wrapper

########################################################################################################################
########################################################################################################################