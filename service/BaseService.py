import json
from pathlib import Path
from persistence.Database import Database


class BaseService:
    def __init__(self):
        parent_dir = Path(__file__).parent.resolve().parent
        filename = "dbconnection.json"
        config_filepath = parent_dir / filename

        if not config_filepath.exists():
            raise FileNotFoundError(f"File not found: {config_filepath}")
        try:
            with open(config_filepath, 'r', encoding='utf-8') as file:
                dbconnection = json.loads(file.read())
        except Exception as e:
            raise IOError(f"Error reading file {config_filepath}: {e}")
        host = dbconnection["host"]
        database = dbconnection["database"]
        user = dbconnection["user"]
        password = dbconnection["password"]
        port = dbconnection["port"]
        pool_name = "mypool"
        pool_size = 5
        self.db = Database(host, database, user, password, port, pool_name, pool_size)
        self.db.connect()