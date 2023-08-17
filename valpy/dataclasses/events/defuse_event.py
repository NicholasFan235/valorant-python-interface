from .._player_id import PlayerID
from ..player_location import PlayerLocation


class DefuseEvent:
    def __init__(self, x, y, time):
        self.x, self.y, self.time = x, y, time
        self.defuser = None
        self.player_locations = []

    def add_player_location(self, player:PlayerLocation, defuser):
        if defuser:
            self.defuser = player
        else:
            self.player_locations.append(player)
