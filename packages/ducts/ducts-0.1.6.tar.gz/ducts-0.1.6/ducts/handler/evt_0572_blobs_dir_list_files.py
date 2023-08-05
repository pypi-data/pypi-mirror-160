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
local num_files = ARGV[1];
local file_start_index = 2
for i = 0, num_files - 1 do
  redis.call("HSET", redis_key_contents_object, ARGV[file_start_index + 2*i], ARGV[file_start_index + 2*i + 1]);
end
local stream_id = redis.call("XADD", redis_key_contents, "*", unpack(ARGV, file_start_index + 2 * num_files, table.maxn(ARGV)));
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
        call = self.list_files
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
    
    async def list_files(
            self
            , group_key : str
            , content_key : str
            , namespace : str = ''):
    
        if not group_key:
            raise ValueError('group_key must be given')
        if not content_key:
            raise ValueError('content_key must be given')

        return await self.helper.list_dir_children(
            self.manager.redis
            , group_key
            , content_key
            , namespace)


