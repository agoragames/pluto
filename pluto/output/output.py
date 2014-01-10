'''
Copyright (c) 2014, Aaron Westendorf All rights reserved.

https://github.com/agoragames/pluto/blob/master/LICENSE.txt
'''

__output_types__ = {}
__output_backend__ = None

class OutputType(type):
  
  def __init__(self, name, bases, dct):
    global __output_types__
    super(OutputType,self).__init__(name, bases, dct)
 
    if globals().get('Output') in bases:
      __output_types__[name] = self

class Output(object):
  __metaclass__ = OutputType
  
  def __new__(cls, configuration={}):
    if cls==Output and 'type' in configuration:
      # load a specific output based on the short name of the class
      if configuration['type'] in __output_types__:
        return __output_types__[ configuration['type'] ]( configuration )
      else:
        raise ImportError("Unsupported or unknown output type %s", configuration['type'])
    return object.__new__(cls, configuration)
  
  def __init__(self, configuration={}):
    self.configuration = configuration

