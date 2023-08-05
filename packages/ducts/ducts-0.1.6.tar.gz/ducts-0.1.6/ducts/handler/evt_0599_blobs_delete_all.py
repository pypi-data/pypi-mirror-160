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
        handler_spec.set_description('[TEST_USE_ONLY] delete all blobs keys')
        return handler_spec

    async def handle(self, event):
        return await self.delete_all(event.data)

    async def delete_all(self, keyword):
        if keyword != "I'm crazy!":
            raise ValueError('you are too smart to delete all contents!')

        scan_key = self.helper.scan_key_blobs()
        count = 0
        async for key in self.manager.redis.scan_for(scan_key):
            ret = await self.manager.redis.execute('DEL', key)
            logger.info('DELETE|%s|%s', key, ret)
            count += 1
        return count
