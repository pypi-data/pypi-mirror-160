from ducts.spi import EventHandler, EventSession

from io import BytesIO
from datetime import datetime
from struct import pack
from itertools import chain
from functools import partial
import math
import hashlib

from mimetypes import guess_type
from email.utils import formatdate
from email.utils import parsedate_to_datetime

from aiohttp import web

import traceback
import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    SCRIPT='''\
local redis_key_contents = KEYS[1];
local redis_key_contents_object = KEYS[2];
local redis_key_contents_keys = KEYS[3];
local redis_key_contents_object_buffer = KEYS[4];
local content_key = ARGV[1];
local content_order = ARGV[2];
local content_exists = ARGV[3];
if content_exists == "0" then
  redis.call("RENAME", redis_key_contents_object_buffer, redis_key_contents_object);
else
  redis.call("DEL", redis_key_contents_object_buffer);
end
local stream_id = redis.call("XADD", redis_key_contents, "*", unpack(ARGV, 4, table.maxn(ARGV)));
redis.call("ZADD", redis_key_contents_keys, content_order, content_key);
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
        call = partial(self.add_content, event.session.session_id())
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

    async def add_content(
            self
            , session_id : str
            , group_key : str
            , buffer_key : str
            , content_key : str = ''
            , content_type : str = ''
            , encoding : str =''
            , last_modified : str = ''
            , order : int = ''
            , namespace :str = ''
            , **other_params):
        if not session_id:
            raise ValueError('session_id must be given')
        if not group_key:
            raise ValueError('group_key must be given')
        if not buffer_key:
            raise ValueError('buffer_key must be given')
        if not isinstance(buffer_key, str):
            raise ValueError('buffer_key mus be string but was {}'.format(type(content)))

        group = await self.helper.get_group_metadata(self.manager.redis, group_key, namespace)
        metadata = await self.helper.new_content_metadata(other_params.copy()
                                                          , content_key
                                                          , content_type
                                                          , encoding
                                                          , last_modified)
        
        metadata.content_type = metadata.content_type if metadata.content_type else 'application/octet-stream'
        if encoding:
            metadata.encoding = encoding
        
        redis_key_contents_object_buffer = self.helper.obj_key_for_object_buffer(session_id, buffer_key)
        content_length = await self.manager.redis.execute('STRLEN', redis_key_contents_object_buffer)
        sha1 = hashlib.sha1()
        buf_len = sha1.block_size * 4096
        start = 0
        while start <= content_length:
            end = start + buf_len - 1
            buf = await self.manager.redis.execute('GETRANGE', redis_key_contents_object_buffer, start, end)
            sha1.update(buf)
            start += buf_len
            
        metadata.content_length = content_length
        metadata.cid = sha1.hexdigest()

        index = await self.manager.redis.execute('INCR', self.helper.incr_key_for_content_id(group.gid))
        metadata.order = order if order else index * 10

        redis_key_contents_object = self.helper.obj_key_for_content(group.gid, metadata.cid)
        content_exists = int(await self.manager.redis.execute('EXISTS', redis_key_contents_object)) 
        
        if metadata.content_key:
            if int(await self.manager.redis.execute('EXISTS', self.helper.stream_key_for_contents_metadata(group.gid, metadata.content_key))) > 0:
                raise KeyError('content_key:[{}/{}] already exits.'.format(group_key, content_key))
            else:
                pass
        else:
            metadata.content_key = hashlib.sha1(redis_key_contents_object.encode('UTF-8')).hexdigest()
        
        redis_key_contents_metadata = self.helper.stream_key_for_contents_metadata(group.gid, metadata.content_key)
        redis_key_contents_keys = self.helper.zset_key_for_content_keys(group.gid)

        ret = await self.manager.redis.evalsha(
            Handler.SCRIPT
            , 4
            , redis_key_contents_metadata, redis_key_contents_object, redis_key_contents_keys, redis_key_contents_object_buffer
            , metadata.content_key, metadata.order, content_exists, *chain.from_iterable(metadata.items()))
        return {'group_key': group.group_key, 'content_key': metadata.content_key}
            


