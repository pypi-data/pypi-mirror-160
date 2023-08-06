"""downloader"""
from urllib.request import Request, urlopen

import requests

from .logger import Logger


def download_file(url: str, filename: str) -> bool:
    """download file by url

    Args:
        url (str): url
        filename (str): filename

    Returns:
        bool: 是否下载成功
    """
    try:
        content = requests.get(url).content
    except Exception as e:
        Logger.error(e)
        return False
    with open(filename, "wb") as fw:
        fw.write(content)
    return True


def download_web_text(url: str) -> str:
    """下载网页源码

    Args:
        url (str): url

    Returns:
        str: 网页源码
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0"}
        req = Request(url=url, headers=headers)
        content = urlopen(req).read().decode("utf-8")
        return content
    except Exception as e:
        print(e)
        return ""
