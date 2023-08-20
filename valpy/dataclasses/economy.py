

class Economy:
    def __init__(self, value, weapon_id, armor_id):
        self.value = value
        self.weapon_id = weapon_id
        self.armor_id = armor_id

    def __str__(self):
        return f'${self.value}, armor: {self.armor_name}, weapon: {self.weapon_name}'
