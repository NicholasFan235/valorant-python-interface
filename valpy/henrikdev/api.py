import requests
import json

url = "https://api.henrikdev.xyz"

def get(endpoint):
    response = requests.get(endpoint)
    if not response.ok:
        print(response.content)
    return response

def get_json(endpoint):
    return get(endpoint).json()

def get_player(name, tag):
    endpoint = f'{url}/valorant/v1/account/{name}/{tag}'
    return get_json(endpoint)

def get_matches(region, name, tag, **kwargs):
    query = '&'.join(f'{k}={v}' for k,v in kwargs.items())
    endpoint = f'{url}/valorant/v3/matches/{region}/{name}/{tag}'
    if query != '': endpoint += '?'+query
    return get_json(endpoint)

def get_lifetime_matches(region, name, tag, **kwargs):
    query = '&'.join(f'{k}={v}' for k,v in kwargs.items())
    endpoint = f'{url}/valorant/v1/lifetime/matches/{region}/{name}/{tag}'
    if query != '': endpoint += '?'+query
    return get_json(endpoint)

def get_match(match_id):
    endpoint = f'{url}/valorant/v2/match/{match_id}'
    return get_json(endpoint)
