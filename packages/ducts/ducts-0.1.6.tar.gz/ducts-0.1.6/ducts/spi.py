import os
import sys
from pathlib import Path
import importlib
from importlib import machinery
import abc
import inspect

from collections import namedtuple
from collections import OrderedDict
from collections import defaultdict
from enum import Enum

import asyncio

import logging

class EventHandler(metaclass=abc.ABCMeta):

    ATTR_KEY = 'KEY'

    @abc.abstractmethod
    async def setup(self, handler_spec, manager):
        '''
        called onece when server starts setup process.
        coroutine returned by this method is awaited by the manager
        '''
        pass
    
    async def run(self, manager):
        '''
        called onece when server is started.
        coroutine returned by this method is passed to ensure_future method
        '''
        pass
    
    @abc.abstractmethod
    async def handle(self, event):
        '''
        called when messaged is passed by the client.
        '''
        pass
    
    async def handle_connected(self, event_session):
        '''
        called when the new session is started.
        '''
        pass

    async def handle_wait_reconnect(self, event_session):
        '''
        called when the connection failure is detected.
        '''
        pass

    async def handle_closed(self, event_session):
        '''
        called when the session is closed.
        '''
        pass

class HandlerSpec():

    def __init__(self, id, key, callback):
        self.id = id
        self.key = key
        self.callback = callback
        self.responsive = False
        self.description = ''
        self.webapi_context = key.lower()
        
        #self.input_sample = None
        #self.output_sample = None

    def __str__(self):
        return '{}({})-{}:{}'.format(type(self), id(self), self.id, self.key)
        
    def __repr__(self):
        return '{}({})-{}:{}'.format(type(self), id(self), self.id, self.key)
        
    def set_as_responsive(self):
        self.responsive = True
        
    def set_description(self, description):
        self.description = description

    def set_webapi_context(self, webapi_context):
        self.webapi_context = webapi_context

    def _asdict(self):
        return OrderedDict([(key,getattr(self, key))for key in ['id', 'key', 'callback', 'responsive', 'description']])
    
class webapi(object):

    apis = defaultdict(dict)

    @classmethod
    def add_route(cls, path='', method='*'):
        '''
        use this decorator to add webapi route
        '''
        def deco(func):
            cls.apis[func.__module__][path] = ('add_route', method, func.__name__)
            return func
        return deco

class EventHandlerManager(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def redis(self):
        pass

    @abc.abstractmethod
    def load_helper_module(self, module_name):
        pass

    @abc.abstractmethod
    def get_handler_module(self, event_name):
        pass

    @abc.abstractmethod
    def get_handler_for(self, event_id):
        pass

    @abc.abstractmethod
    def handlers(self):
        pass

    @abc.abstractmethod
    async def has_server_attribute(self, key):
        pass

    @abc.abstractmethod
    async def get_server_attribute(self, key):
        pass

    @abc.abstractmethod
    async def set_server_attribute(self, key, value):
        pass

    
class Event(object):

    def __init__(self, event_id, event_session, data = None):
        assert event_id >= 0, 'event_id cannot be negative.'
        assert event_session, 'event_session cannot be null.'
        self.id = event_id
        self.session = event_session
        self.data = data

        
class EventSession(metaclass=abc.ABCMeta):

    def __init__(self):
        self._local_property = {}

    @property
    def local_property(self):
        return self._local_property

    #@property
    @abc.abstractmethod
    def request_id(self):
        pass

    #@property
    @abc.abstractmethod
    def session_id(self):
        pass

    @property
    @abc.abstractmethod
    def loop(self):
        pass

    @property
    @abc.abstractmethod
    def redis(self):
        pass

    @abc.abstractmethod
    async def has_session_attribute(self, key):
        pass

    @abc.abstractmethod
    async def get_session_attribute(self, key):
        pass

    @abc.abstractmethod
    async def set_session_attribute(self, key, value):
        pass

    @abc.abstractmethod
    async def has_server_attribute(self, key):
        pass

    @abc.abstractmethod
    async def get_server_attribute(self, key):
        pass

    @abc.abstractmethod
    async def set_server_attribute(self, key, value):
        pass

    @abc.abstractmethod
    async def is_closed(self):
        pass

class RedisClient(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    async def execute(self, cmd, *args):
        pass
            
    @abc.abstractmethod
    async def execute_str(self, cmd, *args):
        pass
            
    @abc.abstractmethod
    async def subscribe(self, key):
        pass
        
    @abc.abstractmethod
    async def unsubscribe(self, key_or_channel):
        pass
        
    @abc.abstractmethod
    async def psubscribe(self, key):
        pass
        
    @abc.abstractmethod
    async def punsubscribe(self, key_or_channel):
        pass
        
    @abc.abstractmethod
    async def xadd(self, streamkey, *args, **kwargs):
        pass
    
    @abc.abstractmethod
    async def xadd_and_publish(self, pubkey, streamkey, *args, **kwargs):
        pass

    @abc.abstractmethod
    async def xget_str(self, streamkey, stream_id):
        pass

    @abc.abstractmethod
    async def xlast_str(self, streamkey):
        pass

    @abc.abstractmethod
    async def psub_and_xrange_str(self, subkey, streamkey, last_count = 0):
        pass
        
    @abc.abstractmethod
    async def psub_and_xrange_str_for_each_id(self, subkey, streamkey):
        pass

