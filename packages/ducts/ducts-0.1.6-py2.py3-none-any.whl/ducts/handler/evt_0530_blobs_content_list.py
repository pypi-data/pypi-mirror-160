from ducts.spi import EventHandler, webapi

from io import BytesIO
from hashlib import md5
from datetime import datetime

import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.manager = manager
        self.helper = manager.load_helper_module('helper_blobs')
        handler_spec.set_description('Get Value from Redis Server')
        return handler_spec

    async def handle(self, event):
        call = self.list_contents
        if isinstance(event.data, str):
            return await call(event.data)
        elif isinstance(event.data, list):
            return await call(*event.data)
        elif isinstance(event.data, dict):
            return await call(**event.data)
        elif event.data:
            raise ValueError('invalid argument. data=[{}]'.format(event.data))
        else:
            raise ValueError('group_key is required.')
    
    async def list_contents(self, group_key :str = '', namespace : str = '', **params) -> list:
        group = await self.helper.get_group_metadata(self.manager.redis, group_key, namespace)
        zkey = self.helper.zset_key_for_content_keys(group.gid)
        contents = await self.manager.redis.execute_str('ZRANGE', zkey, 0, -1)
        return contents
    
