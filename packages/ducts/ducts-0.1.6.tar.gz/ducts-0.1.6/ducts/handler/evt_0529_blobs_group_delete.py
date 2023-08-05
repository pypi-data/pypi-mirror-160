from ducts.spi import EventHandler, EventSession

from io import BytesIO
from datetime import datetime
from itertools import chain
import math
import hashlib
import struct

from mimetypes import guess_type
from email.utils import formatdate
from email.utils import parsedate_to_datetime

from aiohttp import web

import traceback
import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    SCRIPT='''\
local redis_key_group_metadata = KEYS[1];
local redis_key_group_names = KEYS[2];
local group_key = ARGV[1];
local group_name_with_key_new = ARGV[2];
local group_name_with_key_old = ARGV[3];
local stream_id = redis.call("XADD", redis_key_group_metadata, "*", unpack(ARGV, 4, table.maxn(ARGV)));
redis.call("ZREM", redis_key_group_names, group_name_with_key_old);
redis.call("ZADD", redis_key_group_names, 0, group_name_with_key_new);
return stream_id;
'''

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.manager = manager
        self.helper = manager.load_helper_module('helper_blobs')

        handler_spec.set_description('Register Resource')
        return handler_spec

    async def handle(self, event):
        call = self.delete
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
    
    
    async def delete(self, group_key : str, namespace : str = '') -> int:
        metadata = await self.helper.get_group_metadata(self.manager.redis, group_key, namespace)
        count = 0
        
        scan_key = self.helper.scan_key_blobs_gid(metadata.gid)
        async for key in self.manager.redis.scan_for(scan_key):
            ret = await self.manager.redis.execute('DEL', key)
            logger.info('DELETE|%s|%s', key, ret)
            count += 1
        redis_key_group_metadata = self.helper.stream_key_for_group_metadata(metadata.group_key)
        ret = await self.manager.redis.execute('DEL', redis_key_group_metadata)
        count += 1
        
        return count

