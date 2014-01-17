'''
Copyright (c) 2014, Aaron Westendorf All rights reserved.

https://github.com/agoragames/pluto/blob/master/LICENSE.txt
'''

from pymongo import MongoClient
from .datastore import Datastore

class Mongo(Datastore):

  def _init_client(self):
    # TODO: support more options
    db = self.configuration.pop('db', 'pluto')
    collection = self.configuration.pop('collection', 'data') # TODO: figure this out better
    self._client = MongoClient(**self.configuration)[db][collection]
