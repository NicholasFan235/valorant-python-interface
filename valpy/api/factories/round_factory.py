from .events.defuse_event_factory import DefuseEventFactory
from .player_stats_factory import PlayerStatsFactory
from .events.plant_event_factory import PlantEventFactory
import valpy


class RoundFactory:
    def read(data, round:int=None):
        r = valpy.Round(round, data['winningTeam'], data['roundResult'])
        if 'bombPlanter' in data:
            r.add_plant_event(PlantEventFactory.read(data))
        if 'bombDefuser' in data:
            r.add_defuse_event(DefuseEventFactory.read(data))
        for ps in data['playerStats']:
            r.add_player_stats(PlayerStatsFactory.read(ps))
        return r
    