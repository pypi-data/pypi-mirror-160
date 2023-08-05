from ducts.spi import EventHandler, webapi

from aiohttp import web

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.manager = manager
        handler_spec.set_description('イベント情報を返します。')
        handler_spec.set_as_responsive()
        return handler_spec

    async def handle(self, event):
        return await event.session.redis.execute(event.data[0], *event.data[1:])

    @webapi.add_route(path='/', method='GET')
    async def get(self, request):
        return web.json_response(self.manager.key_ids)

    @webapi.add_route(path='/{id}', method='GET')
    async def get_by_id(self, request):
        eid = int(request.match_info['id'])
        return web.json_response(self.manager.get_handler_for(eid)[1].SPEC._asdict())

