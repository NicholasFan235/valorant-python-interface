import requests
import requests.adapters
import valpy
import threading


class Connection(requests.Session):
    def __init__(self, stop=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://api.henrikdev.xyz"
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=valpy.henrikdev.Config.pool_connections,
            pool_maxsize=valpy.henrikdev.Config.pool_max_size)
        self.mount(self.url, adapter)
        self.stop = stop if stop is not None else threading.Event()
    
    def get(self, endpoint):
        while not self.stop.is_set():
            response = super().get(endpoint)
            if response.ok: return response
            
            if response.status_code == 429:
                print(f'Rate Limited: {endpoint}')
                self.stop.wait(10)
                continue
            print(response.content)
            raise response.raise_for_status()

    def get_json(self, endpoint):
        return self.get(endpoint).json()
    
    def get_player(self, name, tag):
        endpoint = f'{self.url}/valorant/v1/account/{name}/{tag}'
        return self.get_json(endpoint)

    def get_matches(self, region, name, tag, **kwargs):
        query = '&'.join(f'{k}={v}' for k,v in kwargs.items())
        endpoint = f'{self.url}/valorant/v3/matches/{region}/{name}/{tag}'
        if query != '': endpoint += '?'+query
        return self.get_json(endpoint)

    def get_lifetime_matches(self, region, name, tag, **kwargs):
        query = '&'.join(f'{k}={v}' for k,v in kwargs.items())
        endpoint = f'{self.url}/valorant/v1/lifetime/matches/{region}/{name}/{tag}'
        if query != '': endpoint += '?'+query
        return self.get_json(endpoint)

    def get_match(self, match_id):
        endpoint = f'{self.url}/valorant/v2/match/{match_id}'
        return self.get_json(endpoint)
    
