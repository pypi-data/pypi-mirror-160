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
#            , filename : str
#            , namespace : str
#            , group_key : str
#            , content_key : str
    
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

        file_keys = {}
        for i,f in enumerate(files):
            if 'filename' not in f:
                raise ValueError('filename is empty. files[{}]=[{}]'.format(i,f))
            if 'content_key' not in f:
                raise ValueError('content_key is empty. files[{}]=[{}]'.format(i,f))
            filename = f['filename']
            file_content_key = f['content_key']
            if filename in file_keys:
                raise ValueError('filename[{}] is duplicated. files[{}]=[{}]'.format(filename, i, f))
            if int(await self.manager.redis.execute('HEXISTS', redis_key_dir, filename)) > 0:
                raise ValueError('filename[{}] already exists in directory[{}/{}] in namespace[{}].'.format(filename, group_key, content_key, namespace))
            file_group, file_content, file_version = await self.helper.get_group_content_metadata_with_version(
                self.manager.redis
                , f['group_key'] if 'group_key' in f and f['group_key'] else group_key
                , file_content_key
                , f['namespace'] if 'namespace' in f and f['namespace'] else namespace)
            file_keys[filename] = self.helper.dir_content_file_value(file_group.group_key, file_content.content_key, is_dir = file_content.is_dir)
            
        ret = await self.manager.redis.evalsha(
            Handler.SCRIPT
            , 2
            , redis_key_contents_metadata, redis_key_dir
            , len(file_keys), *chain.from_iterable(file_keys.items()), *chain.from_iterable(dir_content.items()))
        return {k:self.helper.split_dir_content_file_value(v) for k,v in (await self.manager.redis.hget_all_str(redis_key_dir)).items()}


