"""获取电脑系统信息"""
import platform
import re

import psutil
import torch

__all__ = ["get_cpu_info", "get_gpu_info", "get_package_info", "get_memory_info"]


def get_cpu_info() -> dict:
    """cpu info

    Returns:
        dict: keys: ["system", "cpu_name", "cpu_count", "cpu_threads", "cpu_core"]
    """
    return {
        "system": platform.version(),
        "cpu_name": get_cpu_name(),
        "cpu_count": get_cpu_count(),
        "cpu_threads": get_cpu_threads(),
        "cpu_core": get_cpu_core(),
    }


def get_gpu_info():
    """gpu info

    Returns:
        dict: keys: ["gpu_name", "gpu_num"]
    """
    return {
        "gpu_name": torch.cuda.get_device_name(0),
        "gpu_num": torch.cuda.device_count(),
    }


def get_memory_info():
    """GB"""
    pc_mem = psutil.virtual_memory()
    gb_factor = 1024.0 ** 3
    return {
        "total": float(pc_mem.total / gb_factor),
        "available": float(pc_mem.available / gb_factor),
        "used": float(pc_mem.used / gb_factor),
    }


def get_package_info():
    """package info

    Returns:
        dict: keys: ["python", "pytorch", "cuda", "cudnn"]
    """
    return {
        "python": platform.python_version(),
        "pytorch": torch.__version__,
        "cuda": torch.version.cuda,
        "cudnn": torch.backends.cudnn.version(),
    }


def get_cpu_name() -> str:
    """cpu name

    Returns:
        str: _description_
    """
    cpuinfo = read_file("/proc/cpuinfo")
    rep = "model\s+name\s+:\s+(.+)"
    tmp = re.search(rep, cpuinfo, re.I)
    cpu_name = tmp.groups()[0]
    return cpu_name


def get_cpu_count() -> int:
    return len(set(re.findall("physical id.+", read_file("/proc/cpuinfo"))))


def get_cpu_threads() -> int:
    return psutil.cpu_count()


def get_cpu_core() -> int:
    return psutil.cpu_count(logical=False)


def read_file(filename) -> str:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except:
        pass

    return ""
