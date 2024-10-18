from mariadb import DataError
from .sql_provider import SQLProvider
from .context_manager import DBContextManager

def alter(dbconfig: dict, query: str, args: tuple) -> None:
    with DBContextManager(dbconfig) as cur:
        cur.execute(query, args)

def select(dbconfig: dict, query: str, args: tuple) -> list:
    with DBContextManager(dbconfig) as cur:
        cur.execute(query, args)
        result = [i for i in cur]
    return result
