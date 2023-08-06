from human_cver.datasets.Pose2Mesh.Human36M.dataset import Human36M
from human_cver.models.smpl.smpl import SMPL
from human_cver.vis.dataset_viewer import show_dataset

smpl = SMPL(model_path="/home/lwk/human_cver/data", joint_type="SMPL")
show_dataset(Human36M(smpl=smpl))
