
import hashlib
from datetime import datetime
from email.utils import parsedate_to_datetime
from mimetypes import guess_type

import asyncio

from iflb import nameddict
from ifconf import configure_module, config_callback

import logging
logger = logging.getLogger(__name__)
        
@config_callback
def config(loader):
    pass



conf = configure_module(config)

GroupMetadata = nameddict(
    'GroupMetadata',
    (
        'gid'
        , 'group_key'
        , 'group_key_text'
        , 'group_name'
        , 'content_type'
    ))

ContentMetadata = nameddict(
    'ContentMetadata',
    (
        'cid'
        , 'is_dir'
        , 'content_key'
        , 'content_key_name'
#        , 'content_name'
        , 'content_type'
        , 'content_length'
        , 'last_modified'
        , 'encoding'
#        , 'md5'
        , 'order'
        , 'revert_to'
    ))

VERSION_LATEST = 'latest'
KEY_SEPARATOR = '::'


def is_compatible_with_sha1_key(key):
    try:
        return len(key) == 40 and int(key, 16) != 0
    except ValueError:
        return False

def group_key_text_for(key, namespace):
    assert key, 'group_key cannot be blank'
    #assert not is_compatible_with_sha1_key(key), 'group_key must not hash_key but text_key'
    keys = namespace.split(KEY_SEPARATOR) if namespace else []
    keys.extend(key.split(KEY_SEPARATOR))
    return KEY_SEPARATOR.join(filter(lambda v:v, keys))
    
def group_key_for(key, namespace):
    if key:
        if is_compatible_with_sha1_key(key):
            return key
        else:
            return hashlib.sha1(group_key_text_for(key, namespace).encode('UTF-8')).hexdigest()
    else:
        raise KeyError('group_key is empty')


def content_key_for(key):
    if key:
        if is_compatible_with_sha1_key(key):
            return key
        else:
            return hashlib.sha1(key.encode('UTF-8')).hexdigest()
    else:
        raise KeyError('content_key is empty')


def scan_key_blobs():
    return 'BLOBS/*'

def scan_key_blobs_gid(group_id):
    return f'BLOBS/GID={group_id}*'

def scan_key_blobs_gkey():
    return f'BLOBS/GKEY=*/METADATA'

def incr_key_for_group_id():
    return f'BLOBS/GROUP_ID'

def zset_key_for_group_names():
    return f'BLOBS/GROUP_NAMES'

def stream_key_for_group_metadata(group_key):
    return f'BLOBS/GKEY={group_key}/METADATA'

def incr_key_for_content_id(group_id):
    return f'BLOBS/GID={group_id}/CONTENT_ID'

def zset_key_for_content_keys(group_id):
    return f'BLOBS/GID={group_id}/CONTENT_KEYS'

#def stream_key_for_contents_metadata(group_id):
#    return f'BLOBS/GID={group_id}/CONTENTS_METADATA'

#def list_key_for_versions(group_id, content_key):
#    return f'BLOBS/GID={group_id}/CKEY={content_key}/VERSIONS'

def stream_key_for_contents_metadata(group_id, content_key):
    return f'BLOBS/GID={group_id}/CKEY={content_key}/METADATA'

def obj_key_for_content(group_id, content_id, is_dir = 0):
    ctype = 'DIR' if is_dir else 'OBJ'
    return f'BLOBS/GID={group_id}/CID={content_id}/{ctype}'

def stream_key_for_object_buffer():
    return 'BLOBS/BUFFER'

def obj_key_for_object_buffer(session_id, buffer_id):
    return f'BLOBS/BUFFER/{session_id}/{buffer_id}'

def dir_content_file_value(group_key, content_key, version=VERSION_LATEST, is_dir = False):
    assert is_compatible_with_sha1_key(group_key), 'group_key must be sha1 key'
    assert is_compatible_with_sha1_key(content_key), 'content_key must be sha1 key'
    return f'{group_key}.{content_key}.{version}.{1 if is_dir else 0}'

def split_dir_content_file_value(val):
    return {v[0]:v[1] for v in zip(['group_key', 'content_key', 'version', 'is_dir'], val.split('.'))}

async def list_dir_children(redis, group_key, content_key, namespace = ''):
    dir_group, dir_content, dir_version = await get_group_content_metadata_with_version(
        redis
        , group_key
        , content_key
        , namespace)
    redis_key_dir = obj_key_for_content(dir_group.gid, dir_content.cid, is_dir = 1)
    if int(await redis.execute('EXISTS', redis_key_dir)) == 0:
        raise ValueError('Directory not found:[{}/{}] in namespace[{}]'.format(group_key, content_key, namespace))
    return {k:split_dir_content_file_value(v) for k,v in (await redis.hget_all_str(redis_key_dir)).items()}

async def get_group_metadata_with_version(redis, group_key, namespace):
    key = group_key_for(group_key, namespace)
    stream_key = stream_key_for_group_metadata(key)
    stream_id, kv = await redis.xlast_str_with_id(stream_key)
    if not stream_id:
        raise KeyError('group_key[{}] not found.'.format(group_key))
    return (GroupMetadata(kv), stream_id)

async def get_group_metadata(redis, group_key, namespace):
    key = group_key_for(group_key, namespace)
    stream_key = stream_key_for_group_metadata(key)
    kv = await redis.xlast_str(stream_key)
    if not kv:
        raise KeyError('group_key[{}] not found in namespace[{}].'.format(group_key, namespace))
    return GroupMetadata(kv)

async def get_group_content_metadata_with_version(redis, group_key, content_key, namespace):
    group = await get_group_metadata(redis, group_key, namespace)

    key = content_key_for(content_key)
    stream_key = stream_key_for_contents_metadata(group.gid, key)
    stream_id, kv = await redis.xlast_str_with_id(stream_key)
    if not stream_id:
        raise KeyError('content_key [{}] in group[{}::{}] not found.'.format(content_key, namespace, group_key))
    return (group, ContentMetadata(kv), stream_id)
    
async def get_group_content_metadata_for(redis, group_key, content_key, version, namespace):
    if not version or version == VERSION_LATEST:
        return await get_group_content_metadata_with_version(redis, group_key, content_key, namespace)
    
    group = await get_group_metadata(redis, group_key, namespace)
    key = content_key_for(content_key)
    stream_key = stream_key_for_contents_metadata(group.gid, key)
    try:
        ret_version, content_dict = await redis.xget_str_with_id(stream_key, version)
    #except aioredis.errors.ReplyError:  TODO should handle redis client
    except Exception:
        raise KeyError('version[{}] in [{}]'.format(version, stream_key))
        
    content = ContentMetadata(content_dict)
    if not content or content.content_key != key:
        raise KeyError('version[{}] not found in content_key [{}] in group[{}::{}]'.format(version, content_key, namespace, group_key))
    return (group, content, ret_version)

def determine_last_modified(last_modified_in_request):
    if last_modified_in_request:
        try:
            dt = datetime.fromtimestamp(int(last_modified_in_request))
        except ValueError:
            dt = parsedate_to_datetime(last_modified_in_request)
    else:
       dt = datetime.now()
    return int(dt.timestamp())

async def new_content_metadata(params : dict
                               , content_key : str
#                               , content_name : str
                               , content_type : str
                               , encoding : str
                               , last_modified : str):

    metadata = ContentMetadata(params)
    if content_key:
        if is_compatible_with_sha1_key(content_key):
            metadata.content_key = content_key
#            metadata.content_name = content_name
        else:
            metadata.content_key = hashlib.sha1(content_key.encode('UTF-8')).hexdigest()
            metadata.content_key_name = content_key
#            metadata.content_name = content_name if content_name else content_key
#    metadata.content_type = content_type if content_type else guess_type(content_name)[0]
    metadata.content_type = content_type if content_type else guess_type(content_key)[0]
    metadata.last_modified = determine_last_modified(last_modified)
    return metadata

