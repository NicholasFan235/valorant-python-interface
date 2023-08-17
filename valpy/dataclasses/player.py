from ._player_id import PlayerID


class Player:
    def __init__(self, id, name, tag, team,
                 character,
                 score, kills, deaths, assists,
                 headshots, bodyshots, legshots,
                 damage_dealt, damage_taken):
        self.player_id, self.tag = PlayerID(id, name, team), tag
        self.character = character
        self.score, self.kills, self.deaths, self.assists = score, kills, deaths, assists
        self.headshots, self.bodyshots, self.legshots = headshots, bodyshots, legshots
        self.damage_dealt, self.damage_taken = damage_dealt, damage_taken

    @property
    def id(self):
        return self.player_id.id

    @property
    def name(self):
        return self.player_id.name

    @property
    def team(self):
        return self.player_id.team
