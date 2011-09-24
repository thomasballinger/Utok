#!/usr/bin/env python
import os
from glob import glob
os.system('wget http://redis.googlecode.com/files/redis-2.2.14.tar.gz')
os.system('tar -xzf redis-2.2.14.tar.gz')
os.chdir('redis-2.2.14')
os.system('make')
os.system('rm redis-2.2.14.tar.gz')
