
from pluto.node import Node
from datetime import *
import time
from random import randint

class Seed(Node):
  def run(self):
    for x in range(self.configuration['profiles']):
      profile = { 'name' : 'gamer_%d'%(x) }
      day = datetime.utcnow() + timedelta(days=randint(*self.configuration['day_range']))
      profile['updated_at'] = day
      for field in self.configuration['fields']:
        profile[ field ] = randint(*self.configuration['field_range'])
      self.output.client.save( profile )
    print 'Seeded %s %s'%(self.output.client.count(), self.configuration['object'])

class Timeseries(Node):

  def timeseries(self):
    return self.output.timeseries(
      type='histogram',
      read_func=int,
      intervals = {
        'daily' : {
          'step' : 'daily',
        }
      }
    )

  def run(self):
    field = self.configuration['field']
    print 'timeseries on %s over %s records from %s'%(\
      field,
      self.input.client.count(),
      self.input
    )

    series = self.timeseries()

    # HACK: because we don't know the name of the timeseries until now
    series.delete( field )

    for profile in self.input.client.find():
      if profile.get(field):
        # HACK: see https://github.com/agoragames/kairos/issues/39
        stamp = time.mktime( profile['updated_at'].timetuple() )
        series.insert( field, profile[field], timestamp=stamp )

class Report(Node):
  def run(self):
    transforms = ['min', 'max', 'mean', 'sum']
    for node in Node:
      print '%s ran at %s'%( node.name, node.configuration.get('run_at') )

    seed = Node.find_one({'type':'Seed'})
    print 'Seed'
    print '================================='
    print 'Generated %d %s'%( seed.output.client.count(), seed.configuration['object'] )
    print '-\n'
    print '-\n'

    kills = Node.find_one({'type':'Timeseries', 'field':'kills'})
    props = kills.timeseries().properties('kills')
    print 'Kills'
    print '================================='
    print 'Kills from %s to %s'%( datetime.utcfromtimestamp(props['daily']['first']), datetime.utcfromtimestamp(props['daily']['last']))
    for (stamp,data) in kills.timeseries().iterate('kills', 'daily', transform=transforms):
      print datetime.utcfromtimestamp(stamp)
      for transform in transforms:
        print '____%s: %s'%(transform, data[transform])
    print '-\n'
    print '-\n'

    deaths = Node.find_one({'type':'Timeseries', 'field':'deaths'})
    props = deaths.timeseries().properties('deaths')
    print 'Deaths'
    print '================================='
    print 'Deaths from %s to %s'%( datetime.utcfromtimestamp(props['daily']['first']), datetime.utcfromtimestamp(props['daily']['last']))
    for (stamp,data) in deaths.timeseries().iterate('deaths', 'daily', transform=transforms):
      print datetime.utcfromtimestamp(stamp)
      for transform in transforms:
        print '____%s: %s'%(transform, data[transform])
    print '-\n'
    print '-\n'
