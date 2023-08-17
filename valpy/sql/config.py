import pathlib


class IngestConfig:
    data_folder = pathlib.Path('data')

    log_folder = pathlib.Path(data_folder, 'logs')
    database_file = pathlib.Path(data_folder, 'database.db')
    match_data_folder = pathlib.Path(data_folder, 'match_data')
    matches_folder = pathlib.Path(data_folder, 'matches')
    