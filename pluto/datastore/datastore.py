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

class Datastore(object):
  __metaclass__ = DatastoreType
  
  def __new__(cls, configuration={}):
    if cls==Datastore and 'type' in configuration:
      # load a specific datastore based on the short name of the class
      if configuration['type'] in __datastore_types__:
        return __datastore_types__[ configuration['type'] ]( configuration )
      else:
        raise ImportError("Unsupported or unknown datastore type %s", configuration['type'])
    return object.__new__(cls, configuration)
  
  def __init__(self, configuration={}):
    self.configuration = configuration
    self._client = None

  def _init_client(self):
    '''Hook for subclasses to initialize the client.'''
    # must se

  @property
  def client(self):
    return self._client

  def timeseries(self, **kwargs):
    '''Return a timeseries built off of the client.'''
    return Timeseries( self._client, **kwargs )
