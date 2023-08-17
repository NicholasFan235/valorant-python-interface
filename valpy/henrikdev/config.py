import dataclasses

class Config:
    pool_connections=2
    pool_max_size=2

class ViewConfig:
    pass

class CollectConfig:
    pass

@dataclasses.dataclass
class SynchronizeConfig:
    name:str
    tag:str
    region:str = 'eu'
    filter:str = 'competitive'

    matches_per_page=20

    def __str__(self):
        return f'{self.name}#{self.tag} {self.region} {self.filter}'
