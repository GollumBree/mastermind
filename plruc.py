from functools import lru_cache, wraps
from pathlib import Path
import pickle
import time


@lru_cache(maxsize=None)
def load_cache(path: Path):
    if path.exists():
        with path.open("rb") as f:
            return pickle.load(f)
    return {}


def plruc(func):
    """Persistent LRU cache decorator."""
    cache = load_cache(Path(f".{func.__module__}::{func.__name__}.plruc.pkl"))
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        args_cache = (args, frozenset(kwargs.items()))

        if args_cache in cache:
            return cache[args_cache]
        result = func(*args, **kwargs)
        cache[args_cache] = result
        with Path(f".{func.__module__}::{func.__name__}.plruc.pkl").open("wb") as f:
            pickle.dump(cache, f)
        return result
    
    return wrapper