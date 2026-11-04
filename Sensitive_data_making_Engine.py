"""Mask selected fields in JSON-like dictionaries and lists."""
import json
from typing import Any, Dict, Iterable, List, Union

JsonType = Union[Dict[str, Any], List[Any], str, int, float, bool, None]
MASK = "********"


def mask_sensitive_data(data: JsonType, target_keys: Iterable[str]) -> JsonType:
    """Return a new structure with case-insensitively matched fields masked.

    Keys match exactly after case folding. Matching values are replaced entirely,
    including dictionaries and lists. Unselected values remain visible.
    Input must be acyclic JSON-like data with string dictionary keys.
    """
    if isinstance(target_keys, (str, bytes)):
        raise TypeError("target_keys must be an iterable of key names, not a string")
    names = list(target_keys)
    if any(not isinstance(key, str) for key in names):
        raise TypeError("Each target key must be a string")
    sensitive = frozenset(key.casefold() for key in names)

    def walk(value: JsonType) -> JsonType:
        if isinstance(value, dict):
            return {
                key: MASK if key.casefold() in sensitive else walk(item)
                for key, item in value.items()
            }
        if isinstance(value, list):
            return [walk(item) for item in value]
        return value

    return walk(data)


def main() -> None:
    """Print a masked demonstration using synthetic example values only."""
    payload = {
        "user_id": 1,
        "profile": {
            "first_name": "Example",
            "last_name": "User",
            "security": {"password": "demo-only", "pin": "0000"},
        },
        "payment_methods": [
            {"type": "example_card", "number": "demo-card-number"},
            {"type": "example_account", "email": "person@example.com"},
        ],
        "status": "active",
    }
    keys = ["password", "pin", "number", "email", "first_name", "last_name"]
    print("Masked example payload:")
    print(json.dumps(mask_sensitive_data(payload, keys), indent=2))


if __name__ == "__main__":
    main()
