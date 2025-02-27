import os
import json
from enum import Enum


class Scopes(Enum):
    ProxyWrite = ""
    ProxyRead = ""


def _generate_scopes() -> Scopes:
    path = os.getcwd() + "/scopes.json"
    with open(path, "r") as f:
        data = json.loads(f.read())

    class Scopes(Enum):
        ProxyWrite = data["ProxyWrite"]
        ProxyRead = data["ProxyRead"]

    return Scopes


Scopes = _generate_scopes()
