from ducts.spi import EventHandler, EventSession

from io import BytesIO
from datetime import datetime
import time
from struct import pack
from itertools import chain
import math
import hashlib

from email.utils import formatdate
from email.utils import parsedate_to_datetime

from aiohttp import web

import traceback
import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):


    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.manager = manager
        self.helper = manager.load_helper_module('helper_blobs')

        handler_spec.set_description('Register Resource')
        return handler_spec

    async def handle(self, event):
        call = self.find_metadata
        if isinstance(event.data, str):
            raise ValueError('invalid argument. data=[{}]'.format(event.data))
        elif isinstance(event.data, list):
            return await call(*event.data)
        elif isinstance(event.data, dict):
            return await call(**event.data)
        elif event.data:
            raise ValueError('invalid argument. data=[{}]'.format(event.data))
        else:
            raise ValueError('group_key is required.')
    
    async def find_metadata(
            self
            , group_key : str
            , path : list
            , namespace : str = ''):
    
        if not group_key:
            raise ValueError('group_key must be given')
        if not path:
            raise ValueError('path must be given')

        if isinstance(path, str):
            path = path.split('/')
        path = filter(lambda v:v, path)
        
        root_group, root_content, version = await self.helper.get_group_content_metadata_with_version(
            self.manager.redis, group_key, '/', namespace)

        current_stack = ['']
        current_group = root_group.group_key
        current_content = root_content.content_key
        current_version = version
        for child in path:
            current_stack.append(child)
            children = await self.helper.list_dir_children(self.manager.redis, current_group, current_content)
            if child not in children:
                return False
            current_content = children[child]['content_key']
        group, content, version = await self.helper.get_group_content_metadata_with_version(
            self.manager.redis, current_group, current_content, '')
        return True
