import valpy
from ...dataclasses._player_id import PlayerID


class PlayerStatsFactory:
    def read(data):
        ps = valpy.PlayerStats(
            data['subject'],
            None,
            None,
            len(data['kills']), data['score'],
            data['wasAfk'], data['wasPenalized'],
            data['stayedInSpawn'])
        for event in data['damage']:
            ps.add_damage_event(
                valpy.DamageEvent(
                    PlayerID(event['receiver'],
                             None,
                             None),
                    event['damage'],
                    event['headshots'],
                    event['bodyshots'],
                    event['legshots']))
        ps.add_economy(valpy.Economy(
            data['economy']['loadoutValue'],
            data['economy']['weapon'],
            data['economy']['armor']))
        return ps