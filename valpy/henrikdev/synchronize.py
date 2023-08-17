from .connection import Connection
from .config import SynchronizeConfig
import valpy.sql
import threading


class Synchronize:
    def __init__(self, conn:Connection, ingest:valpy.sql.Ingest, cfg:SynchronizeConfig, stop:threading.Event=None):
        self.conn = conn
        self.ingest = ingest
        self.cfg = cfg
        self.stop = stop if stop is not None else threading.Event()

    def run(self):
        page = 1
        match_ids = []
        while not self.stop.is_set():
            #print(f'Synchronize page {page} for {self.cfg}')
            r = self.conn.get_lifetime_matches(
                self.cfg.region,
                self.cfg.name,
                self.cfg.tag,
                filter=self.cfg.filter,
                size=SynchronizeConfig.matches_per_page,
                page=page)
            
            for d in r['data']:
                match_ids.append(d['meta']['id'])
            
            if len(match_ids) > 20:
                self.ingest.push_overviews(match_ids)
                match_ids = []
            
            if r['results']['after'] > 0:
                page += 1
            else:
                break
        print(f'Completed Synchronize for {self.cfg}')
        self.ingest.push_overviews(match_ids)

