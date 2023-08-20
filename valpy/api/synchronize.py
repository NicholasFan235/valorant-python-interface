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
        start = 0
        match_ids = []
        while not self.stop.is_set():
            print(f'Synchronize from {start} for {self.cfg}')
            try:
                r = self.conn.get_match_history(
                    player_id=self.cfg.player_id,
                    start=start,
                    stop=start + self.cfg.matches_per_page,
                    queue=self.cfg.queue
                )
            except InterruptedError:
                continue
            
            for d in r['History']:
                match_ids.append(d['MatchID'])
            
            if len(match_ids) > 100:
                self.ingest.push_overviews(match_ids)
                match_ids = []
            
            if r['EndIndex'] < r['Total']:
                start = r['EndIndex']
            else:
                break
        print(f'Completed Synchronize for {self.cfg}')
        self.ingest.push_overviews(match_ids)

