import valpy


class RoundFactory:
    def read(data, round:int=None):
        r = valpy.Round(round, data['winning_team'], data['end_type'])
        if data['bomb_planted']:
            r.add_plant_event(valpy.PlantEventFactory.read(data['plant_events']))
        if data['bomb_defused']:
            r.add_defuse_event(valpy.DefuseEventFactory.read(data['defuse_events']))
        for ps in data['player_stats']:
            r.add_player_stats(valpy.PlayerStatsFactory.read(ps))
        return r