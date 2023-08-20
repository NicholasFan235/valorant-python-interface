import requests

maps = None
def retrieve_maps():
    global maps
    maps = {}
    r = requests.get('https://valorant-api.com/v1/maps')
    r.raise_for_status()
    for map in r.json()['data']:
        maps[map['uuid']] = map['displayName']
        maps[map['mapUrl']] = map['displayName']

def get_map_name(map):
    global maps
    if maps is None: retrieve_maps()
    if map in maps: return maps[map]
    else: return map


class Match:
    def __init__(self, match_id, season_id, game_version,
                 map, start_time, game_length, rounds_played, outcome,
                 queue):
        self.match_id, self.season_id = match_id, season_id
        self.game_version = game_version
        self.map = get_map_name(map)
        self.start_time = start_time
        self.game_length, self.rounds_played, self.outcome = game_length, rounds_played, outcome
        self.queue = queue
        self.rounds = []
        self.players = []
        self.kills = []

