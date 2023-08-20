import sqlite3
import threading
import datetime


class Connection:
    def get_connection(self):
        if threading.current_thread().ident not in self.connections:
            self.connections[threading.current_thread().ident] = sqlite3.connect(check_same_thread=False, *self.args, **self.kwargs)
            print(f'Created database connection, currently {len(self.connections)} connections open.')
        return self.connections[threading.current_thread().ident]

    def __del__(self):
        n = len(self.connections)
        for c in self.connections.values():
            c.close()
        print(f'Closed {n} database connections.')

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.connections = {}
        with self.get_connection() as conn:
            conn.executescript('''
                            CREATE TABLE IF NOT EXISTS players (
                                id TEXT PRIMARY KEY,
                                name TEXT NOT NULL,
                                tag TEXT NOT NULL,

                                UNIQUE(name, tag)
                            );
                            
                            CREATE TABLE IF NOT EXISTS match_overviews(
                               id TEXT PRIMARY KEY,
                               retrieved BOOLEAN NOT NULL
                            );

                            CREATE TABLE IF NOT EXISTS matches (
                                id TEXT PRIMARY KEY,
                                map TEXT NOT NULL,
                                start_time TIMESTAMP NOT NULL,
                                duration TIMESTAMP NOT NULL,
                                rounds INTEGER NOT NULL,
                                queue TEXT NOT NULL,
                                outcome TEXT NOT NULL,
                                data_link TEXT,
                                match_link TEXT,
                                data_source TEXT
                            );

                            CREATE TABLE IF NOT EXISTS match_players (
                                player_id TEXT NOT NULL,
                                match_id TEXT NOT NULL,
                                team TEXT NOT NULL,
                                agent TEXT NOT NULL,
                                score INTEGER NOT NULL,
                                kills INTEGER NOT NULL,
                                deaths INTEGER NOT NULL,
                                assists INTEGER NOT NULL,
                                party_id TEXT,
                                rank INTEGER,
                                rank_name TEXT,


                                UNIQUE(player_id, match_id),
                                FOREIGN KEY(player_id) REFERENCES players(id),
                                FOREIGN KEY(match_id) REFERENCES matches(id)
                            );
                          ''')

    def write_player(self, player):
        try:
            with self.get_connection() as conn:
                conn.execute('''
                                INSERT INTO players(id, name, tag)
                                VALUES (?, ?, ?)
                                ON CONFLICT DO NOTHING;
                            ''', (player.id, player.name, player.tag))
        except Exception as e:
            raise e

    def write_match(self, match):
        try:
            for player in match.players: self.write_player(player)
            with self.get_connection() as conn:
                conn.execute('''
                                INSERT INTO matches(id, map, start_time, duration, rounds, queue, outcome)
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                                ON CONFLICT DO UPDATE SET
                                    map = excluded.map,
                                    start_time = excluded.start_time,
                                    duration = excluded.duration,
                                    rounds = excluded.rounds,
                                    queue = excluded.queue,
                                    outcome = excluded.outcome;
                            ''',
                            (match.match_id, match.map, datetime.datetime.timestamp(match.start_time), match.game_length, match.rounds_played, match.queue, match.outcome))
                for player in match.players:
                    conn.execute('''
                                        INSERT INTO match_players(player_id, match_id, team, agent, score, kills, deaths, assists, party_id, rank, rank_name)
                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                        ON CONFLICT DO UPDATE SET
                                            team = excluded.team,
                                            agent = excluded.agent,
                                            score = excluded.score,
                                            kills = excluded.kills,
                                            deaths = excluded.deaths,
                                            assists = excluded.assists,
                                            party_id = excluded.party_id,
                                            rank = excluded.rank,
                                            rank_name = excluded.rank_name;
                                    ''',
                                    (player.id, match.match_id, player.team, player.character, player.score, player.kills, player.deaths, player.assists, player.party_id, player.rank, player.rank_name))
                conn.execute('INSERT INTO match_overviews(id, retrieved) VALUES (?, true) ON CONFLICT (id)\
                             DO UPDATE SET retrieved = true;', (match.match_id,))
        except Exception as e:
            raise e
    
    def add_data_links(self, match_id, data_file, match_file, data_source=None):
        try:
            with self.get_connection() as conn:
                conn.execute('''
                                UPDATE matches SET
                                    data_link = ?,
                                    match_link = ?,
                                data_source = ?
                                WHERE id = ?;
                            ''',
                            (str(data_file), str(match_file), str(data_source), match_id))
        except Exception as e:
            raise e
    
    def write_match_overview(self, match_id):
        try:
            with self.get_connection() as conn:
                conn.execute('''
                                INSERT INTO match_overviews(id, retrieved)
                                VALUES (?, false)
                                ON CONFLICT DO NOTHING;
                            ''',
                            (match_id,))
        except Exception as e:
            raise e
    
    def write_match_overviews(self, match_ids):
        try:
            with self.get_connection() as conn:
                conn.executemany('INSERT INTO match_overviews(id, retrieved)\
                                 VALUES (?, false) ON CONFLICT DO NOTHING;',
                                 [(id,) for id in match_ids])
        except Exception as e:
            raise e

    def has_match(self, match_id:str):
        result = False
        try:
            with self.get_connection() as conn:
                cur = conn.cursor()
                cur.execute('SELECT EXISTS(SELECT 1 FROM matches WHERE matches.id = ? LIMIT 1)', (match_id,))
                result = cur.fetchone()[0] == 1
                cur.close()
        except Exception as e:
            raise e
        return result
    
    def has_match_overview(self, match_id:str):
        print(match_id)
        result = False
        try:
            with self.get_connection() as conn:
                cur = conn.cursor()
                cur.execute('SELECT EXISTS(SELECT 1 FROM match_overviews WHERE match_overviews.id = ? LIMIT 1)', (match_id,))
                result = cur.fetchone()[0] == 1
                cur.close()
        except Exception as e:
            raise e
        return result

    def get_matches_to_collect(self, limit=10):
        result = []
        try:
            with self.get_connection() as conn:
                cur = conn.cursor()
                cur.execute('SELECT id FROM match_overviews WHERE retrieved=false LIMIT ?;', (limit,))
                result = [r[0] for r in cur.fetchall()]
                cur.close()
        except Exception as e:
            raise e
        return result


