from ducts.spi import EventHandler

from io import BytesIO
from datetime import datetime
from hashlib import md5, sha1, sha256
from struct import pack
from itertools import chain

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
        handler_spec.set_description('open buffer')
        return handler_spec

    async def handle(self, event):
        return await self.open_buffer(event.session.session_id())

    async def open_buffer(self, session_id):
        redis_key_buffer_keys = self.helper.stream_key_for_object_buffer()
        kv = {'sid': session_id}
        stream_id = await self.manager.redis.execute('XADD', redis_key_buffer_keys, '*', *chain.from_iterable(kv.items()))
        buffer_id = sha1(stream_id).hexdigest()
        redis_key_for_object_buffer = self.helper.obj_key_for_object_buffer(session_id, buffer_id)
        await self.manager.redis.execute('SET', redis_key_for_object_buffer, '')
        return buffer_id
        
