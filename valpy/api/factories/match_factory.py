import valpy
from .round_factory import RoundFactory
from .events.kill_event_factory import KillEventFactory
import datetime


class MatchFactory:
    def read(data):
        team_win_map = {d['teamId']:d['won'] for d in data['teams']}
        assert(sum(team_win_map.values()) == 1 or sum(team_win_map.values()) == 0)
        outcome = 'draw'
        for k,v in team_win_map.items():
            if v: outcome = k
        
        m = valpy.Match(
            data['matchInfo']['matchId'],
            data['matchInfo']['seasonId'],
            data['matchInfo']['gameVersion'],
            data['matchInfo']['mapId'],
            datetime.datetime.fromtimestamp(data['matchInfo']['gameStartMillis']/1000),
            data['matchInfo']['gameLengthMillis']//1000,
            len(data['roundResults']),
            outcome,
            data['matchInfo']['queueID'])
        m.rounds = []
        for r in data['roundResults']:
            m.rounds.append(RoundFactory.read(r, r['roundNum']))
        m.players = []
        for p in data['players']:
            m.players.append(valpy.Player(
                p['subject'], p['gameName'], p['tagLine'], p['teamId'],
                p['characterId'],
                p['stats']['score'], p['stats']['kills'], p['stats']['deaths'], p['stats']['assists'],
                p['partyId'], p['competitiveTier']))
        m.kills = []
        for k in data['kills']:
            kill_event = KillEventFactory.read(k)
            m.kills.append(kill_event)
            m.rounds[kill_event.round].kill_events.append(kill_event)
        return m
