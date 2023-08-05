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
local redis_key_contents = KEYS[1];
local redis_key_contents_object = KEYS[2];
local redis_key_contents_keys = KEYS[3];
local content_key = ARGV[1];
local content_order = ARGV[2];
local content = ARGV[3];
if content ~= "" then
  redis.call("SET", redis_key_contents_object, content);
end
local stream_id = redis.call("XADD", redis_key_contents, "*", unpack(ARGV, 4, table.maxn(ARGV)));
redis.call("ZADD", redis_key_contents_keys, content_order, content_key);
return stream_id;
'''
    
    SCRIPT_METADATA_ONLY='''\
local redis_key_contents = KEYS[1];
local redis_key_contents_keys = KEYS[2];
local content_key = ARGV[1];
local content_order = ARGV[2];
local stream_id = redis.call("XADD", redis_key_contents, "*", unpack(ARGV, 3, table.maxn(ARGV)));
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
        call = self.update_content
        if isinstance(event.data, str):
            raise ValueError('invalid argument. update parameters are required. data=[{}]'.format(event.data))
        elif isinstance(event.data, list):
            return await call(*event.data)
        elif isinstance(event.data, dict):
            return await call(**event.data)
        elif event.data:
            raise ValueError('invalid argument. data=[{}]'.format(event.data))
        else:
            raise ValueError('update parameters are required. data=[{}]'.format(event.data))
        #return await self.update_content(event.session, event.data[0], event.data[1], event.data[2], event.data[3] if len(event.data) > 3 else {})

    async def update_content(
            self
            , group_key : str
            , content_key : str
            , content : bytes
            , namespace : str = ''
            , **update_params):
        
        if not group_key:
            raise ValueError('group_key must be given')
        if not content_key:
            raise ValueError('content_key must be given')
        if not isinstance(update_params, dict):
            raise ValueError('update_dict must be an instance of dict')
        
        group, metadata, version = await self.helper.get_group_content_metadata_with_version(
            self.manager.redis, group_key, content_key, namespace)
        
        old = metadata.copy()
        metadata.update(update_params)

        if metadata.cid != old.cid:
            raise ValueError('cid was expeccted to be [{}] but was [{}].'.format(old.cid, metadata.cid))

        if metadata.content_key != old.content_key:
            raise ValueError('content_key was expeccted to be [{}] but was [{}].'.format(old.content_key, metadata.content_key))

        redis_key_contents_metadata = self.helper.stream_key_for_contents_metadata(group.gid, metadata.content_key)
        redis_key_contents_keys = self.helper.zset_key_for_content_keys(group.gid)
        
        if not content:
            if old == content:
                return version
            else:
                ret = await self.manager.redis.evalsha(
                    Handler.SCRIPT_METADATA_ONLY
                    , 2
                    , redis_key_contents_metadata, redis_key_contents_keys
                    , metadata.content_key, metadata.order, *chain.from_iterable(metadata.items()))
                return {'group_key': group.group_key, 'content_key': metadata.content_key, 'version': ret.decode('UTF-8')}

        if isinstance(content, str):
            metadata.encoding = metadata.encoding if metadata.encoding else 'UTF-8'
            content = content.encode(metadata.encoding)
        elif not isinstance(content, bytes):
            raise ValueError('content must be str or bytes but was {}'.format(type(content)))
    
        metadata.content_length = len(content)
        metadata.cid = hashlib.sha1(content).hexdigest()
        redis_key_contents_object = self.helper.obj_key_for_content(group.gid, metadata.cid)
        if int(await self.manager.redis.execute('EXISTS', redis_key_contents_object)) > 0:
            content = ''

        if old.last_modified == metadata.last_modified:
            metadata.last_modified = int(datetime.now().timestamp())
        else:
            metadata.last_modified = self.helper.determine_last_modified(metadata.last_modified)
        
        ret = await self.manager.redis.evalsha(
            Handler.SCRIPT
            , 3
            , redis_key_contents_metadata, redis_key_contents_object, redis_key_contents_keys
            , metadata.content_key, metadata.order, content, *chain.from_iterable(metadata.items()))
        return {'group_key': group.group_key, 'content_key': metadata.content_key, 'version': ret.decode('UTF-8')}
        
