from ducts.spi import EventHandler

from io import BytesIO
from datetime import datetime
from hashlib import md5, sha1, sha256
from struct import pack
from itertools import chain
from functools import partial

from mimetypes import guess_type
from email.utils import formatdate
from email.utils import parsedate_to_datetime

from aiohttp import web

import traceback
import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.manager = manager
        self.helper = manager.load_helper_module('helper_blobs')
        handler_spec.set_description('add buffer data')
        return handler_spec

    async def handle(self, event):
        call = partial(self.add_to_buffer, event.session.session_id())
        if isinstance(event.data, str):
            raise ValueError('invalid argument. buffer_id and buffer_data are required. data=[{}]'.format(event.data))
        elif isinstance(event.data, list):
            return await call(*event.data)
        elif isinstance(event.data, dict):
            return await call(**event.data)
        elif event.data:
            raise ValueError('invalid argument. data=[{}]'.format(event.data))
        else:
            raise ValueError('invalid argument. buffer_id and buffer_data are required. data=[{}]'.format(event.data))
        #return await self.add_to_buffer(event.session.session_id(), event.data[0], event.data[1])

    async def add_to_buffer(self, session_id, buffer_id, buffer_data):
        if not buffer_id:
            raise ValueError('buffer_id cannot be null')
        if not buffer_data:
            raise ValueError('buffer data cannot be null')

        redis_key_for_object_buffer = self.helper.obj_key_for_object_buffer(session_id, buffer_id)
        
        if not await self.manager.redis.execute('EXISTS', redis_key_for_object_buffer):
            raise ValueError('buffer_id[{}] not found in session[{}]'.format(buffer_id, session_id))

        return await self.manager.redis.execute('APPEND', redis_key_for_object_buffer, buffer_data)
