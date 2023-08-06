"""md5sum

"""
import hashlib
import os.path as osp
from typing import List, Tuple

from ..io.io import find_all_file
from .tasks import multi_tasks


def md5sum(filename: str) -> str:
    """计算文件的md5值

    copy from https://www.aiuai.cn/aifarm1114.html
    """
    f = open(filename, "rb")
    md5 = hashlib.md5()
    while True:
        fb = f.read(8096)
        if not fb:
            break
        md5.update(fb)
    f.close()
    return md5.hexdigest()


def md5sum_folder(folder: str) -> List[Tuple[str, str]]:
    """计算文件夹的md5值(支持多级目录)

    Args:
        folder (str): 文件夹

    Returns:
        List[Tuple[str, str]]: [[md5, filename],...]
    """
    md5_list = []
    filename_list = list(find_all_file(folder))
    md5_list = multi_tasks(md5sum, filename_list, pbar_name="md5sum", workers=12)
    return zip(md5_list, filename_list)


def save_md5sum(path: str, md5_filename: str = "md5.txt", cut_folder: str = "") -> None:
    """保存MD5到文件

    Args:
        path (str): file or folder
        md5_filename (str): md5.txt
        cut_folder (str): 去除路径头部
    """
    if osp.isfile(path):
        md5_filename_list = [[md5sum(path), path]]
    elif osp.isdir(path):
        md5_filename_list = md5sum_folder(path)
    else:
        assert False, "path is bad"

    if not cut_folder.endswith("/"):
        cut_folder = cut_folder + "/"
    with open(md5_filename, "w", encoding="utf-8") as fw:
        for md5, filename in md5_filename_list:
            if cut_folder and filename.startswith(cut_folder):
                filename = filename[len(cut_folder) :]
            fw.write(f"{md5} {filename}\n")


def check_md5sum(path: str, md5_filename: str = "md5.txt") -> None:
    """检查MD5

    Args:
        path (str): folder
        md5_filename (str): md5.txt
    """
    md5_list = []
    with open(md5_filename, "r") as fr:
        for line in fr.readlines():
            md5, filename = line.replace("  ", " ").strip().split(" ")
            md5_list.append([md5, filename])

    def check(md5, filename):
        if md5sum(osp.join(path, filename)) != md5:
            print("MD5 bad:", filename)

    multi_tasks(check, md5_list, pbar_name="check md5")
