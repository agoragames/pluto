'''
Copyright (c) 2014, Aaron Westendorf All rights reserved.

https://github.com/agoragames/pluto/blob/master/LICENSE.txt
'''

__input_types__ = {}
__input_backend__ = None

class InputType(type):
  
  def __init__(self, name, bases, dct):
    global __input_types__
    super(InputType,self).__init__(name, bases, dct)
 
    if globals().get('Input') in bases:
      __input_types__[name] = self

class Input(object):
  __metaclass__ = InputType
  
  def __new__(cls, configuration={}):
    if cls==Input and 'type' in configuration:
      # load a specific input based on the short name of the class
      if configuration['type'] in __input_types__:
        return __input_types__[ configuration['type'] ]( configuration )
      else:
        raise ImportError("Unsupported or unknown input type %s", configuration['type'])
    return object.__new__(cls, configuration)
  
  def __init__(self, configuration={}):
    self.configuration = configuration
