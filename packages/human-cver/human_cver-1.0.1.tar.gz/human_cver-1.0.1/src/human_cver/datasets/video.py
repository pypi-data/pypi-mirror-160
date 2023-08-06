import os.path as osp
from typing import Dict, List

import cv2
import numpy as np

from ..tools.logger import Logger
from .base import BaseDataset


class VideoDataset(BaseDataset):
    """视频数据集"""

    def __init__(self, video_filename: str) -> None:
        super().__init__()
        self.video_filename = video_filename
        if not osp.exists(video_filename):
            Logger.error(f"not exists: {video_filename}")
            return

        self.cap = cv2.VideoCapture(video_filename)
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self._curr_frame = -1

    def info(self):
        return {
            "frame_width": self.frame_width,
            "frame_height": self.frame_height,
            "frame_count": self.frame_count,
            "fps": self.fps,
            "fname": self.video_filename,
        }

    def keys(self) -> List[str]:
        return ["img"]

    def __len__(self):
        return self.frame_count

    def __getitem__(self, index) -> Dict[str, np.ndarray]:
        if not (0 <= index < len(self)):
            Logger.error(f"bad index: {index}")
            return
        if self._curr_frame + 1 != index:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, index)
        opened, frame = self.cap.read()
        self._curr_frame = index
        if not opened:
            Logger.error(f"can not open: {self.video_filename}")
            return

        return {
            "img": frame,
        }

    def close(self):
        self.cap.close()
