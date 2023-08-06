import logging
import os
import os.path as osp
import platform

import logzero
from logzero import logger

# python3.8版本之后才支持 stacklevel
version = platform.python_version()
version = [int(a) for a in version.split(".")]
has_stacklevel = not (version[0] <= 3 and version[1] < 8)


class Logger:
    """日志"""

    _logfilename = None

    @staticmethod
    def debug(msg: str):
        """debug

        Args:
            msg (str): 需要打印的字符串
        """
        if has_stacklevel:
            logger.debug(msg, stacklevel=2)
        else:
            logger.debug(msg)

    @staticmethod
    def info(msg: str):
        """info

        Args:
            msg (str): 需要打印的字符串
        """
        if has_stacklevel:
            logger.info(msg, stacklevel=2)
        else:
            logger.info(msg)

    @staticmethod
    def warn(msg: str):
        """warn

        Args:
            msg (str): 需要打印的字符串
        """
        if has_stacklevel:
            logger.warning(msg, stacklevel=2)
        else:
            logger.warning(msg)

    @staticmethod
    def error(msg):
        """error

        Args:
            msg (str): 需要打印的字符串
        """
        if has_stacklevel:
            logger.error(msg, stacklevel=2)
        else:
            logger.error(msg)

    @staticmethod
    def logfile(filename: str, clear: bool = False):
        """设置日志文件名

        Args:
            filename (str): 日志文件名
            clear (bool, optional): 是否清除日志文件. Defaults to False.
        """
        path = osp.dirname(filename)
        if path and (not osp.exists(path)):
            os.makedirs(path, exist_ok=True)

        msg = f"logfile -> {filename}"
        if has_stacklevel:
            logger.warning(msg, stacklevel=2)
        else:
            logger.warning(msg)
        if clear and osp.exists(filename):
            os.remove(filename)
        logzero.logfile(filename)
        Logger._logfilename = filename

    @staticmethod
    def loglevel(level):
        """设置日志等级: debug, info, warn, error"""
        level = level.upper()
        logzero.loglevel(eval(f"logging.{level}"))

        msg = f"loglevel -> {level}"
        if has_stacklevel:
            logger.warning(msg, stacklevel=2)
        else:
            logger.warning(msg)

    @staticmethod
    def print(*text_list, end="\n"):
        """print

        Args:
            end (str, optional): 分隔符. Defaults to "\n".
        """
        if len(text_list) == 0:
            text = "\n"
            end = ""
        else:
            text = " ".join([str(t) for t in text_list])

        if Logger._logfilename is not None:
            with open(Logger._logfilename, "a") as fw:
                fw.write(text + end)
        else:
            print(text, end=end)


Logger.loglevel("debug")
