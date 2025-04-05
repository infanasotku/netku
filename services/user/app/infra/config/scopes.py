import os
import json
from enum import Enum


class Scopes(Enum):
    UsersWrite = ""
    UsersRead = ""


def _generate_scopes() -> Scopes:
    path = os.getcwd() + "/scopes.json"
    with open(path, "r") as f:
        data = json.loads(f.read())

    class Scopes(Enum):
        UsersWrite = data["UsersWrite"]
        UsersRead = data["UsersRead"]

    return Scopes


Scopes = _generate_scopes()
