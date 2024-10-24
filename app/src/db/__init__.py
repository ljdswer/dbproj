from mariadb import DataError
from logging import getLogger
from .sql_provider import SQLProvider
from .context_manager import DBContextManager

def alter(dbconfig: dict, query: str, args: tuple) -> None:
    with DBContextManager(dbconfig) as cur:
        cur.execute(query, args)

def select(dbconfig: dict, query: str, args: tuple) -> list:
    logger = getLogger(__name__)
    with DBContextManager(dbconfig) as cur:
        logger.debug(f"Executing {query} with: {args}")
        cur.execute(query, args)
        result = [i for i in cur]
    return result
