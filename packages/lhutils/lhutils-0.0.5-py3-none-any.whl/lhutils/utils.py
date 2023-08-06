# -*- coding: utf8 -*-
import os
import math
import requests

from tenacity import *

from typing import Dict, List, Tuple
from typing import Optional, Union, Any


def sec2time(seconds: int):
    """
    秒转时间

    :param seconds: 秒
    :return

    >>> sec2time(60)
        00:01:00
    >>> sec2time(60*60)
        01:00:00
    >>> sec2time(60*60*24)
        1 days, 00:00:00
    """

    seconds = 0 if seconds < 0 else math.ceil(seconds)

    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)

    if d == 0:
        return '%02d:%02d:%02d' % (h, m, s)

    return '%d days, %02d:%02d:%02d' % (d, h, m, s)


def hms2sec(hms: str):
    """
    %H:%M:%S转秒

    :param hms: 格式: 00:00:00
    :return sec
    """
    h, m, s = [int(i) for i in hms.split(':')]
    return 3600 * h + 60 * m + s


@retry(
    reraise=True,
    wait=wait_fixed(1),
    stop=stop_after_attempt(3),
)
def download_file(
        url: str,
        file: str,
        cache=True,
        unbroken=True,
        ** kwargs
):
    """
    下载文件并保存

    :param url: 网络文件地址
    :param file: 本地文件地址
    :param cache: 把本地文件作为缓存条件，检查缓存是否存在，如果存在就不会下载网络文件
    :param unbroken: 检查下载的文件的完整性，防止因为网络问题导致文件下载完整。
    :param **kwargs: requests(..., **kwargs)
    """

    # 判断缓存
    if cache and os.path.exists(file):
        return None

    # 读取网络文件
    # 设置一个默认的超时时间
    timeout = kwargs.pop('timeout', 120)
    response = requests.get(url, timeout=timeout, **kwargs)

    if response.status_code != 200:
        raise ValueError(
            response.status_code,
            response.text,
            response.url
        )

    # 验证文件完整性
    if unbroken:
        expected_length = response.headers.get('Content-Length')
        if expected_length is None:
            raise IOError('requests response header does not contain the "content-Length", so data integrity cannot be verified.')
        actual_length = response.raw.tell()
        expected_length = int(expected_length)
        if actual_length < expected_length:
            raise IOError('incomplete read ({} bytes read, {} more expected)'.format(actual_length, expected_length - actual_length))

    # 保存文件
    with open(file, 'wb') as fp:
        fp.write(response.content)
