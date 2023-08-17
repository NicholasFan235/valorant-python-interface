import valpy
from ...dataclasses._player_id import PlayerID

class KillEventFactory:
    def read(data):
        ke = valpy.KillEvent(data['round'], data['kill_time_in_round'],
                       valpy.PlayerLocation(
                          data['victim_puuid'],
                          data['victim_display_name'],
                          data['victim_death_location']['x'],
                          data['victim_death_location']['y'], 0,
                          data['victim_team']))
        for p in data['player_locations_on_kill']:
            ke.add_player_location(
                valpy.PlayerLocation(
                    p['player_puuid'],
                    p['player_display_name'],
                    p['location']['x'], p['location']['y'],
                    p['view_radians'], p['player_team']),
                p['player_puuid'] == data['killer_puuid'])
        for a in data['assistants']:
            ke.add_assistant(
                PlayerID(a['assistant_puuid'],
                         a['assistant_display_name'],
                         a['assistant_team']))
        return ke
