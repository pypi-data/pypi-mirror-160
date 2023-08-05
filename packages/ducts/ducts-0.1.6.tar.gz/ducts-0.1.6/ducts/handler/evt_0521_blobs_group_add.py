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
local group_key_name = ARGV[2];
local stream_id = redis.call("XADD", redis_key_group_metadata, "*", unpack(ARGV, 3, table.maxn(ARGV)));
if group_key_name ~= "::" then
  redis.call("ZADD", redis_key_group_names, 0, group_key_name);
end
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
        call = self.add_group
        if isinstance(event.data, str):
            return await call(event.data)
        elif isinstance(event.data, list):
            return await call(*event.data)
        elif isinstance(event.data, dict):
            return await call(**event.data)
        elif event.data:
            raise ValueError('invalid argument. data=[{}]'.format(event.data))
        else:
            return await call()

    async def add_group(self, group_key : str = '', namespace : str = '', content_type : str = '', **other_params):
        metadata = self.helper.GroupMetadata(other_params.copy())
        metadata.content_type = content_type if content_type else 'application/octet-stream'

        if group_key:
            if self.helper.is_compatible_with_sha1_key(group_key):
                metadata.group_key = group_key
            else:
                group_key = self.helper.group_key_text_for(group_key, namespace)
                metadata.group_key = hashlib.sha1(group_key.encode('UTF-8')).hexdigest()
                metadata.group_key_text = group_key
            if int(await self.manager.redis.execute('EXISTS', self.helper.stream_key_for_group_metadata(metadata.group_key))) > 0:
                raise KeyError('group_key:[{}] already exits.'.format(group_key))
            metadata.gid = await self.manager.redis.execute('INCR', self.helper.incr_key_for_group_id())
        else:
            metadata.gid = await self.manager.redis.execute('INCR', self.helper.incr_key_for_group_id())
            metadata.group_key = group_key if group_key else hashlib.sha1(struct.pack('i', metadata.gid)+struct.pack('d', datetime.now().timestamp())).hexdigest()
        
        redis_key_group_metadata = self.helper.stream_key_for_group_metadata(metadata.group_key)
        redis_key_group_names = self.helper.zset_key_for_group_names()
        group_key_name = metadata.group_key_text if metadata.group_key_text else '::' #'::' means ignore in script.

        ret = await self.manager.redis.evalsha(
            Handler.SCRIPT
            , 2
            , redis_key_group_metadata, redis_key_group_names
            , metadata.group_key, group_key_name, *chain.from_iterable(metadata.items()))
        return metadata.group_key
            


