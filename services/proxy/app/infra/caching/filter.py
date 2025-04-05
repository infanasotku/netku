from typing import Any
import re


def create_egnine_keys_filter(engnine_key_pattern: str):
    def filtrate_engine_keys(msg: dict[str, Any]) -> bool:
        m = re.match(engnine_key_pattern, msg["data"])
        return False if m is None else True

    return filtrate_engine_keys
