'''
Copyright (c) 2014, Aaron Westendorf All rights reserved.

https://github.com/agoragames/pluto/blob/master/LICENSE.txt
'''

from pymongo import MongoClient
from .datastore import Datastore, Timeseries

class Mongo(Datastore):

  def _init_client(self):
    # TODO: fix this ugly where we have to remove a small number of fields
    # because MongoClient can't just ignore things it doesn't care about.
    config = self.configuration.copy()
    d_type = config.pop('type', None)
    db = config.pop('db', 'pluto')
    collection = config.pop('collection', self._node.name)
    self._client = MongoClient(**config)[db][collection]

  def timeseries(self, **kwargs):
    '''Return a timeseries built off of the client.'''
    # customized because kairos needs a database handle and client is a
    # collection.
    return Timeseries( self._client.database, **kwargs )
