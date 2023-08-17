from .._player_id import PlayerID


class DamageEvent:
    def __init__(self, receiver:PlayerID, damage, headshots, bodyshots, legshots):
        self.receiver = receiver
        self.damage = damage
        self.headshots, self.bodyshots, self.legshots = headshots, bodyshots, legshots

    def __str__(self):
        return f'{self.damage} -> {self.receiver.name}'
    