'''
Copyright (c) 2014, Aaron Westendorf All rights reserved.

https://github.com/agoragames/pluto/blob/master/LICENSE.txt
'''

CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']

BROKER_URL = 'amqp://guest:guest@localhost:5672//'

CELERY_IMPORTS = ('pluto.node',)

# TODO: setup a real backend for nodes
from .node import Node
Node.backend = {}
