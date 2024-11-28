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
        schema = [c[0] for c in cur.description]
        result = [dict(zip(schema, row)) for row in cur.fetchall()]
    return result

def callproc(dbconfig: dict, procedure: str, args: tuple) -> list:
    logger = getLogger(__name__)
    with DBContextManager(dbconfig) as cur:
        logger.debug(f"Executing {procedure} with: {args}")
        cur.callproc(procedure, args)
        schema = [c[0] for c in cur.description]
        result = [dict(zip(schema, row)) for row in cur.fetchall()]
        cur.nextset()
    return result