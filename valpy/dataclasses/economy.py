

class Economy:
    def __init__(self, value, weapon_id, weapon_name, armor_id, armor_name):
        self.value = value
        self.weapon_id, self.weapon_name = weapon_id, weapon_name
        self.armor_id, self.armor_name = armor_id, armor_name

    def __str__(self):
        return f'${self.value}, armor: {self.armor_name}, weapon: {self.weapon_name}'
