

class PlayerID:
    def __init__(self, id, name, team):
        self.id, self.name, self.team = id, name, team

    def __eq__(self, other):
        return self.id == other.id
