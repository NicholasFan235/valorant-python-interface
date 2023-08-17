import valpy


class MatchFactory:
    def read(data):
        assert(not (data['teams']['red']['has_won'] and data['teams']['blue']['has_won']))
        outcome = 'draw'
        if not data['teams']['red']['has_won']: outcome = 'blue'
        if not data['teams']['blue']['has_won']: outcome = 'red'
        
        m = valpy.Match(
            data['metadata']['matchid'],
            data['metadata']['season_id'],
            data['metadata']['game_version'],
            data['metadata']['game_start_patched'],
            data['metadata']['map'],
            data['metadata']['game_start'],
            data['metadata']['game_length'],
            data['metadata']['rounds_played'],
            outcome,
            data['metadata']['mode'],
            data['metadata']['mode_id'],
            data['metadata']['queue'])
        m.rounds = []
        for i, r in enumerate(data['rounds']):
            m.rounds.append(valpy.RoundFactory.read(r, i))
        m.players = []
        for p in data['players']['all_players']:
            m.players.append(valpy.Player(
                p['puuid'], p['name'], p['tag'], p['team'],
                p['character'],
                p['stats']['score'], p['stats']['kills'], p['stats']['deaths'], p['stats']['assists'],
                p['stats']['headshots'], p['stats']['bodyshots'], p['stats']['legshots'],
                p['damage_made'], p['damage_received']))
        m.kills = []
        for k in data['kills']:
            kill_event = valpy.KillEventFactory.read(k)
            m.kills.append(kill_event)
            m.rounds[kill_event.round].kill_events.append(kill_event)
        return m
