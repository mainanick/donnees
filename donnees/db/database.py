import os

from sqlalchemy import create_engine


class DatabaseConnection(object):
    _config = None
    engine = None

    @classmethod
    def config(self):
        if self._config is not None:
            return self._config

        if not os.environ['DSCONFIG']:
            raise ValueError("Database Config Missing")

        self._config = os.environ['DSCONFIG']
        return self._config

    @classmethod
    def connect(self):
        self.engine = create_engine(self.config())

    @classmethod
    def execute(self, query):
        if self.engine is None:
            self.connect()
        connection = self.engine.connect()
        results = connection.execute(query).fetchall()
        connection.close()
        return results
