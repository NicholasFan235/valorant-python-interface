from .connection import Connection
from .factories.match_factory import MatchFactory
import valpy.sql
import json
import pathlib
import threading


class Collect:
    def __init__(self, conn:Connection, ingest:valpy.sql.Ingest, stop=None):
        self.conn = conn
        self.ingest = ingest
        self.stop = stop if stop is not None else threading.Event()
        self.replace = False

    def run(self):
        while not self.stop.is_set():
            ids = self.ingest.get_matches_to_collect(10)
            if len(ids) <= 0:
                print('Nothing to Collect, waiting...')
                self.stop.wait(10)
                continue
            
            for id in ids:
                if id in self.ingest and not self.replace: continue
                try:
                    r = self.conn.get_match_details(id)
                except InterruptedError:
                    break
                match_file = pathlib.Path(valpy.sql.IngestConfig.match_data_folder, f'{id}.json')
                match_file.parent.mkdir(exist_ok=True, parents=True)
                with open(match_file, 'w') as f:
                    json.dump(r, f)
                self.ingest.push_match(match_file, MatchFactory, 'riotgames')
                print(f'Collected {id}')

