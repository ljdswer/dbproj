import mariadb
import logging

class DBContextManager:
    def __init__(self, config: dict):
        self._config = config
        self._conn = None
        self._cursor = None

    def __enter__(self):
        logger = logging.getLogger(__name__)
        try:
            self._conn = mariadb.connect(
                user=self._config["user"],
                password=self._config["pass"],
                host=self._config["host"],
                port=self._config["port"],
                database=self._config["name"],
            )
            self._conn.autocommit = True
            self._cursor = self._conn.cursor()
            return self._cursor
        except (mariadb.Error, KeyError) as err:
            logger.error(err)
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._conn and self._cursor:
            if exc_type:
                self._conn.rollback()
            else:
                self._conn.commit()
            self._cursor.close()
            self._conn.close()
        if exc_type:
            return False
        return True
