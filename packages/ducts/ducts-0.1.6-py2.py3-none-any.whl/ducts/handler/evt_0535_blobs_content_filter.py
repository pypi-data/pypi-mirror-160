from ducts.spi import EventHandler, webapi

from io import BytesIO
from hashlib import md5
from datetime import datetime
from functools import partial

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
            call = partial(call, event.data)
        elif isinstance(event.data, list):
            call = partial(call, *event.data)
        elif isinstance(event.data, dict):
            call = partial(call, **event.data)
        elif event.data:
            raise ValueError('invalid argument. data=[{}]'.format(event.data))
        else:
            raise ValueError('group_key is required.')
        async for ret in call():
            yield ret
    
    async def list_contents(self, group_key :str = '', namespace : str = '', **filters) -> list:
        group = await self.helper.get_group_metadata(self.manager.redis, group_key, namespace)
        zkey = self.helper.zset_key_for_content_keys(group.gid)
        for content_key in await self.manager.redis.execute_str('ZRANGE', zkey, 0, -1):
            stream_key = self.helper.stream_key_for_contents_metadata(group.gid, content_key)
            stream_id, kv = await self.manager.redis.xlast_str_with_id(stream_key)
            assert stream_id is not None, 'stream_key must exist'
            if {k:v for k,v in kv.items() if k in filters and filters[k] == v}:
                yield self.helper.ContentMetadata(kv)

    
