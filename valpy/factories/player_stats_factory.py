import valpy
from ..dataclasses._player_id import PlayerID


class PlayerStatsFactory:
    def read(data):
        ps = valpy.PlayerStats(
            data['player_puuid'],
            data['player_display_name'],
            data['player_team'],
            data['kills'], data['score'],
            data['was_afk'], data['was_penalized'],
            data['stayed_in_spawn'])
        for event in data['damage_events']:
            ps.add_damage_event(
                valpy.DamageEvent(
                    PlayerID(event['receiver_puuid'],
                             event['receiver_display_name'],
                             event['receiver_team']),
                    data['damage'],
                    data['headshots'],
                    data['bodyshots'],
                    data['legshots']))
        ps.add_economy(valpy.Economy(
            data['economy']['loadout_value'],
            data['economy']['weapon']['id'],
            data['economy']['weapon']['name'],
            data['economy']['armor']['id'],
            data['economy']['armor']['name']))
        return ps