from ._player_id import PlayerID
from .economy import Economy
from .events.damage_event import DamageEvent
from .events.kill_event import KillEvent


class PlayerStats(PlayerID):
    def __init__(self, id, name, team, kills, score, was_afk=False, was_penalized=False, stayed_in_spawn=False):
        self.player_id = PlayerID(id, name, team)
        self.kills, self.score = kills, score
        self.was_afk, self.was_penalized, self.stayed_in_spawn =\
            was_afk, was_penalized, stayed_in_spawn
        self.damage_events = []
        self.kill_events = []
        self.economy = None

    def add_economy(self, economy:Economy):
        self.economy = economy

    def __str__(self):
        return f'{self.name}: ({self.score}CS){self.kills}K'

    @property
    def id(self):
        return self.player_id.id

    @property
    def name(self):
        return self.player_id.name.split('#')[0]

    @property
    def tag(self):
        return self.player_id.name.split('#')[1]

    @property
    def team(self):
        return self.player_id.team

    def add_damage_event(self, event:DamageEvent):
        self.damage_events.append(event)

    def add_kill_event(self, event:KillEvent):
        self.kill_events.append(event)