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
        call = self.list_versions
        if isinstance(event.data, str):
            raise ValueError('both group_key and content_key are required.')
        elif isinstance(event.data, list):
            return await call(*event.data)
        elif isinstance(event.data, dict):
            return await call(**event.data)
        elif event.data:
            raise ValueError('invalid argument. data=[{}]'.format(event.data))
        else:
            raise ValueError('both group_key and content_key are required.')
        
    async def list_versions(self, group_key : str, content_key : str, version : str = '+', namespace : str = '', count = 10) -> dict:
        group = await self.helper.get_group_metadata(self.manager.redis, group_key, namespace)

        ret = await self.manager.redis.xrevrange_str(
            self.helper.stream_key_for_contents_metadata(group.gid, content_key)
            , start = version, stop = '-', count = count)
        return list(ret)

