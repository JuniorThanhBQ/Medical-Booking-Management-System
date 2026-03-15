import json
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
file_path = os.path.join(BASE_DIR, "users.json")

def login(username, password):
    with open(file_path, "r") as f:
        users = json.load(f)

    for user in users:
        if user["username"] == username and user["password"] == password:
            return user

    return None