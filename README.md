# Sensitive Data Masking Engine

A small Python utility that recursively masks selected fields in dictionaries and lists without modifying the original input.

## Run

Requires Python 3.6 or later. Uses only the Python standard library.

```sh
python3 Sensitive_data_making_Engine.py
```

The demo uses synthetic data and prints only the masked payload. The existing source filename is preserved for compatibility.

## Use in your code

```python
from Sensitive_data_making_Engine import mask_sensitive_data

payload = {
    "profile": {"Password": "demo-only"},
    "accounts": [{"email": "person@example.com"}],
    "status": "active",
}
masked = mask_sensitive_data(payload, ["PASSWORD", "email"])
# {"profile": {"Password": "********"},
#  "accounts": [{"email": "********"}], "status": "active"}
```

## Behavior

- Matches field names exactly, ignoring case in both input keys and target rules.
- Traverses nested dictionaries and lists, copying their containers.
- Replaces the whole matching value with `********`, regardless of its type.
- Leaves unselected fields and primitive values visible.
- Normalizes the target rules once; generators are supported.
- Rejects a bare string or non-string target key with `TypeError`.

Select all fields that require masking for your use case. This is a configurable field masker, not automatic personal-data detection, encryption, or a guarantee that an entire payload is safe to log. It expects acyclic JSON-like data with string keys; deeply nested inputs are subject to Python's recursion limit.

## Checks

```sh
python3 -m unittest -v test_masking.py
```

Checks cover nested lists, mixed-case rules, independent input containers, whole-field replacement, exact matching, primitive values, generator rules, and invalid rules.
