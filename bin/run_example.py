#!/usr/bin/env python

import copy

from pluto.node import Node
from example import *

configuration = {
  #'input' : {
    #'type'    : 'mongo',
    #'db'      : 'example',
  #},
  'output' : {
    'type'    : 'mongo',
    'db'      : 'example',
  },
  'environment'   : 'customer'
}

def config(c={}):
  rval = copy.deepcopy(configuration)
  rval.update(c)
  return rval

print 'init backend'
Node.backend = {}
Node.backend.drop()

print 'seeding values'
s = Seed( config({
  'object': 'profile',
  'profiles' : 500,
  'fields' : ['kills', 'deaths', 'maim'],
  'field_range': [10,100],
  'day_range' : [-7, 0]
}) )

print 'generating timeseries'
k = Timeseries( config({
  'field':'kills',
  'listen': [
    {'spec':{'type':'Seed', 'environment':'customer', 'object':'profile'}}
  ]
}) ).save()
d = Timeseries( config({
  'field':'deaths',
  'listen': [
    {'spec':{'type':'Seed', 'environment':'customer', 'object':'profile'}}
  ]
}) ).save()

print 'generating report'
r = Report( config({
  'listen': [
    {'spec':{'environment':'customer', 'type':'Timeseries', 'field':'deaths'}}
  ]
}) ).save()

s.output.client.drop()
k.output.client.drop()
d.output.client.drop()

s.schedule()
