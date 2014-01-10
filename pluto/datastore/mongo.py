'''
Copyright (c) 2014, Aaron Westendorf All rights reserved.

https://github.com/agoragames/pluto/blob/master/LICENSE.txt
'''

from pymongo import MongoClient
from .input import Input

class Mongo(Input):

  def _init_client(self):
    self._client = MongoClient(**self.configuration)[ \
      config.get('database', 'pluto') ][ \
      config.get('collection', 'input') ]

  # TODO: finder API
