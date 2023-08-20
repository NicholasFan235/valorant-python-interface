import dataclasses

class Config:
    pool_connections=2
    pool_max_size=2
    username=None
    password=None

class CollectConfig:
    pass

@dataclasses.dataclass
class SynchronizeConfig:
    player_id:str
    name:str
    tag:str
    queue:str = 'competitive'

    matches_per_page=20

    def __str__(self):
        return f'{self.name}#{self.tag} {self.queue}'
