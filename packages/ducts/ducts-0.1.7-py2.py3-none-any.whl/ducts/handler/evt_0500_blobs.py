from ducts.spi import EventHandler, webapi

from io import BytesIO
from hashlib import md5
from datetime import datetime

from aiohttp import web


import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.manager = manager
        self.helper = manager.load_helper_module('helper_blobs')
        handler_spec.set_description('Get Value from Redis Server')
        return handler_spec

    async def run(self, manager):
        self.list_groups = self.manager.get_handler_module('BLOBS_GROUP_LIST').list_groups
        self.list_group_names = self.manager.get_handler_module('BLOBS_GROUP_LIST_NAMES').list_groups
        self.list_contents = self.manager.get_handler_module('BLOBS_CONTENT_LIST').list_contents
        self.list_content_versions = self.manager.get_handler_module('BLOBS_CONTENT_VERSIONS').list_versions
        self.list_content_metadata = self.manager.get_handler_module('BLOBS_CONTENT_METADATA').get_metadata
        self.list_group_versions = self.manager.get_handler_module('BLOBS_GROUP_VERSIONS').list_versions
        self.get_group_metadata = self.manager.get_handler_module('BLOBS_GROUP_METADATA').get_metadata
        self.dir_list_files = self.manager.get_handler_module('BLOBS_DIR_LIST_FILES').list_files
        self.dir_find_metadata = self.manager.get_handler_module('BLOBS_DIR_FILE_METADATA').find_metadata
        
    async def handle(self, event):
        call = self.get_content
        if isinstance(event.data, str):
            raise ValueError('both group_key and content_key are required.')
        elif isinstance(event.data, list):
            coro = call(*event.data)
        elif isinstance(event.data, dict):
            coro = call(**event.data)
        elif event.data:
            raise ValueError('invalid argument. data=[{}]'.format(event.data))
        else:
            raise ValueError('both group_key and content_key are required.')
        content_metadata, data_length = await coro.__anext__()
        async for ret in coro:
            yield ret

    async def get_content(self
                          , group_key : str
                          , content_key : str
                          , version : str = ''
                          , namespace : str = ''
                          , start : int = 0
                          , stop : int = -1):
        if version:
            group, content, version = await self.helper.get_group_content_metadata_for(
                self.manager.redis, group_key, content_key, version, namespace)
        else:
            group, content, version = await self.helper.get_group_content_metadata_with_version(
                self.manager.redis, group_key, content_key, namespace)

        redis_key_blob_data = self.helper.obj_key_for_content(group.gid,  content.cid, content.is_dir)
        content_length = await self.manager.redis.execute('STRLEN', redis_key_blob_data)
        if content_length != int(content.content_length):
            #load from other locations
            pass

        if start == 0 and stop == -1:
            data = await self.manager.redis.execute('GET', redis_key_blob_data)
        elif start > content_length:
            raise ValueError('RequestRangeNotSatisfiable. length=[{}] but start was [{}]'.format(content_length, start))
        else:
            data = await self.manager.redis.execute('GETRANGE', redis_key_blob_data, start, stop)
            
        yield (content, len(data))
        bio = BytesIO(data)
        for buf in iter(lambda: bio.read(1024*1024), b''):
            yield buf
        
    @webapi.add_route(path='/dir{sep1:[/]?}{group_key:[^/]*}{sep2:[/]?}{path:.*}', method='GET')
    async def dir_find(self, request):
        fmt = request.query.get('format', 'metadata')
        #ret = {k: '{}'.format(getattr(request, k)) for k in dir(request)}
        #return web.json_response(ret)
        group_key = request.match_info['group_key']
        path = request.match_info['path']
        #logger.info(f'*********************************{group_key}-{path}')
        if not group_key:
            ret = await self.list_group_names()
            return web.json_response(ret)
        try:
            if not path:
                ret = await self.dir_list_files(group_key, '/')
                return web.json_response(ret)
            version, group, content = await self.dir_find_metadata(group_key, path.split('/'))
            if content.is_dir:
                ret = await self.dir_list_files(group.group_key, content.content_key)
            else:
                ret = [version, group, content]
            if fmt == 'blob':
                await self.load_content(request, group.group_key, content.content_key)
                return 
            else:
                return web.json_response(ret)
        except (KeyError, ValueError, FileNotFoundError) as e:
            logger.exception(f'/{group_key}/{path}', e)
            raise web.HTTPNotFound()
    
    @webapi.add_route(path='/groups', method='GET')
    async def group_names(self, request):
        ret = await self.list_groups()
        return web.json_response(ret)
    
    @webapi.add_route(path='/group_names', method='GET')
    async def group_keys(self, request):
        ret = await self.list_group_names()
        return web.json_response(ret)
    
    @webapi.add_route(path='/groups/{group_key}/metadata', method='GET')
    async def group_metadata(self, request):
        group_key = request.match_info['group_key']
        namespace = ''
        try:
            ret = await self.get_group_metadata(group_key, namespace)
            return web.json_response(ret)
        except KeyError as e:
            raise web.HTTPNotFound()

    @webapi.add_route(path='/groups/{group_key}/versions', method='GET')
    async def group_metadata(self, request):
        group_key = request.match_info['group_key']
        namespace = ''
        try:
            ret = await self.list_group_versions(group_key, namespace)
            return web.json_response(ret)
        except KeyError as e:
            raise web.HTTPNotFound()

    @webapi.add_route(path='/groups/{group_key}/contents', method='GET')
    async def content_keys(self, request):
        group_key = request.match_info['group_key']
        namespace = ''
        try:
            ret = await self.list_contents(group_key, namespace)
            return web.json_response(ret)
        except KeyError as e:
            raise web.HTTPNotFound()

    @webapi.add_route(path='/groups/{group_key}/contents/{content_key}/versions', method='*')
    async def content_versions(self, request):
        group_key = request.match_info['group_key']
        content_key = request.match_info['content_key']
        try:
            ret = await self.list_content_versions(group_key, content_key)
            return web.json_response(ret)
        except KeyError as e:
            raise web.HTTPNotFound()
        
    @webapi.add_route(path='/groups/{group_key}/contents/{content_key}/metadata', method='*')
    async def content_metadata(self, request):
        group_key = request.match_info['group_key']
        content_key = request.match_info['content_key']
        try:
            ret = await self.list_content_metadata(group_key, content_key)
            return web.json_response(ret)
        except KeyError as e:
            raise web.HTTPNotFound()

    @webapi.add_route(path='/groups/{group_key}/contents/{content_key}/versions/{version}/metadata', method='*')
    async def content_metadata_of(self, request):
        group_key = request.match_info['group_key']
        content_key = request.match_info['content_key']
        version = request.match_info['version']
        try:
            ret = await self.list_content_metadata(group_key, content_key, version)
            return web.json_response(ret)
        except KeyError as e:
            raise web.HTTPNotFound()

    #@webapi.add_route(path=r'/blob{sep1:[/]?}{namespace:[^/]*}/{group_key:[^.]+}.{content_key:[^.]+}{sep3:[.]?}{version:[^.]*}', method='*')
    @webapi.add_route(path=r'/blob/{group_key:[^/]+}/{content_key:[^/]+}{sep3:[/]?}{version:[^/]*}', method='*')
    async def service(self, request):
        logger.debug('HEADERS|%s', request.raw_headers)
        try:
            #namespace = request.match_info['namespace']
            namespace = ''
            group_key = request.match_info['group_key']
            content_key = request.match_info['content_key']
            version = request.match_info['version']
            logger.debug('REQUEST|%s, %s, %s, %s.', namespace, group_key, content_key, version)
            await self.load_content(request, group_key, content_key, version, namespace)
            return
        except KeyError as e:
            logger.warning(e)
            raise web.HTTPNotFound()
        
    async def load_content(self, request, group_key, content_key, content_version, namespace = ''):
        group, content, version = await self.helper.get_group_content_metadata_for(
            self.manager.redis, group_key, content_key, content_version, namespace)

        redis_key_blob_data = self.helper.obj_key_for_content(group.gid,  content.cid, content.is_dir)
        content_length = await self.manager.redis.execute('STRLEN', redis_key_blob_data)
        if content_length != int(content.content_length):
            #load from other locations
            pass

        content_range = None
        if request.http_range is None or (request.http_range.start == request.http_range.stop == None):
            http_status = 200
            data = await self.manager.redis.execute('GET', redis_key_blob_data)
        elif request.http_range.start > content_length:
            err = web.HTTPRequestRangeNotSatisfiable()
            err.headers['Content-Range'] = 'bytes {}'.format(content_length)
            raise err
        else:
            http_status = 206
            start = request.http_range.start if request.http_range.start is not None else 0
            stop = request.http_range.stop -1 if request.http_range.stop is not None else content_length - 1
            data = await self.manager.redis.execute('GETRANGE', redis_key_blob_data, start, stop)
            content_range = "bytes {}-{}/{}".format(start, stop, content_length)

        data_length = len(data)
        response = web.StreamResponse(status=http_status)
        response.content_type = content.content_type
        response.content_length = data_length
        response.headers['Accept-Ranges'] = 'bytes'
        if content_range is not None:
            response.headers['Content-Range'] = content_range
        response.headers['ETag'] = content.cid
        await response.prepare(request)
        bio = BytesIO(data)
        for buf in iter(lambda: bio.read(1024*1024), b''):
            await response.write(buf)
        await response.write_eof()



    
