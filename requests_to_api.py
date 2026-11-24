### TESTING PURPOSES ###################################################################################################
########################################################################################################################

import requests
from datetime import date

### Log-in to get token ###
token = "..."
###########################

headers = {
    "Authorization": f"Bearer {token}"
}

def create_account(name, last_name, email, password):
    data = {"name": name, "last_name": last_name, "email": email, "password": password}
    response = requests.post("http://127.0.0.1:5000/api/register", json=data)
    print(response.json(), response.status_code)

def login(email, password):
    data = {"email": email, "password": password}
    response = requests.post("http://127.0.0.1:5000/api/login", json=data)
    print(response.json(), response.status_code)

def add_room(type, price):
    data = {"type": type, "price": price}
    response = requests.post("http://127.0.0.1:5000/api/rooms", json=data, headers=headers)
    print(response.json(), response.status_code)

def make_reservation(room_id, start_date, end_date):
    data = {"room_id": room_id, "start_date": start_date, "end_date": end_date}
    response = requests.post("http://127.0.0.1:5000/api/reservations", json=data, headers=headers)
    print(response.json(), response.status_code)

def get_free_rooms(start_date, end_date, type=None):
    data = {"start_date": start_date, "end_date": end_date, "type": type}
    response = requests.get("http://127.0.0.1:5000/api/rooms", params=data, headers=headers)
    print(response.json(), response.status_code)

def delete_reservation(id):
    response = requests.delete(f"http://127.0.0.1:5000/api/reservations/{id}", headers=headers)
    print(response.json(), response.status_code)

def change_room_status(id, if_active):
    data = {"active": if_active}
    response = requests.patch(f"http://127.0.0.1:5000/api/rooms/{id}", json=data, headers=headers)
    print(response.json(), response.status_code)

def get_user_reservations():
    response = requests.get("http://127.0.0.1:5000/api/reservations", headers=headers)
    print(response.json(), response.status_code)

def get_all_rooms():
    response = requests.get("http://127.0.0.1:5000/api/rooms/all", headers=headers)
    print(response.json(), response.status_code)

def get_all_reservations():
    response = requests.get("http://127.0.0.1:5000/api/reservations/all", headers=headers)
    print(response.json(), response.status_code)

def get_user_role():
    response = requests.get("http://127.0.0.1:5000/api/users/role", headers=headers)
    print(response.json(), response.status_code)

### TESTING ###########################################################
#create_account("Jan", "Kowalski", "test@test.pl", "1234")
#login("kubaw1028@gmail.com", "1234")
#add_room(1, 199)
#start = date(2025, 7, 1)
#start_s = start.isoformat()
#end = date(2025, 7, 3)
#end_s = end.isoformat()
#make_reservation(1, start_s, end_s)

#get_free_rooms(start_s, end_s, 1)
#delete_reservation(4)
#change_room_status(6, True)
#get_user_reservations()
#get_all_rooms()
#get_all_reservations()

#get_user_role()
#######################################################################