'''
Copyright (c) 2014, Aaron Westendorf All rights reserved.

https://github.com/agoragames/pluto/blob/master/LICENSE.txt
'''

from pymongo import MongoClient
from .datastore import Datastore

__node_types__ = {}
__node_backend__ = None

class NodeType(type):
  
  def __init__(self, name, bases, dct):
    global __node_types__
    super(NodeType,self).__init__(name, bases, dct)
 
    if globals().get('Node') in bases:
      __node_types__[name] = self

  @property
  def backend(self):
    return __node_backend__

  @backend.setter
  def backend(self, config):
    global __node_backend__
    __node_backend__ = MongoClient(**config)[ config.get('database','pluto') ][ 'nodes' ]

# TODO inherit from celery task?
class Node(object):
  __metaclass__ = NodeType
  
  def __new__(cls, configuration={}):
    if cls==Node and 'type' in configuration:
      # load a specific node based on the short name of the class
      if configuration['type'] in __node_types__:
        return __node_types__[ configuration['type'] ]( configuration )
      else:
        raise ImportError("Unsupported or unknown node type %s", configuration['type'])
    return object.__new__(cls, configuration)
  
  def __init__(self, configuration={}):
    self.configuration = configuration

    # TODO: initialize input and output, or lazy on property read?

  def __str__(self):
    '''String version of a node.'''
    type_str = self.configuration.get('type', 'Node')
    return '%s(%s)'%( type_str, self.configuration )

  @classmethod
  def find(self, **kwargs):
    '''
    Returns an iterator on nodes that match the conditions.
    '''
    for node in __node_backend__.find( **kwargs ):
      yield Node(node)

  @property
  def input(self):
    if 'input' in self.configuration:
      rval = getattr(self, '_input')
      if not rval:
        rval = self._input = Datastore( self.configuration['input'] )
      return rval
    return None

  @property
  def output(self):
    if 'output' in self.configuration:
      rval = getattr(self, '_output')
      if not rval:
        rval = self._output = Datastore( self.configuration['output'] )
      return rval
    return None

  @property
  def backend(self):
    return Node.backend

  @property
  def id(self):
    return self.configuration.get('_id')

  def save(self):
    # TODO also block saving nodes with an unknown type?
    if 'type' not in self.configuration and self.__class__ is not Node:
      self.configuration['type'] = self.__class__.__name__
    self.backend.save( self.configuration )
    return self
