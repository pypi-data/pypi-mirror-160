import sys

import cv2
import numpy as np
from PySide6 import QtCore, QtGui
from PySide6.QtGui import QScreen
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSlider,
                               QVBoxLayout, QWidget)
from torch.utils.data import Dataset

from ..datasets import ImageFolderDataset, VideoDataset
from .pose_3d_widget import Pose3DWidget

__all__ = ["show_dataset"]


class ImageWidget(QLabel):
    """显示图片"""

    def __init__(self, img: np.ndarray = None):
        super().__init__()
        if img is not None:
            self.set_img(img)

    def set_img(self, img: np.ndarray):
        height, width, channel = img.shape
        assert channel == 3
        qImg = QtGui.QImage(img.data, width, height, width * channel, QtGui.QImage.Format_BGR888)
        self.setPixmap(QtGui.QPixmap.fromImage(qImg))

    def set_imgname(self, imgname):
        self.set_img(cv2.imread(imgname))


class DatasetWidget(QWidget):
    def __init__(self, dataset: Dataset = None) -> None:
        super().__init__()

        class Slider(QSlider):
            def __init__(self, max_num: int = 100):
                super().__init__(QtGui.Qt.Horizontal)
                self.set_max(max_num)

            def set_max(self, max_num: int):
                self.setMinimum(0)
                self.setMaximum(max_num)
                self.setSingleStep(1)
                self.setTickInterval(max(1, int(max_num / 10.0)))
                self.setTickPosition(QSlider.TicksBelow)

        layout1 = QVBoxLayout()
        layout = QHBoxLayout()
        self.slider = Slider()
        self.w_img = ImageWidget()
        self.w_pose_3d = Pose3DWidget()
        layout1.addWidget(self.slider)
        layout1.addWidget(self.w_img)
        layout.addLayout(layout1, 3)
        layout.addWidget(self.w_pose_3d, 1)
        self.setLayout(layout)
        self.slider.valueChanged.connect(self.valuechange)

        if dataset is not None:
            self.set_dataset(dataset)
            self.set_index(0)

    def set_dataset(self, dataset):
        self.dataset = dataset
        self.slider.set_max(len(self.dataset) - 1)

    def valuechange(self):
        self.set_index(self.slider.value())

    def set_index(self, index):
        d = self.dataset.render(index)
        if isinstance(d, dict):
            self.w_img.set_img(d["img"])
            if "pose_3d" in d:
                self.w_pose_3d.render(d["pose_3d"])
        else:
            self.w_img.set_img(d)

    def get_img(self, index):
        """获取数据集需要显示的内容"""
        if hasattr(self.dataset, "render"):
            return self.dataset.render(index)
        else:
            return self.dataset[index]["img"]


class DatasetViewer(QWidget):
    """数据集可视化界面"""

    def __init__(self, dataset: Dataset):
        super().__init__()

        self.setMouseTracking(True)

        layout = QVBoxLayout()
        layout.addWidget(DatasetWidget(dataset))
        self.setLayout(layout)
        # 软件图标
        # self.setWindowIcon(QtGui.QIcon(BOX_ICON["scholar"]))
        self.setWindowTitle("DatasetViewer")
        self.showMaximized()
        self.show()


def center(window):
    center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
    geo = window.frameGeometry()
    geo.moveCenter(center)
    window.move(geo.topLeft())


def show_dataset(dataset):
    """数据集可视化界面"""
    app = QApplication()
    main_window = DatasetViewer(dataset)
    center(main_window)

    sys.exit(app.exec())


if __name__ == "__main__":
    show_dataset(VideoDataset("xxx.mp4"))
