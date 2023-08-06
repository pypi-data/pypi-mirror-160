"""time and date"""
import time


def get_time_str(time_float: float = None) -> str:
    """获取当前时间字符串

    Args:
        time_float (float, optional): time.time(). Defaults to None.

    Returns:
        str: 日期时间, 格式: 2021.05.17 12:20:20
    """

    if time_float is None:
        time_float = time.time()
    time_local = time.localtime(time_float)
    return time.strftime("%Y.%m.%d %H:%M:%S", time_local)


def get_date_str(time_float: float = None) -> str:
    """获取日期

    Args:
        time_float (float, optional): time.time(). Defaults to None.

    Returns:
        str: 格式: 2021.05.17
    """
    return get_time_str(time_float).split(" ")[0]


def get_time_folder() -> str:
    """获取以时间命名的文件夹名称

    Returns:
        str: 格式: 20210517_122020
    """

    return time.strftime("%Y%m%d_%H%M%S", time.localtime(time.time()))
