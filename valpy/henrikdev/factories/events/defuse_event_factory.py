import valpy


class DefuseEventFactory:
    def read(data):
        de = valpy.DefuseEvent(
            data['defuse_location']['x'],
            data['defuse_location']['y'],
            data['defuse_time_in_round'])
        for p in data['player_locations_on_defuse']:
            de.add_player_location(
                valpy.PlayerLocation(
                    p['player_puuid'],
                    p['player_display_name'],
                    p['location']['x'], p['location']['y'],
                    p['view_radians'], p['player_team']),
                p['player_puuid'] == data['defused_by']['puuid'])
        return de
