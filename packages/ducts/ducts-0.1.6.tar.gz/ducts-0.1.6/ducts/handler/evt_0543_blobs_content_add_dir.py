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

    SCRIPT='''\
local redis_key_contents = KEYS[1];
local redis_key_contents_object = KEYS[2];
local redis_key_contents_keys = KEYS[3];
local content_key = ARGV[1];
local content_order = ARGV[2];
local dir_name = ARGV[3];
local dir_value = ARGV[4];
redis.call("HSET", redis_key_contents_object, dir_name, dir_value);
local stream_id = redis.call("XADD", redis_key_contents, "*", unpack(ARGV, 5, table.maxn(ARGV)));
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
        call = self.add_content
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
            , group_key : str
            , content_key : str = ''
            , order : int = ''
            , namespace :str = ''
            , **other_params):
        
        if not group_key:
            raise ValueError('group_key must be set')

        group = await self.helper.get_group_metadata(self.manager.redis, group_key, namespace)
        metadata = await self.helper.new_content_metadata(other_params.copy()
                                                          , content_key
                                                          , 'application/json'
                                                          , 'UTF-8'
                                                          , time.time())

        index = await self.manager.redis.execute('INCR', self.helper.incr_key_for_content_id(group.gid))
        metadata.cid = index
        metadata.order = order if order else index * 10
        
        metadata.is_dir = 1
        redis_key_contents_object = self.helper.obj_key_for_content(group.gid, metadata.cid, metadata.is_dir)
        assert int(await self.manager.redis.execute('EXISTS', redis_key_contents_object)) == 0, 'cid must be unique, [{}]'.format(index)
        
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
            , 3
            , redis_key_contents_metadata, redis_key_contents_object, redis_key_contents_keys
            , metadata.content_key, metadata.order, '.', self.helper.dir_content_file_value(group.group_key, metadata.content_key, is_dir=1), *chain.from_iterable(metadata.items()))
        return {'group_key': group.group_key, 'content_key': metadata.content_key}
            


