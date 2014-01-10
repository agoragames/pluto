'''
Copyright (c) 2014, Aaron Westendorf All rights reserved.

https://github.com/agoragames/pluto/blob/master/LICENSE.txt
'''

from pymongo import MongoClient
from bson import ObjectId

from .datastore import Datastore
#from . import celeryconfig
#from celery.contrib.methods import task
from celery import Celery

#app = Celery(__name__, broker='amqp://guest@localhost//')
app = Celery()
#app.config_from_object( celeryconfig )
app.config_from_object( 'pluto.celeryconfig' )

@app.task
def run(node_id):
  print 'RUNNING ', node_id
  try:
    node = Node.find( node_id )
    print 'IS ', node
  except Exception as e:
    print 'FAIL ', e
    import traceback
    traceback.print_exc()

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
  def find(self, *args, **kwargs):
    '''
    Returns an iterator on nodes that match the conditions.
    '''
    if len(args)==1 and isinstance(args[0], (str,unicode,ObjectId)):
      return Node( __node_backend__.find_one(ObjectId(args[0])) )
    else:
      return self.find_iter(*args, **kwargs)

  @classmethod
  def find_iter(self, *args, **kwargs):
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

  def schedule(self):
    '''Schedule this node to be run.'''
    # TODO: if not saved, save now so that there's an id
    #cereal = self.configuration.copy()
    #cereal['_id'] = str(cereal['_id'])
    run.delay( str(self.configuration['_id']) )
