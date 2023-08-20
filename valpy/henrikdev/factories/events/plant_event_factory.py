import valpy

class PlantEventFactory:
    def read(data):
        pe = valpy.PlantEvent(
            data['plant_location']['x'],
            data['plant_location']['y'],
            data['plant_time_in_round'],
            data['plant_site'])
        for p in data['player_locations_on_plant']:
            pe.add_player_location(
                valpy.PlayerLocation(
                    p['player_puuid'],
                    p['player_display_name'],
                    p['location']['x'], p['location']['y'],
                    p['view_radians'], p['player_team']),
                p['player_puuid'] == data['planted_by']['puuid'])
        return pe
