#!/usr/bin/env python

from pluto.node import Node
from example import *

configuration = {
  'input' : {
    'type'    : 'mongo',
    'db'      : 'example',
  },
  'output' : {
    'type'    : 'mongo',
    'db'      : 'example',
  },
  'environment'   : 'customer'
}

def config(c={}):
  rval = configuration.copy()
  rval.update(c)
  return rval

print 'init backend'
Node.backend = {}
Node.backend.drop()

print 'seeding values'
s = Seed( config() )
s.schedule()

print 'generating timeseries'
k = Timeseries( config({
  'field':'kills',
  'listen': [
    {'spec':{'type':'Seed', 'environment':'customer'}}
  ]
}) ).save()
d = Timeseries( config({
  'field':'deaths',
  'listen': [
    {'spec':{'type':'Seed', 'environment':'customer'}}
  ]
}) ).save()
