from .._player_id import PlayerID
from ..player_location import PlayerLocation

class PlantEvent:
    def __init__(self, x, y, time, site):
        self.x, self.y, self.time, self.site = x, y, time, site
        self.planter = None
        self.player_locations = []

    def add_player_location(self, player:PlayerLocation, planter):
        if planter:
            self.planter = player
        else:
            self.player_locations.append(player)

