import valpy


class DefuseEventFactory:
    def read(data):
        de = valpy.DefuseEvent(
            data['defuseLocation']['x'],
            data['defuseLocation']['y'],
            data['defuseRoundTime'])
        for p in data['defusePlayerLocations']:
            de.add_player_location(
                valpy.PlayerLocation(
                    p['subject'],
                    None,
                    p['location']['x'], p['location']['y'],
                    p['viewRadians'], None),
                p['subject'] == data['bombDefuser'])
        return de
