from ._player_id import PlayerID
import requests


ranks = {
    0: 'UNRANKED',
    1: 'Unused1',
    2: 'Unused2',
    3: 'IRON 1',
    4: 'IRON 2',
    5: 'IRON 3',
    6: 'BRONZE 1',
    7: 'BRONZE 2',
    8: 'BRONZE 3',
    9: 'SILVER 1',
    10: 'SILVER 2',
    11: 'SILVER 3',
    12: 'GOLD 1',
    13: 'GOLD 2',
    14: 'GOLD 3',
    15: 'PLATINUM 1',
    16: 'PLATINUM 2',
    17: 'PLATINUM 3',
    18: 'DIAMOND 1',
    19: 'DIAMOND 2',
    20: 'DIAMOND 3',
    21: 'ASCENDANT 1',
    22: 'ASCENDANT 2',
    23: 'ASCENDANT 3',
    24: 'IMMORTAL 1',
    25: 'IMMORTAL 2',
    26: 'IMMORTAL 3',
    27: 'RADIANT'
}

def get_rank_name(rank):
    global ranks
    if rank in ranks: return ranks[rank]
    else: return rank


characters = None

def retrieve_characters():
    global characters
    characters = {}
    r = requests.get('https://valorant-api.com/v1/agents')
    r.raise_for_status()
    for c in r.json()['data']:
        characters[c['uuid']] = c['displayName']
        characters[c['developerName']] = c['displayName']

def get_character(character_id):
    global characters
    if characters is None: retrieve_characters()
    if character_id in characters: return characters[character_id]
    else: return character_id

class Player:
    def __init__(self, id, name, tag, team,
                 character_id,
                 score, kills, deaths, assists,
                 party_id, rank):
        self.player_id, self.tag = PlayerID(id, name, team), tag
        self.character = get_character(character_id)
        self.score, self.kills, self.deaths, self.assists = score, kills, deaths, assists
        self.party_id, self.rank = party_id, rank
        self.rank_name = get_rank_name(rank)

    @property
    def id(self):
        return self.player_id.id

    @property
    def name(self):
        return self.player_id.name

    @property
    def team(self):
        return self.player_id.team
