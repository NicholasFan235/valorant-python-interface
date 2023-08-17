from ._player_id import PlayerID

import matplotlib.pylab as plt
import matplotlib
import numpy as np


class PlayerLocation:
    def __init__(self, id, name, x, y, angle, team):
        self.player_id = PlayerID(id, name, team)
        self.x, self.y, self.angle = x, y, angle

    @property
    def id(self):
        return self.player_id.id

    @property
    def name(self):
        return self.player_id.name.split('#')[0]

    @property
    def tag(self):
        return self.player_id.name.split('#')[1]

    @property
    def team(self):
        return self.player_id.team

    def artists(self, status):
        if (status==1):
            yield matplotlib.patches.FancyArrowPatch(
                (self.x, self.y), (self.x + 1000*np.cos(self.angle), self.y + 1000*np.sin(self.angle)),
                color=self.team.lower(), arrowstyle='->', mutation_scale=15)
        yield matplotlib.text.Text(
            self.x, self.y + 250, self.name, color='k',
            horizontalalignment='center')
        yield matplotlib.patches.Circle(
            (self.x, self.y), 200, facecolor=self.team.lower() if status == 1 else 'white',
            edgecolor=self.team.lower() if status == 0 else None, linewidth=1)

    def __str__(self):
        return f'Player({self.name}, {self.x}, {self.y}, {self.team})'