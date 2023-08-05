from ducts.spi import EventHandler, webapi

import re
from io import BytesIO
from hashlib import md5
from datetime import datetime

from aiohttp import web


import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    PATTERN = r'^(BLOBS/GKEY=)([a-f0-9^]+)(/METADATA)'

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
        scan_key = self.helper.scan_key_blobs_gkey()
        ret = []
        async for key in self.manager.redis.scan_for(scan_key):
            ret.append(re.match(self.PATTERN, key).groups()[1])
        return ret
    
