import requests
import json

from tsdl.common.util import to_dict

_timeout_ = 60
_method_ = 'get'


def get(url, params: dict = None):
    try:
        res = requests.get(url=url, params=params, timeout=_timeout_)
        try:
            return json.loads(res.text)
        except Exception as e:
            return res.text
    except Exception as e:
        raise e


def post(url, params: dict = None, jsons: dict = None):
    try:
        res = requests.post(url=url, params=params, json=jsons, timeout=_timeout_)
        try:
            return json.loads(res.text)
        except Exception as e:
            return res.text
    except Exception as e:
        raise e


def put(url, params: dict = None):
    try:
        res = requests.put(url=url, params=params, timeout=_timeout_)
        try:
            return json.loads(res.text)
        except Exception as e:
            return res.text
    except Exception as e:
        raise e


def delete(url, params: dict = None):
    try:
        res = requests.delete(url=url, params=params, timeout=_timeout_)
        try:
            return json.loads(res.text)
        except Exception as e:
            return res.text
    except Exception as e:
        raise e

