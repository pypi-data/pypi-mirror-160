from ducts.spi import EventHandler, webapi

from io import BytesIO
from hashlib import md5
from datetime import datetime

from aiohttp import web


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
        return await self.list_groups()
    
    async def list_groups(self):
        groups = await self.manager.redis.execute_str('ZRANGE', self.helper.zset_key_for_group_names(), 0, -1)
        return groups
    
