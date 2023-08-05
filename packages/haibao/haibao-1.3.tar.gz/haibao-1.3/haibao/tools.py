# -*- encoding: utf-8 -*-
import time
import json

import signal
import requests


__author__ = u'seal'


def getAddressByIp(ip):
    """
    通过ip地址获取归属地以及其他详细信息
    """
    if not isinstance(ip, str) and not isinstance(ip, unicode):
        raise ValueError('ipaddress must be str')
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?query={}&resource_id=6006'.format(ip)
    try:
        html = requests.get(url=url, headers=headers).text
        data = json.loads(html)
    except Exception as e:
        return 'time error'
    return data


def getSampleAddressByIp(ip):
    """
    通过ip地址获取归属地
    """
    data = getAddressByIp(ip)
    if isinstance(data, dict):
        try:
            data = data['data'][0]['location']
        except:
            return 'time error'
    return data


class FunctionTimeOut(Exception):
    pass


def timeout_handler(signum, frame):
    raise FunctionTimeOut


def func_set_timeout(timeout):
    def wraper(func):
        def wrap(*args, **kwargs):
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(timeout)
            try:
                return func(*args, **kwargs)
            except FunctionTimeOut:
                return None
        return wrap
    return wraper


if __name__ == '__main__':
    pass
