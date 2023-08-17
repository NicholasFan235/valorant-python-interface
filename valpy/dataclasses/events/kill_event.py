from ..player_location import PlayerLocation
from .._player_id import PlayerID


class KillEvent:
    def __init__(self, round:int, time:int, victim:PlayerLocation):
        self.round, self.time = round, time
        self.victim = victim
        self.killer = None
        self.player_locations = []
        self.assistants = []

    def add_player_location(self, player:PlayerLocation, killer:bool):
        if killer:
            self.killer = player
        else:
            self.player_locations.append(player)

    def add_assistant(self, assistant:PlayerID):
        self.assistants.append(assistant)

    @property
    def artists(self):
        for a in self.victim.artists(0): yield a
        for a in self.killer.artists(1): yield a
        for p in self.player_locations:
            for a in p.artists(1): yield a

    @property
    def killer_team(self):
        yield self.killer
        for p in self.player_locations:
            if p.team == self.killer.team: yield p

    @property
    def victim_team(self):
        yield self.victim
        for p in self.player_locations:
            if p.team == self.victim.team: yield p

    def __str__(self):
        return f'KillEvent(Round {self.round}:{self.time}s, ' +\
            f'{self.killer.name.split("#")[0]} -> ' +\
            f'{self.victim.name.split("#")[0]}, ' +\
            f'{len(self.player_locations) + 1} remaining)'
