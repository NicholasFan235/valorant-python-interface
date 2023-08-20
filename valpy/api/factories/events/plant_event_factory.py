import valpy

class PlantEventFactory:
    def read(data):
        pe = valpy.PlantEvent(
            data['plantLocation']['x'],
            data['plantLocation']['y'],
            data['plantRoundTime'],
            data['plantSite'])
        for p in data['plantPlayerLocations']:
            pe.add_player_location(
                valpy.PlayerLocation(
                    p['subject'],
                    None,
                    p['location']['x'], p['location']['y'],
                    p['viewRadians'], None),
                p['subject'] == data['bombPlanter'])
        return pe
