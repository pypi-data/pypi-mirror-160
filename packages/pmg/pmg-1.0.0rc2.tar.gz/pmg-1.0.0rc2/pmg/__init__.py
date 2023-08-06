import builtins
import collections
import collections.abc
import datetime
import decimal
import functools
import hashlib
import itertools
import json
import logging
import numbers
import os
import random
import re
import socket
import sys
import time
import traceback
import typing
import uuid
import zoneinfo


# Configuration helpers

def get_config(key, default_value=None):
    if default_value is None:
        assert f"PMG_{key}" in os.environ, f"Configuration key {key} (environment variable PMG_{key}) not found."
    return os.environ.get(f"PMG_{key}", default_value)

def get_config_keys(pattern):
    import fnmatch
    return {k[4:]: v for k, v in os.environ.items() if k.startswith('PMG_') and fnmatch.fnmatch(k[4:], pattern)}


# Global configuration variables

ASCII_SUB = '\x1a'
DEFAULT_HASH_ALGO = hashlib.sha1
TRACE_LOG = get_config('TRACE_LOG', '0') == '1'

# Object Helpers

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

def coalesce(*arg):
    for el in arg:
        if el is not None:
            return el
    return None


# ID Helpers

def newid():
    return str(uuid.uuid4())

def newrunid():
    return f"{utcnow().strftime('%y%m%d%H%M%S%f')}{''.join([random.choice('ABCDEFGHJKLMNPQRSTUVWXYZ') for i in range(4)])}"


# Collection Helpers

def empty(obj):
    return obj is None or len(obj) == 0

def blank(obj):
    return obj is None or str(obj).strip() == ''

def allblank(obj):
    return all(map(blank, obj))


# Formatting helpers

def to_sql(obj):
    if obj is None:
        return 'NULL'
    if isinstance(obj, str):
        return "'{}'".format(obj.replace("'", "''"))
    if isinstance(obj, bool):
        return '1' if obj else '0'
    # datetime.datetime inherits from datetime.date and will be caught
    if isinstance(obj, (datetime.date, datetime.time)):
        return "'{}'".format(obj.isoformat())
    if isinstance(obj, numbers.Real):
        return str(obj)
    assert False, 'We should not be here.'

def to_csv(obj, delim='\t', delim_sub: str = None,
           float_decimals: int = 10, bool_true_value: str = None, bool_false_value: str = None):
    s = ''
    delim_sub = coalesce(delim_sub, ASCII_SUB)
    bool_true_value = coalesce(bool_true_value, '1')
    bool_false_value = coalesce(bool_false_value, '0')
    if obj is not None:
        # datetime.datetime inherits from datetime.date and will be caught
        if isinstance(obj, (datetime.date, datetime.time)):
            return obj.isoformat()
        elif isinstance(obj, numbers.Real):
            s = str(round(obj, float_decimals))
        elif isinstance(obj, bool):
            s = bool_true_value if obj else bool_false_value
        else:
            s = str(obj)
    assert delim_sub not in s, 'Cannot safely serialize data that contains ASCII_SUB character'
    return s.replace(delim, delim_sub)

def to_namedtuple(dictionary: dict):
    return collections.namedtuple('Record', dictionary.keys())(**dictionary)

def make_iterable(obj):
    if isinstance(obj, str) or not isinstance(obj, collections.abc.Iterable):
        return [obj]
    return obj


# File Helpers

if os.name != 'nt':
    import pwd
    import grp

def touch(fname, mode=0o666, dir_fd=None, **kwargs):
    flags = os.O_CREAT | os.O_APPEND
    with os.fdopen(os.open(fname, flags=flags, mode=mode, dir_fd=dir_fd)) as f:
        os.utime(f.fileno() if os.utime in os.supports_fd else fname,
                 dir_fd=None if os.supports_fd else dir_fd, **kwargs)

def chownmod(path, owner=None, group=None, perms=None):
    assert os.name != 'nt', "chownmod() is not available in Windows, sadly."
    if owner is not None or group is not None:
        uid = pwd.getpwnam(owner).pw_uid if owner is not None else -1
        gid = grp.getgrnam(group).gr_gid if group is not None else -1
        os.chown(path, uid, gid)
    if perms is not None:
        os.chmod(path, perms)

def getfiles(path):
    for root, dirs, files in os.walk(path):
        for fn in files:
            yield os.path.join(root, fn)

def iterfiles(path):
    for fn in os.listdir(path):
        fullpath = os.path.join(path, fn)
        if os.path.isdir(fullpath):
            continue
        else:
            yield fullpath

def iterdirs(path):
    for fn in os.listdir(path):
        fullpath = os.path.join(path, fn)
        if not os.path.isdir(fullpath):
            continue
        else:
            yield fullpath

def hashfile(path, hash_algo=None):
    h = coalesce(hash_algo, DEFAULT_HASH_ALGO())
    with open(path, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()


# String Helpers

def mass_replace(s, replace_vars):
    if s is None:
        return s
    if not isinstance(replace_vars, dict):
        raise Exception('replace_vars must be a dict.')
    for v in replace_vars.keys():
        s = s.replace(v, replace_vars[v])
    return s

def string_to_dict(records_string: str,
                   record_delim: str = ',',
                   pair_delim: str = '=',
                   key_processing_function: typing.Callable = None) -> dict:
    return {coalesce(key_processing_function, identity)(kvp[0]): kvp[1]
            for kvp in (kvp.split(pair_delim)
                        for kvp in records_string.split(record_delim))}

def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]

def hashstr(s, hash_algo=None):
    h = coalesce(hash_algo, DEFAULT_HASH_ALGO())
    if isinstance(s, bytes):
        h.update(s)
    else:
        h.update(s.encode('utf-8'))
    return h.hexdigest()

def camel_case_split(identifier):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    return [m.group(0) for m in matches]

def quote(s, quote):
    assert quote not in s, f"String '{s}' already contains quote ({quote}), escaping is needed."
    return f"{quote}{s}{quote}"

def strif(cond, s):
    return s if cond else ''

# Date/Time Helpers

def today(format: str = None) -> str:
    """Return today's date as an ISO formatted string or with the provided format."""
    if format is None:
        return datetime.datetime.today().date().isoformat()
    return datetime.datetime.today().date().strftime(format)

def now(format: str = None, timezone: str = None) -> str:
    dt = None
    if timezone is None:
        dt = datetime.datetime.now()
    else:
        dt = datetime.datetime.now(zoneinfo.ZoneInfo(timezone))
    if format is None:
        return dt.isoformat()
    return dt.strftime(format)

def utcnow():
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)

def timezone(tz_name):
    return zoneinfo.ZoneInfo(tz_name)

def is_datetime_naive(dt):
    return dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None

def is_datetime_utc(dt):
    return not is_datetime_naive(dt) and \
        (dt.tzinfo == datetime.timezone.utc or
         dt.tzinfo.utcoffset(dt).total_seconds() == 0)

def parse_iso_date(dt):
    d = [int(date_part) for date_part in dt.split('-')]
    return datetime.date(d[0], d[1], d[2])

def parse_iso_datetime_utc(dt):
    assert dt[-1] == 'Z', 'UTC date/time with Z ending expected'
    assert dt[4] == '-' and dt[7] == '-' and dt[10] == 'T' and dt[13] == ':' and dt[16] == ':' and dt[19] == '.', 'Unexpected ISO date/time format'
    return datetime.datetime(int(dt[0:4]), int(dt[5:7]), int(dt[8:10]), int(dt[11:13]), int(dt[14:16]), int(dt[17:19]), int(dt[20:26]))


# System Helpers

def has_module(module_name):
    return module_name in sys.modules

def get_exc_info():
    return '\n'.join(traceback.format_exception(*sys.exc_info()))


# JSON Helpers

class FriendlyJsonEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            if isinstance(o, decimal.Decimal):
                return format(o, 'f')
            elif isinstance(o, (datetime.date, datetime.time)):
                return o.isoformat()
            elif isinstance(o, bytes):
                try:
                    return o.decode('utf-8')
                except UnicodeError:
                    return f'<Binary ({len(o)} bytes)>'
            elif isinstance(o, set):
                return tuple(o)
            return super(FriendlyJsonEncoder, self).default(o)
        except Exception as ex:
            return f'<Unencodable type {builtins.type(o)} ({type(ex)})>'

def to_json(obj, **kwargs):
    return json.dumps(obj, cls=FriendlyJsonEncoder, **kwargs)

def pretty_json(js):
    return json.dumps(js, indent=4)


# Logging Helpers

LOG_CONTEXT = {'host': socket.gethostname()}
class JsonFormatter(logging.Formatter):
    def formatException(self, exc_info):
        result = super().formatException(exc_info)
        return repr(result)

    def format(self, record):
        super().format(record)
        js = {}
        for k, v in record.__dict__.items():
            if k not in 'msg args levelno filename exc_info created msecs relativeCreated thread threadName processName process':
                if v:
                    js[k] = v
            js['created'] = datetime.datetime.fromtimestamp(record.created)
            js.update(LOG_CONTEXT)
        return json.dumps(js, cls=FriendlyJsonEncoder)

def configure_logging():
    handler = logging.StreamHandler()
    formatter = JsonFormatter(logging.BASIC_FORMAT)
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(os.environ.get('PMG_LOGLEVEL', 'INFO'))
    root.addHandler(handler)

def logwrap(logger):
    def innerlogwrap(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            correlation_id = newid()
            start_time = time.process_time()
            LOG_CONTEXT['correlation_id'] = correlation_id
            if TRACE_LOG:
                logger.debug(f'> Begin function {func.__name__}()', extra={'function': {'name': func.__name__, 'args': args, **kwargs}})
            try:
                res = func(*args, **kwargs)
            except Exception as e:
                logger.exception(f'Exception in function {func.__name__}()', extra={'function': {'name': func.__name__, 'args': args, **kwargs}}, exc_info=e)
                raise
            if TRACE_LOG:
                logger.debug(f'> End function {func.__name__}() after {time.process_time() - start_time:,.3f} seconds')
            return res
        return wrapper
    return innerlogwrap

def is_weekend(dt):
    return dt.weekday() in [5, 6]

def identity(s):
    assert s == s, 'Invalid value for identity function'
    return s

def skip(iterable, entries_to_skip):
    return itertools.islice(iterable, entries_to_skip, None)

class UserError(Exception):
    pass
