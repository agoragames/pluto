'''
Copyright (c) 2014, Aaron Westendorf All rights reserved.

https://github.com/agoragames/pluto/blob/master/LICENSE.txt
'''

from kairos import Timeseries

__datastore_types__ = {}

class DatastoreType(type):
  
  def __init__(self, name, bases, dct):
    global __datastore_types__
    super(DatastoreType,self).__init__(name, bases, dct)
 
    if globals().get('Datastore') in bases:
      __datastore_types__[name] = self
      __datastore_types__[name.lower()] = self

class Datastore(object):
  __metaclass__ = DatastoreType
  
  def __new__(cls, node, configuration={}):
    d_type = configuration.pop('type', None)
    if cls==Datastore and d_type:
      # load a specific datastore based on the short name of the class
      if d_type in __datastore_types__:
        return __datastore_types__[ d_type ].__new__(__datastore_types__[d_type], node, configuration)
      else:
        raise ImportError("Unsupported or unknown datastore type %s", configuration['type'])
    return object.__new__(cls, configuration)
  
  def __init__(self, node, configuration={}):
    self._node = node
    self.configuration = configuration
    self._client = None
    self._init_client()

  def _init_client(self):
    '''Hook for subclasses to initialize the client.'''
    # must se

  @property
  def client(self):
    return self._client

  def timeseries(self, **kwargs):
    '''Return a timeseries built off of the client.'''
    return Timeseries( self._client, **kwargs )
