'''
Copyright (c) 2014, Aaron Westendorf All rights reserved.

https://github.com/agoragames/pluto/blob/master/LICENSE.txt
'''

from datetime import datetime

from pymongo import MongoClient
from bson import ObjectId

from .datastore import Datastore
from celery import Celery

# Use the module name so that we don't have a circular load order
app = Celery()
app.config_from_object( 'pluto.celeryconfig' )

@app.task
def run(node_id, context_id=None):
  try:
    node = Node.find( node_id )
    if context_id:
      context = Node.find( context_id )
    else:
      context = None
    node.runit(context=context)
  except Exception as e:
    # TODO: handle exceptions in a celery-friendly way that also
    # says a lot more about what happened
    print 'FAIL ', e
    import traceback
    traceback.print_exc()

  for other in Node:
    # Recursion is a no-no
    if other.id == node.id: continue

    for l in other.configuration.get('listen',[]):
      l_spec = l.copy()
      l_spec.setdefault('spec',{})['_id'] = node.id
      if Node.count( **l_spec ):
        other.schedule( context=node )

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

  def __iter__(self):
    for node in __node_backend__.find():
      yield Node(node)

# TODO inherit from celery task?
class Node(object):
  __metaclass__ = NodeType
  
  def __new__(cls, config=None):
    config = config or {}
    if cls==Node and 'type' in config:
      # try to load the module if it's defined
      if config['type'] not in __node_types__ and config.get('module'):
        # Use fromlist argument to load "foo.bar.hello.world". No need to
        # do anything other than ensure that Node types have been defined.
        __import__(config['module'], fromlist=[config['module']])

      # load a specific node based on the short name of the class
      if config['type'] in __node_types__:
        return __node_types__[ config['type'] ].__new__(__node_types__[config['type']], config)
      else:
        
        raise ImportError("Unsupported or unknown node type %s", config['type'])
    return object.__new__(cls, config)
  
  def __init__(self, config=None):
    config = config or {}
    self.configuration = config
    
    if 'type' not in self.configuration and self.__class__ is not Node:
      self.configuration['type'] = self.__class__.__name__
      self.configuration['module'] = self.__class__.__module__

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
  def find_one(self, spec_or_id=None):
    '''
    Return a single node or None.
    '''
    if isinstance(spec_or_id, (str,unicode)):
      spec_or_id = ObjectId(spec_or_id)
    res = __node_backend__.find_one(spec_or_id)
    if res:
      return Node(res)
    return None
  
  @classmethod
  def count(self, *args, **kwargs):
    return __node_backend__.find( **kwargs ).count()

  @classmethod
  def find_iter(self, *args, **kwargs):
    for node in __node_backend__.find( **kwargs ):
      yield Node(node)

  @property
  def input(self):
    rval = getattr(self, '_input', None)
    if not rval and 'input' in self.configuration:
      rval = self._input = Datastore( self, self.configuration['input'] )
    return rval

  @property
  def output(self):
    rval = getattr(self, '_output', None)
    if not rval and 'output' in self.configuration:
      rval = self._output = Datastore( self, self.configuration['output'] )
    return rval

  @property
  def backend(self):
    return Node.backend

  @property
  def id(self):
    return self.configuration.get('_id')

  @property
  def name(self):
    return self.__class__.__name__

  def save(self):
    # TODO also block saving nodes with an unknown type?
    if 'type' not in self.configuration and self.__class__ is not Node:
      self.configuration['type'] = self.__class__.__name__
      self.configuration['module'] = self.__class__.__module__
    self.backend.save( self.configuration )
    return self

  def schedule(self, context=None):
    '''Schedule this node to be run.'''
    # TODO: if not saved, save now so that there's an id
    if '_id' not in self.configuration:
      self.save()
    if context:
      if '_id' not in context.configuration:
        context.save()
      context = str(context.configuration['_id'])
    
    # singleton support
    # TODO: make this so that bugs don't prevent from ever running, i.e.
    # that run_at never gets updated for whatever reason.
    if not self.configuration.get('schedule_at'):
      self.configuration['schedule_at'] = datetime.utcnow()
      self.save()
    elif self.configuration.get('run_at', datetime.fromtimestamp(0)) >= self.configuration['schedule_at']:
      self.configuration['schedule_at'] = datetime.utcnow()
      self.save()
    else:
      return self
   
    # TODO: support apply_async with countdown and/or ETA args 
    run.delay( str(self.configuration['_id']), context_id=context )
    return self

  def runit(self, context=None):
    '''Wrapper around running the node's analysis.'''
    if self.input == None and context:
      self._input = context.output
    self.configuration['run_at'] = datetime.utcnow()
    self.save()

    self.run()
    return self
