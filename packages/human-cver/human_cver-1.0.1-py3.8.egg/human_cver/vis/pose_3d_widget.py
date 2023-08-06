import sys
from PySide6.QtWidgets import QMainWindow, QApplication
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np


def axisEqual3D(ax):
    extents = np.array([getattr(ax, "get_{}lim".format(dim))() for dim in "xyz"])
    sz = extents[:, 1] - extents[:, 0]
    centers = np.mean(extents, axis=1)
    maxsize = max(abs(sz))
    r = maxsize / 2
    for ctr, dim in zip(centers, "xyz"):
        getattr(ax, "set_{}lim".format(dim))(ctr - r, ctr + r)


class Figure3D(object):
    def __init__(self, title:str="3D") -> None:
        self.fig = plt.figure(figsize=(10, 10))
        self.ax = self.fig.add_subplot(111, projection="3d")
        self.ax.set_box_aspect([1, 1, 1])
        # self.render(np.zeros([10, 3]))

        self.ax.set_xlabel("X axis")
        self.ax.set_ylabel("Y axis")
        self.ax.set_zlabel("Z axis")
        self.ax.set_title(title)
        # self.ax.legend()
        axisEqual3D(self.ax)

    def render(self, kps_3d, kps_line=None):
        # 绘制骨架
        self.ax.clear()
        kps_line = kps_line or []
        for a, b in kps_line:
            x = np.array([kps_3d[a, 0], kps_3d[b, 0]])
            y = np.array([kps_3d[a, 1], kps_3d[b, 1]])
            z = np.array([kps_3d[a, 2], kps_3d[b, 2]])
            self.ax.plot(x, z, -y, c="r", linewidth=1)

        for i in range(kps_3d.shape[0]):
            x = kps_3d[i, 0]
            y = kps_3d[i, 1]
            z = kps_3d[i, 2]
            self.ax.scatter(x, y, z, c="g", marker='o')


    def show(self):
        self.fig.show()
def vis_3d_pose(kps_3d, kps_line, title: str = "3D Pose"):
    fig = Figure3D(title)
    fig.render(kps_3d, kps_line)
    fig.show()


class Pose3DWidget(FigureCanvasQTAgg):
    def __init__(self, kps_line=None):

        self.figure3d = Figure3D()
        self.kps_line = kps_line
        # fig, ax = vis_3d_pose([], [], show=False)
        # self.ax = ax
        super().__init__(self.figure3d.fig)

    def render(self, pose_3d, kps_line=None):
        kps_line = kps_line or self.kps_line
        self.figure3d.render(pose_3d, kps_line)


# class MainWindow(QMainWindow):
#     def __init__(self, *args, **kwargs):
#         super(MainWindow, self).__init__(*args, **kwargs)

#         # Create the maptlotlib FigureCanvas object,
#         # which defines a single set of axes as self.axes.
#         w = Pose3DWidget(np.array([[1, 2, 3], [2, 3, 4], [1, 3, 4], [2, 2, 2]]), [[0, 1], [1, 2], [0, 2], [1, 3]])
#         self.setCentralWidget(w)

#         self.show()


# app = QApplication(sys.argv)
# w = MainWindow()
# app.exec_()
