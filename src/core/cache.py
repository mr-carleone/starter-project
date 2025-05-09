# src/core/cache.py
from cachetools import TTLCache

user_cache = TTLCache(maxsize=100, ttl=300)
role_cache = TTLCache(maxsize=50, ttl=300)
