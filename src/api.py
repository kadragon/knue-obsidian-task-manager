import requests


def api_request(query: str) -> dict:
    """
    Send a GET request to the university's API and return the JSON response.

    Args:
        query (str): Search term for API query.

    Returns:
        dict: JSON response from API.
    """
    params = {
        "mode": "search",
        "type": "2",
        "name": query
    }

    try:
        response = requests.get(
            "https://knue.ac.kr/findphone/api.php", params=params)
        return response.json()
    except Exception:
        pass
