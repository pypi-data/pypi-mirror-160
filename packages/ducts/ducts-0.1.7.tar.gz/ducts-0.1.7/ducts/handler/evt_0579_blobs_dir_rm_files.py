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
local file_end_index = 1 + num_files 
redis.call("HDEL", redis_key_contents_object, unpack(ARGV, file_start_index, file_end_index));
local stream_id = redis.call("XADD", redis_key_contents, "*", unpack(ARGV, file_start_index + num_files, table.maxn(ARGV)));
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
            , content_key : str
            , namespace : str = ''
            , files : list = []):
    
        if not group_key:
            raise ValueError('group_key must be given')
        if not content_key:
            raise ValueError('content_key must be given')

        # if not file_content_key:
        #     raise ValueError('file_content_key must be given')
        # if not filename:
        #     raise ValueError('filename must be given')

        dir_group, dir_content, dir_version = await self.helper.get_group_content_metadata_with_version(
            self.manager.redis
            , group_key
            , content_key
            , namespace)
        dir_content.last_modified = self.helper.determine_last_modified(time.time())
        
        redis_key_contents_metadata = self.helper.stream_key_for_contents_metadata(dir_group.gid, dir_content.content_key)
        redis_key_dir = self.helper.obj_key_for_content(dir_group.gid, dir_content.cid, is_dir = 1)
        if int(await self.manager.redis.execute('EXISTS', redis_key_dir)) == 0:
            raise ValueError('Directory not found:[{}/{}] in namespace[{}]'.format(group_key, content_key, namespace))

        files = {files} if isinstance(files, str) else {entry if isinstance(entry, str) else entry['filename'] for entry in files}
        not_found = files - set(await self.manager.redis.execute_str('HKEYS', redis_key_dir))
        if not_found:
            raise ValueError('filename[{}] not dound.'.format(not_dound))
            
        ret = await self.manager.redis.evalsha(
            Handler.SCRIPT
            , 2
            , redis_key_contents_metadata, redis_key_dir
            , len(files), *files, *chain.from_iterable(dir_content.items()))
        return {k:self.helper.split_dir_content_file_value(v) for k,v in (await self.manager.redis.hget_all_str(redis_key_dir)).items()}


