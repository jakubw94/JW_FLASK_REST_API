from datetime import date

### VALIDATORS FOR API ENDPOINTS #######################################################################################
########################################################################################################################

def register(data: dict) -> bool:
    """ Validates json body data for register endpoint """
    required_fields = {"name", "last_name", "email", "password"}
    # Basic required fields check #
    if not (isinstance(data, dict) and "name" in data and "last_name" in data and "email" in data
            and "password" in data and set(data) == required_fields):
        return False
    # Data type check #
    if not (isinstance(data["name"], str) and isinstance(data["last_name"], str) and isinstance(data["email"], str)
            and isinstance(data["password"], str)):
        return False
    # Data length check #
    if not (len(data["name"]) > 2 and len(data["last_name"]) > 2 and len(data["password"]) >= 4):
        return False
    # Email format check #
    if not ("@" in data["email"] and len(data["email"].split("@")) == 2 and data["email"][0] != "@" and
            data["email"][-1] != "@" and data["email"][0] != "." and data["email"][-1] != "." and
            data["email"].count("@") == 1 and "." in data["email"].split("@")[1] and
            data["email"].split("@")[1][0] != "."):
        return False
    return True

def login(data: dict) -> bool:
    """ Validates json body data for login endpoint """
    required_fields = {"email", "password"}
    # Basic required fields check #
    if not (isinstance(data, dict) and "email" in data and "password" in data and set(data) == required_fields):
        return False
    # Data type check #
    if not (isinstance(data["email"], str) and isinstance(data["password"], str)):
        return False
    return True

def rooms(data: dict) -> bool:
    """ Validates json body data for add new room endpoint """
    required_fields = {"type", "price"}
    # Basic required fields check #
    if not (isinstance(data, dict) and "type" in data and "price" in data and set(data) == required_fields):
        return False
    # Data type check #
    if not (isinstance(data["type"], int) and isinstance(data["price"], int)
            and data["type"] in (1, 2, 3) and data["price"] > 0):
        return False
    return True

def reservations(data: dict) -> bool:
    """ Validates json body data for make reservation endpoint """
    required_fields = {"user_id", "room_id", "start_date", "end_date"}
    # Basic required fields check #
    if not (isinstance(data, dict) and "user_id" in data and "room_id" in data and "start_date" in data
            and "end_date" in data and set(data) == required_fields):
        return False
    # Data type check #
    if not (isinstance(data["user_id"], (str, int)) and isinstance(data["room_id"], (str, int))
            and isinstance(data["start_date"], str) and isinstance(data["end_date"], str)):
        return False
    # Convert id to int and date str to date and checks if start_date < end_date #
    try:
        data["user_id"] = int(data["user_id"])
        data["room_id"] = int(data["room_id"])
        data["start_date"] = date.fromisoformat(data["start_date"])
        data["end_date"] = date.fromisoformat(data["end_date"])
        if data["end_date"] > data["start_date"]:
            return True
        return False
    except Exception:
        return False

def free_rooms(data: dict) -> bool:
    """ Validates json body data for get free rooms endpoint """
    required_fields = {"start_date", "end_date"}
    required_fields_opt = {"start_date", "end_date", "type"}
    # Basic required fields check #
    if not (isinstance(data, dict) and "start_date" in data and "end_date" in data and
            (set(data) == required_fields or set(data) == required_fields_opt)):
        return False
    # Data type check #
    if not (isinstance(data["start_date"], str) and isinstance(data["end_date"], str)):
        return False
    # Convert date str to date and checks if start_date < end_date #
    try:
        # OPTIONAL - checking type parameter and converting to int #
        if isinstance(data.get("type"), (str, int)):
            data["type"] = int(data["type"])
            if not data["type"] in (1, 2, 3):
                return False
        data["start_date"] = date.fromisoformat(data["start_date"])
        data["end_date"] = date.fromisoformat(data["end_date"])
        if data["end_date"] > data["start_date"]:
            return True
        return False
    except Exception:
        return False

def room_status(data: dict) -> bool:
    """ Validates if correct data in json - "active" as bool """
    required_fields = {"active"}
    # Basic required fields check #
    if not (isinstance(data, dict) and "active" in data and set(data) == required_fields):
        return False
    # Data type check #
    if not isinstance(data["active"], bool):
        return False
    return True

########################################################################################################################
########################################################################################################################