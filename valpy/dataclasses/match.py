

class Match:
    def __init__(self, match_id, season_id, game_version, game_start_patched,
                 map, start_time, game_length, rounds_played, outcome,
                 mode, mode_id, queue):
        self.match_id, self.season_id = match_id, season_id
        self.game_version, self.game_start_patched = game_version, game_start_patched
        self.map, self.start_time = map, start_time
        self.game_length, self.rounds_played, self.outcome = game_length, rounds_played, outcome
        self.mode, self.mode_id, self.queue = mode, mode_id, queue
        self.rounds = []
        self.players = []
        self.kills = []

