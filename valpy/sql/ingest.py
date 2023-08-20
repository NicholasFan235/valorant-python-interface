from .connection import Connection
from .config import IngestConfig
import json
import pathlib
import pickle
import os


class Ingest:
    def __init__(self):
        db_file = IngestConfig.database_file
        db_file.parent.mkdir(exist_ok=True, parents=True)
        self.db_conn = Connection(IngestConfig.database_file)
        
    def __contains__(self, match_id):
        return self.db_conn.has_match(match_id)

    def push_overview(self, match_id):
        self.db_conn.write_match_overview(match_id)

    def push_overviews(self, match_ids):
        self.db_conn.write_match_overviews(match_ids)

    def push_match(self, match_data_file, factory, data_source=None):
        with open(match_data_file, 'r') as f:
            match = factory.read(json.load(f))
        self.db_conn.write_match(match)
        match_file = pathlib.Path(IngestConfig.matches_folder, f'{match.match_id}.pkl')
        match_file.parent.mkdir(exist_ok=True, parents=True)
        with open(match_file, 'wb') as f:
            pickle.dump(match, f)
        self.db_conn.add_data_links(match.match_id, match_data_file, match_file, data_source)

    def get_matches_to_collect(self, limit=10):
        return self.db_conn.get_matches_to_collect(limit)
    
    def load_match_datas(self, factory, data_source=None):
        for f in os.listdir(IngestConfig.match_data_folder):
            self.push_match(pathlib.Path(IngestConfig.match_data_folder, f), factory)
    