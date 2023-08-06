# lhutils

对常用代码进行封装，防止自己重复造轮子。

github: https://github.com/tasbox/lhutils.git



官方文档:

https://packaging.python.org/en/latest/tutorials/packaging-projects/



pypi:

https://pypi.org/

https://pypi.tuna.tsinghua.edu.cn/simple




## 

秒转时间

```python
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
```


下载文件并保存

```python
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
```