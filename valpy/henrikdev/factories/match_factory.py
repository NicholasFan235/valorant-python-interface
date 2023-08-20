import valpy
import datetime
from .round_factory import RoundFactory
from .events.kill_event_factory import KillEventFactory


class MatchFactory:
    def read(data):
        if 'data' in data:
            data = data['data']
        assert(not (data['teams']['red']['has_won'] and data['teams']['blue']['has_won']))
        outcome = 'draw'
        if not data['teams']['red']['has_won']: outcome = 'blue'
        if not data['teams']['blue']['has_won']: outcome = 'red'
        
        m = valpy.Match(
            data['metadata']['matchid'],
            data['metadata']['season_id'],
            data['metadata']['game_version'],
            data['metadata']['map'],
            datetime.datetime.fromtimestamp(data['metadata']['game_start']),
            data['metadata']['game_length'],
            data['metadata']['rounds_played'],
            outcome,
            data['metadata']['mode_id'])
        m.rounds = []
        for i, r in enumerate(data['rounds']):
            m.rounds.append(RoundFactory.read(r, i))
        m.players = []
        for p in data['players']['all_players']:
            m.players.append(valpy.Player(
                p['puuid'], p['name'], p['tag'], p['team'],
                p['character'],
                p['stats']['score'], p['stats']['kills'], p['stats']['deaths'], p['stats']['assists'],
                p['party_id'], p['currenttier']))
        m.kills = []
        for k in data['kills']:
            kill_event = KillEventFactory.read(k)
            m.kills.append(kill_event)
            m.rounds[kill_event.round].kill_events.append(kill_event)
        return m
