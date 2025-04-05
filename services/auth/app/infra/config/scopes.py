import os
import json
from enum import Enum


class Scopes(Enum):
    AuthRead = ""


def _generate_scopes() -> Scopes:
    path = os.getcwd() + "/scopes.json"
    with open(path, "r") as f:
        data = json.loads(f.read())

    class Scopes(Enum):
        AuthRead = data["AuthRead"]

    return Scopes


Scopes = _generate_scopes()
