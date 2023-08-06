# -----------------------------
# -- kongodb --
# lib module
# -----------------------------

import re
import uuid
import ulid
import json
import arrow
import datetime
from typing import Any
from ctypes import Union
from functools import reduce
from jinja2 import Template

# == JSON


def _json_serialize(o):
    return timestamp_to_str(o)

def _json_deserialize(json_dict):
    for k, v in json_dict.items():
        if isinstance(v, str) and timestamp_valid(v):
            json_dict[k] = arrow.get(v)
    return json_dict

def json_dumps(data: dict) -> str:
    """
    Convert data:dict to json string

    Args:
        data: dict

    Returns:
        str

    """
    return json.dumps(data, default=_json_serialize)


def json_loads(data: str) -> dict:
    """
    Convert data:str to json string

    Args:
        data: str

    Returns:
        dict

    """
    if not data:
        return None
    if isinstance(data, list):
        return [json.loads(v) if v else None for v in data]
    return json.loads(data, object_hook=_json_deserialize)


def get_timestamp() -> arrow.Arrow:
    """
    Generates the current UTC timestamp

    Returns:
      Arrow
    """
    return arrow.utcnow()


def timestamp_to_str(dt) -> str:
    if isinstance(dt, arrow.Arrow):
        return dt.for_json()
    elif isinstance(dt, (datetime.date, datetime.datetime)):
        return dt.isoformat()
    return dt


def timestamp_valid(dt_str) -> bool:
    try:
        datetime.datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
    except:
        return False
    return True


def gen_id() -> str:
    """
    Generates ULID
    26 chars

    Returns:
      string
    """
    return str(ulid.new()).lower()


def chunk_list (lst:list, n:int):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def dict_set(obj: dict, path: str, value: Any):
    """
    *Mutate #obj

    Update a dict via dotnotation

    Args:
        obj:dict - This object will be mutated
        path:str - the dot notation path to update
        value:Any - value to update with

    Returns:
        None
    """
    here = obj
    keys = path.split(".")
    for key in keys[:-1]:
        here = here.setdefault(key, {})
    here[keys[-1]] = value


def dict_get(obj: dict, path: str, default: Any = None) -> dict:
    """
    Get a value from a dict via dot notation

    Args:
        obj: Dict
        path: String - dot notation path
            object-path: key.value.path
            object-with-array-index: key.0.path.value
    Returns:
        mixed
    """
    def _getattr(obj, path):
        try:
            if isinstance(obj, list) and path.isdigit():
                return obj[int(path)]
            return obj.get(path, default)
        except:
            return default
    return reduce(_getattr, [obj] + path.split('.'))


def dict_pop(obj: dict, path: str) -> Any:
    """
    * Mutates #obj

    To pop a property from a dict dotnotation

    Args:
        obj:dict - This object will be mutated
        path:str - the dot notation path to update
        value:Any - value to update with

    Returns:
        Any - The value that was removed
    """

    here = obj
    keys = path.split(".")

    for key in keys[:-1]:
        here = here.setdefault(key, {})
    if isinstance(here, dict):
        return here.pop(keys[-1])
    else:
        val = here[keys[-1]]
        del here[keys[-1]]
        return val


def dict_merge(*dicts) -> dict:
    """         
    Deeply merge an arbitrary number of dicts                                                                    
    Args:
        *dicts
    Return:
        dict

    Example
        dict_merge(dict1, dict2, dict3, dictN)
    """
    updated = {}
    # grab all keys
    keys = set()
    for d in dicts:
        keys = keys.union(set(d))

    for key in keys:
        values = [d[key] for d in dicts if key in d]
        maps = [value for value in values if isinstance(value, dict)]
        if maps:
            updated[key] = dict_merge(*maps)
        else:
            updated[key] = values[-1]
    return updated


def flatten_dict(_dict: dict, _str: str = '', reducer=None) -> dict:
    """
    To flatten a dict. Nested node will be separated by dot or separator
    It takes in consideration dict in list and flat them.
    Non dict stay as is

    Args:
        ddict:
        prefix:
    Returns:
        dict

    """
    sep = "."
    ret_dict = {}
    for k, v in _dict.items():
        if isinstance(v, dict):
            ret_dict.update(flatten_dict(v, _str=sep.join([_str, k]).strip(sep)))
        elif isinstance(v, list):
            _k =  ("%s.%s" % (_str, k)).strip(sep)
            ret_dict[_k] = [flatten_dict(item) if isinstance(item, dict) else item for item in v]
        else:
            ret_dict[sep.join([_str, k]).strip(sep)] = v
    return ret_dict


def unflatten_dict(flatten_dict: dict) -> dict:
    """
    To un-flatten a flatten dict

    Args:
      flatten_dict: A flatten dict
    Returns:
      an unflatten dictionnary
    """
    output = {}
    for k, v in flatten_dict.items():
        path = k.split(".")
        if isinstance(v, list):
            v = [unflatten_dict(i2) if isinstance(i2, dict) else i2 for i2 in v]
        _set_nested(output, path, v)
    return output


def _get_nested_default(d, path):
    return reduce(lambda d, k: d.setdefault(k, {}), path, d)


def _set_nested(d, path, value):
    _get_nested_default(d, path[:-1])[path[-1]] = value


def render_template(source: str, data={}, is_data_flatten=False) -> str:
    """
    Render Template string with interpolation
    """
    _data = data.copy()
    if _data and is_data_flatten:
        _data = unflatten_dict(_data)
    return Template(source).render(**_data)
