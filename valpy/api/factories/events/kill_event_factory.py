from ....dataclasses._player_id import PlayerID
import valpy


class KillEventFactory:
    def read(data):
        ke = valpy.KillEvent(data['round'], data['roundTime'],
                       valpy.PlayerLocation(
                          data['victim'],
                          None,
                          data['victimLocation']['x'],
                          data['victimLocation']['y'], 0,
                          None))
        for p in data['playerLocations']:
            ke.add_player_location(
                valpy.PlayerLocation(
                    p['subject'],
                    None,
                    p['location']['x'], p['location']['y'],
                    p['viewRadians'], None),
                p['subject'] == data['killer'])
        for a in data['assistants']:
            ke.add_assistant(
                PlayerID(a,
                         None,
                         None))
        return ke
