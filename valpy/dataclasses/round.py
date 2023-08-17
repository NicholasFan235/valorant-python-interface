from .player_stats import PlayerStats
from .events.kill_event import KillEvent
from .events.plant_event import PlantEvent
from .events.defuse_event import DefuseEvent


class Round:
    def __init__(self, round, winning_team, end_type):
        self.round = round
        self.winning_team, self.end_type =\
            winning_team, end_type
        self.kill_events = []
        self.player_stats = []
        self.planted, self.defused = False, False
        self.plant_event, self.defuse_event = None, None

    def add_kill_event(self, kill_event:KillEvent):
        self.kill_events.append(kill_event)

    def add_player_stats(self, stats:PlayerStats):
        self.player_stats.append(stats)

    def add_plant_event(self, event:PlantEvent):
        self.planted = True
        self.plant_event = event

    def add_defuse_event(self, event:DefuseEvent):
        self.defused = True
        self.defused_event = event
