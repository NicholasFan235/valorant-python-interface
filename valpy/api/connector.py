import threading
from .connection import Connection
from .collect import Collect
from .synchronize import Synchronize
from .config import SynchronizeConfig
import valpy


class ValorantApiConnector:
    def __init__(self, region='eu'):
        self.stop_flag = threading.Event()
        self.conn = Connection(region=region, stop=self.stop_flag)
        self.ingest = valpy.sql.Ingest()
        self.collect = Collect(self.conn, self.ingest, stop=self.stop_flag)
        self.synchronizers = []
        self.threads = []

    def add_synchronize_target(self, cfg:SynchronizeConfig):
        self.synchronizers.append(Synchronize(self.conn, self.ingest, cfg, stop=self.stop_flag))

    def start(self):
        print('Starting Valorant Api Connector...')
        self.stop_flag.clear()
        self.threads.append(threading.Thread(target=self.collect.run))
        for s in self.synchronizers:
            self.threads.append(threading.Thread(target=s.run))
        for t in self.threads:
            t.start()
    
    def stop(self):
        print(f'Stopping {len(self.threads)} Valorant Api Connector threads...')
        self.stop_flag.set()
        for t in self.threads:
            t.join()
        self.threads = []
        print('Stopped Safely')

