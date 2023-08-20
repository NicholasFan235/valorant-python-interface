import requests
import threading
import time
import datetime
import valpy
import asyncio
import riot_auth

riot_auth.RiotAuth.RIOT_CLIENT_USER_AGENT = "RiotClient/69.0.3.228.1352 %s (Windows;10;;Professional, x64)"

class Connection:
    def __init__(self, region='eu', stop=None):
        self.url = f"https://pd.{region}.a.pvp.net"
        self.stop = stop if stop is not None else threading.Event()
        self.sessions = {}
        self.auth = riot_auth.RiotAuth()
        asyncio.run(
            self.auth.authorize(
                valpy.api.Config.username,
                valpy.api.Config.password
                ))
        print(f'Authorized until {datetime.datetime.fromtimestamp(self.auth.expires_at)}')

    def make_session(self):
        return requests.Session()

    def get_session(self):
        if threading.current_thread().ident not in self.sessions:
            self.sessions[threading.current_thread().ident] = self.make_session()
        return self.sessions[threading.current_thread().ident]

    def get(self, endpoint):
        session = self.get_session()
        while not self.stop.is_set():
            if self.auth.expires_at < time.time():
                asyncio.run(self.auth.reauthorize())
                print(f'Reauthorized until {datetime.datetime.fromtimestamp(self.auth.expires_at)}')
            headers = {
                'X-Riot-Entitlements-JWT': self.auth.entitlements_token,
                'X-Riot-ClientPlatform': '(Windows;10;;Professional, x64)',
                'X-Riot-ClientVersion': '69.0.3.228.1352',
                'Authorization': f'Bearer {self.auth.access_token}'
            }
            response = session.get(endpoint, headers=headers)
            if response.ok: return response
            
            if response.status_code == 429:
                print(f'Rate Limited: {endpoint}')
                self.stop.wait(10)
                continue
            print(response.content)
            raise response.raise_for_status()
        raise InterruptedError

    def get_json(self, endpoint):
        return self.get(endpoint).json()
    
    def get_match_history(self, player_id, start=0, stop=20, queue=None):
        endpoint = f'{self.url}/match-history/v1/history/{player_id}?startIndex={start}&endIndex={stop}'
        if queue is not None: endpoint += f'&queue={queue}'
        return self.get_json(endpoint)

    def get_match_details(self, match_id):
        endpoint = f'{self.url}/match-details/v1/matches/{match_id}'
        return self.get_json(endpoint)
    
