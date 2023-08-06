import glob
import os.path as osp
from typing import List

import cv2

from ..tools.logger import Logger
from .base import BaseDataset


class ImageFolderDataset(BaseDataset):
    """图片文件夹数据集"""

    def __init__(self, folder: str, fmts: List[str] = ["*.jpg", "*.jpeg", "*.png"]) -> None:
        super().__init__()

        if not osp.exists(folder):
            Logger.error(f"not exists: {folder}")
            return

        self.imgnames = []
        for fmt in fmts:
            self.imgnames.extend(glob.glob(osp.join(folder, fmt)))
        self.imgnames.sort()

    def info(self):
        return dict()

    def keys(self):
        return ["imgname", "img"]

    def __len__(self):
        return len(self.imgnames)

    def __getitem__(self, index):
        imgname = self.imgnames[index]
        img = cv2.imread(imgname)
        return {
            "imgname": imgname,
            "img": img,
        }
