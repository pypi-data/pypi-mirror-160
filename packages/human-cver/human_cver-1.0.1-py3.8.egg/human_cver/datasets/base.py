"""base dataset"""
import os.path as osp
from typing import List

import cv2
from torch.utils.data import Dataset


class BaseDataset(Dataset):
    """数据集模板类"""

    def info(self) -> dict:
        """数据集相关信息"""
        raise NotImplementedError

    def keys(self) -> List[str]:
        """数据集包含的内容"""
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def __getitem__(self, index: int) -> dict:
        raise NotImplementedError
