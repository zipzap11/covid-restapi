import requests

URL = "https://data.covid19.go.id/public/api/update.json"


def fetch_data():
    resp = requests.get(url=URL)
    if not resp.ok:
        raise "error"
    data = resp.json()
    return data


DATA = fetch_data()
