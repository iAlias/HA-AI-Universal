import requests


def post_json(url, data, headers=None, timeout=60):
    """Make a POST request with JSON data."""
    response = requests.post(url, json=data, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response.json()
