from sqlalchemy import create_engine, text, event
from datetime import date
import os

engine = create_engine("sqlite:///db.sqlite3", echo=False, future=True)

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

########################################################################################################################

def create_account(name: str, last_name: str, password: str, email: str) -> bool | None:
    """ Creating new record in users table """
    query = text("INSERT INTO users(name, last_name, password, email) VALUES (:name, :last_name, :password, :email)")
    parameters = {"name": name, "last_name": last_name, "password": password, "email": email}
    query_check = text("SELECT id FROM users WHERE email = :email")
    parameters_check = {"email": email}
    try:
        with engine.begin() as conn:
            existing_user = conn.execute(query_check, parameters_check).mappings().first()
            if existing_user:
                return None
            conn.execute(query, parameters)
        return True
    except Exception as e:
        print(e)
        return False

def get_login_data(email: str) -> dict | bool:
    """ Getting user data to verify login """
    query = text("SELECT id, password FROM users WHERE email = :email")
    parameters = {"email": email}
    try:
        with engine.connect() as conn:
            user_data = conn.execute(query, parameters).mappings().first()
            user_data = {} if user_data is None else user_data
        return user_data
    except Exception:
        return False

def add_room(type: int, price: int) -> bool:
    """ Creating new record in rooms table """
    query = text("INSERT INTO rooms(type, price) VALUES(:type, :price)")
    parameters = {"type": type, "price": price}
    try:
        with engine.begin() as conn:
            conn.execute(query, parameters)
        return True
    except Exception as e:
        print(e)
        return False

def get_free_rooms(start_date: date, end_date: date, type: int | None = None) -> list | bool:
    """ Getting list of all free rooms in searched time period """
    if type:
        query = text("SELECT * FROM rooms WHERE id NOT IN "
                     "(SELECT room_id FROM reservations WHERE end_date > :wanted_start AND start_date < :wanted_end) "
                     "AND type = :type AND active = TRUE")
        parameters = {"wanted_start": start_date, "wanted_end": end_date, "type": type}
    else:
        query = text("SELECT * FROM rooms WHERE id NOT IN "
                     "(SELECT room_id FROM reservations WHERE end_date > :wanted_start AND start_date < :wanted_end) "
                     "AND active = TRUE")
        parameters = {"wanted_start": start_date, "wanted_end": end_date}
    try:
        with engine.connect() as conn:
            rooms = [dict(row) for row in conn.execute(query, parameters).mappings().all()]
            rooms.sort(key=lambda x: x["type"])
        return rooms
    except Exception:
        return False

def add_reservation(user_id: str | int, room_id: str | int, start_date: date, end_date: date) -> bool | None:
    """ Counting total price of reservation and creating new record in reservations table """
    query_1 = text("SELECT price FROM rooms WHERE id = :room_id")
    parameters_1 = {"room_id": room_id}
    query_2 = text("INSERT INTO reservations(user_id, room_id, start_date, end_date, total_price)"
                 "VALUES(:user_id, :room_id, :start_date, :end_date, :total_price)")
    parameters_2 = {"user_id": user_id, "room_id": room_id, "start_date": start_date, "end_date": end_date}
    try:
        with engine.begin() as conn:
            # Checking if room is still free #
            rooms = get_free_rooms(start_date, end_date)
            if isinstance(rooms, list) and any(int(room["id"]) == room_id for room in rooms):
                # Making reservation
                room = conn.execute(query_1, parameters_1).mappings().first()
                parameters_2["total_price"] = (end_date - start_date).days * room["price"]
                conn.execute(query_2, parameters_2)
            else:
                return None
        return True
    except Exception:
        return False

def change_room_status(room_id: str | int, active: bool) -> bool:
    """ Changing active parameter (True/False) for room record in rooms table """
    query = text("UPDATE rooms SET active = :active WHERE id = :room_id")
    parameters = {"active": active, "room_id": room_id}
    try:
        with engine.begin() as conn:
            conn.execute(query, parameters)
        return True
    except Exception:
        return False

def get_user_reservations(user_id: int | str) -> list:
    """ Getting all user's reservations """
    query = text("SELECT reservations.*, rooms.type FROM reservations LEFT JOIN rooms ON reservations.room_id = rooms.id WHERE user_id = :user_id")
    parameters = {"user_id": user_id}
    try:
        with engine.connect() as conn:
            reservations = [dict(row) for row in conn.execute(query, parameters).mappings().all()]
        return reservations[::-1]
    except Exception:
        return False

def get_user_role(user_id: int | str) -> str | bool:
    """ Getting user role - user/admin """
    query = text("SELECT role FROM users WHERE id = :user_id")
    parameters = {"user_id": user_id}
    try:
        with engine.connect() as conn:
            role = conn.execute(query, parameters).fetchone()
        return role[0] if role is not None else False
    except Exception:
        return False

def delete_reservation(reservation_id: str | int, user_id: str | int) -> bool:
    """ Deleting reservation record from reservations table specified by id """
    role = get_user_role(user_id)
    if role == "admin":
        query = text("DELETE FROM reservations WHERE id = :reservation_id")
        parameters = {"reservation_id": reservation_id}
    else:
        query = text("DELETE FROM reservations WHERE id = :reservation_id AND user_id = :user_id")
        parameters = {"reservation_id": reservation_id, "user_id": user_id}
    try:
        with engine.begin() as conn:
            conn.execute(query, parameters)
        return True
    except Exception:
        return False

def get_all_reservations() -> list | bool:
    """ Getting all reservations """
    query = text("SELECT reservations.*, rooms.type as room_type, users.name, users.last_name, users.email FROM reservations LEFT JOIN rooms ON reservations.room_id = rooms.id LEFT JOIN users ON reservations.user_id = users.id")
    try:
        with engine.connect() as conn:
            reservations = [dict(row) for row in conn.execute(query).mappings().all()]
        return reservations[::-1]
    except Exception:
        return False

def get_all_rooms() -> list | bool:
    """ Getting all rooms """
    query = text("SELECT * FROM rooms")
    try:
        with engine.connect() as conn:
            rooms = [dict(row) for row in conn.execute(query).mappings().all()]
        return rooms
    except Exception:
        return False

########################################################################################################################
########################################################################################################################