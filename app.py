from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from datetime import timedelta, date
from dotenv import load_dotenv
load_dotenv()
import os
import database as db
import validators
from werkzeug.security import generate_password_hash, check_password_hash
from decorators import check_if_json, admin_required, validate_json, validate_query_args, no_query_args, no_json

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)
jwt = JWTManager(app)

app.before_request(check_if_json) # <--- Checking if valid json body in POST and PATCH requests

### API RESPONSE SCHEME: {"status": True/False, "data": ...} ###

### API ENDPOINTS ######################################################################################################
########################################################################################################################

@app.post("/api/register") # <--- CREATE ACCOUNT, json: {"name": ..., "last_name": ..., "password": ..., "email": ...}
@validate_json(validators.register)
def create_account(data):
    data["password"] = generate_password_hash(data["password"])
    created = db.create_account(**data)
    if created:
        return jsonify({"status": True, "data": None}), 201
    elif created is None:
        return jsonify({"status": False, "data": None}), 409
    else:
        return jsonify({"status": False, "data": None}), 500

########################################################################################################################

@app.post("/api/login") # <--- LOGIN, json: {"email": ..., "password": ...}
@validate_json(validators.login)
def login(data):
    user_data = db.get_login_data(data["email"])
    if user_data:
        if check_password_hash(user_data["password"], data["password"]):
            access_token = create_access_token(identity=str(user_data["id"])) # <--- Creating token with user_id
            return jsonify({"status": True, "data": {"access_token": access_token}}), 200
        else:
            return jsonify({"status": False, "data": None}), 401
    elif user_data is False:
        return jsonify({"status": False, "data": None}), 500
    else:
        return jsonify({"status": False, "data": None}), 401

########################################################################################################################

@app.post("/api/reservations") # <--- BOOKING, json {"user_id": ..., "room_id": ..., "start_date": ..., "end_date": ...}
@jwt_required()
@validate_json(validators.reservations, add_user_id=True)
def add_reservation(data):
    added = db.add_reservation(**data)
    if added:
        return jsonify({"status": True, "data": None}), 201
    elif added is None:
        return jsonify({"status": False, "data": None}), 409
    else:
        return jsonify({"status": False, "data": None}), 500

########################################################################################################################

@app.get("/api/rooms") # <--- GET FREE ROOMS IN SELECTED TIME PERIOD, query params: start_date, end_date, type(None/int)
@jwt_required()
@validate_query_args(validators.free_rooms)
def get_free_rooms(data):
    rooms = db.get_free_rooms(**data)
    if rooms is not False:
        return jsonify({"status": True, "data": rooms}), 200
    else:
        return jsonify({"status": False, "data": None}), 500

########################################################################################################################

@app.delete("/api/reservations/<int:reservation_id>") # <--- DELETE RESERVATION
@jwt_required()
@no_json
def delete_reservation(reservation_id):
    deleted = db.delete_reservation(reservation_id, get_jwt_identity())
    if deleted:
        return jsonify({"status": True, "data": None}), 200
    else:
        return jsonify({"status": False, "data": None}), 500

########################################################################################################################

@app.get("/api/reservations") # <--- GET USER RESERVATIONS
@jwt_required()
@no_query_args
def get_user_reservations():
    reservations = db.get_user_reservations(get_jwt_identity())
    if reservations is not False:
        return jsonify({"status": True, "data": reservations}), 200
    else:
        return jsonify({"status": False, "data": None}), 500

########################################################################################################################

@app.get("/api/users/role") # <--- GET USER ROLE: "user"/"admin"
@jwt_required()
@no_query_args
def get_user_role():
    role = db.get_user_role(get_jwt_identity())
    if role:
        return jsonify({"status": True, "data": {"role": role}}), 200
    else:
        return jsonify({"status": False, "data": None}), 500

### ADMIN ENDPOINTS ####################################################################################################

@app.patch("/api/rooms/<int:room_id>") # <--- CHANGE ROOM STATUS, json: {"active": True/False}
@jwt_required()
@admin_required
@validate_json(validators.room_status)
def change_room_status(data, room_id):
    changed = db.change_room_status(room_id, data["active"])
    if changed:
        return jsonify({"status": True, "data": None}), 200
    else:
        return jsonify({"status": False, "data": None}), 500

########################################################################################################################

@app.post("/api/rooms") # <--- ADD NEW ROOM, json {"type": ..., "price": ...}
@jwt_required()
@admin_required
@validate_json(validators.rooms)
def add_room(data):
    added = db.add_room(data["type"], data["price"])
    if added:
        return jsonify({"status": True, "data": None}), 201
    else:
        return jsonify({"status": False, "data": None}), 500

########################################################################################################################

@app.get("/api/reservations/all") # <--- GET ALL RESERVATIONS
@jwt_required()
@admin_required
@no_query_args
def get_all_reservations():
    reservations = db.get_all_reservations()
    if reservations is not False:
        return jsonify({"status": True, "data": reservations}), 200
    else:
        return jsonify({"status": False, "data": None}), 500

########################################################################################################################

@app.get("/api/rooms/all") # <--- GET ALL ROOMS
@jwt_required()
@admin_required
@no_query_args
def get_all_rooms():
    rooms = db.get_all_rooms()
    if rooms is not False:
        return jsonify({"status": True, "data": rooms}), 200
    else:
        return jsonify({"status": False, "data": None}), 500

########################################################################################################################
########################################################################################################################

### RENDERING HTML SPA ##########################
@app.get("/")
def index():
    return render_template("index_deepseek.html")
#################################################

### RUNNING APP ############
if __name__ == "__main__":
    app.run(debug=True)