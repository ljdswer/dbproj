import simplejson as json # for serializing Decimal
from functools import wraps
from valkey import Valkey, DataError, ConnectionError
from logging import getLogger

class Cache:
    def __init__(self, config: dict):
        self.config = config
        self.conn = self._connect()

    def _connect(self):
        conn = Valkey(**self.config)
        return conn

    def set_value(self, name: str, value_dict: dict, ttl: int):
        value_js = json.dumps(value_dict)
        try:
            self.conn.set(name=name, value=value_js)
            if ttl > 0:
                self.conn.expire(name, ttl)
                return True
        except DataError as err:
            print(f"DataError: {err}")
            return False

    def get_value(self, name: str):
        try:
            value_js = self.conn.get(name)
            if value_js:
                value_dict = json.loads(value_js)
                return value_dict
            else:
                return None
        except ConnectionError as err:
            print(f"ConnectionError: {err}")
            return None

def fetch_from_cache(cache_config: dict, ttl: int):
    cache = Cache(cache_config)
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{json.dumps(args)}:{json.dumps(kwargs)}"
            cached_value = cache.get_value(cache_key)
            if cached_value is not None:
                return cached_value
            result = func(*args, **kwargs)
            cache.set_value(cache_key, result, ttl)
            return result
        return wrapper
    return decorator
