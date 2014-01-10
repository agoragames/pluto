'''
Copyright (c) 2014, Aaron Westendorf All rights reserved.

https://github.com/agoragames/pluto/blob/master/LICENSE.txt
'''

import redis
from .input import Input

class Redis(Input):

  def __init__(self, config):
    self._client = redis.Redis(**config)
