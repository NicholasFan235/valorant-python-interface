from .events.defuse_event_factory import DefuseEventFactory
from .player_stats_factory import PlayerStatsFactory
from .events.plant_event_factory import PlantEventFactory
import valpy


class RoundFactory:
    def read(data, round:int=None):
        r = valpy.Round(round, data['winning_team'], data['end_type'])
        if data['bomb_planted']:
            r.add_plant_event(PlantEventFactory.read(data['plant_events']))
        if data['bomb_defused']:
            r.add_defuse_event(DefuseEventFactory.read(data['defuse_events']))
        for ps in data['player_stats']:
            r.add_player_stats(PlayerStatsFactory.read(ps))
        return r
    