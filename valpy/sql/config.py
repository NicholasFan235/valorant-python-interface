import pathlib


class IngestConfig:
    def set_data_folder(data_folder='data'):
        IngestConfig.data_folder = pathlib.Path(data_folder)
        IngestConfig.log_folder = pathlib.Path(data_folder, 'logs')
        IngestConfig.database_file = pathlib.Path(data_folder, 'database.db')
        IngestConfig.match_data_folder = pathlib.Path(data_folder, 'match_data')
        IngestConfig.matches_folder = pathlib.Path(data_folder, 'matches')


IngestConfig.set_data_folder()
