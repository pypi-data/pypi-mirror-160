from ducts.spi import EventHandler

import time

import asyncio

from ifconf import configure_module, config_callback

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        handler_spec.set_description('called when loop response is ended. message is empty.')
        return handler_spec

    async def handle(self, event):
        return None


