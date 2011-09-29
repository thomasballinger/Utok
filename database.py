"""Everything to do with representing data in the database"""
import redis
import os
import re

def get_redis_object():
    redistogo = os.environ.get('REDISTOGO_URL', None)
    if redistogo:  # Heroku!
        _, password, host, port = re.search(r"(.*)://redistogo:(.*)@(.*):(\d*)", redistogo).groups()
        r = redis.Redis(host=host, port=int(port), password=password)
    else: # local!
        r = redis.Redis()
    return r
