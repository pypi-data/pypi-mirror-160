import os
import os.path as osp

import numpy as np
import torch
import torch.nn as nn
from smplx import SMPL as _SMPL
from smplx.lbs import vertices2joints

from .kp_map import JOINT_MAP, JOINT_NAMES, OPENPOSE_JOINT_NAMES, SMPL_JOINT_NAMES

J_regressor_extra_fname = osp.join(osp.dirname(__file__), "J_regressor_extra.npy")
J_regressor_h36m_correct_fname = osp.join(osp.dirname(__file__), "J_regressor_h36m_correct.npy")
J_regressor_coco_fname = osp.join(osp.dirname(__file__), "J_regressor_coco.npy")  # copy from Pose2Mesh


class SMPLBase(_SMPL):
    def __init__(self, model_path: str, gender: str = "neutral"):
        super().__init__(
            model_path=model_path,
            gender=gender,
            create_betas=False,
            create_body_pose=False,
            create_global_orient=False,
            create_transl=False,
            use_hands=True,
            use_feet_keypoints=True,
        )

def get_gender(gender: str):
    d = {
        "f": "female",
        "female": "female",
        "m": "male",
        "male": "male",
        "n": "neutral",
        "neutral": "neutral",
    }
    gender = gender.lower()
    if gender in d:
        return d[gender]
    assert 0, f"no gender: {gender}"
    return None

class SMPL(nn.Module):
    r"""Extension of the official SMPL implementation to support more joints

    Args:
        model_path:
            SMPL_FEMALE.pkl
            SMPL_MALE.pkl
            SMPL_NEUTRAL.pkl
        gender: str: neutral, male, female
        joint_type: str: J49(OpenPose+SMPL), SMPL(24), OpenPose(25)
    """

    def __init__(self, model_path: str, gender: str = "neutral", joint_type="J49"):
        super().__init__()
        self.smpl_dict = {
            "female": SMPLBase(model_path, gender="female"),
            "male": SMPLBase(model_path, gender="male"),
            "neutral": SMPLBase(model_path, gender="neutral"),
        }
        self.gender = gender
        self.faces = self.smpl_dict["neutral"].faces

        joint_type = joint_type.lower()
        d = {
            "j49": JOINT_NAMES,
            "openpose": OPENPOSE_JOINT_NAMES,
            "smpl": SMPL_JOINT_NAMES,
        }
        if joint_type not in d:
            assert 0, f"no joint type:{joint_type}"

        self.joint_name = d[joint_type]

        joints = [JOINT_MAP[i] for i in self.joint_name]
        self.joint_map = torch.tensor(joints, dtype=torch.long)

        J_regressor_extra = np.load(J_regressor_extra_fname)
        assert J_regressor_extra.shape == (9, 6890)
        self.register_buffer("J_regressor_extra", torch.tensor(J_regressor_extra, dtype=torch.float32))
        self.register_buffer(
            "J_regressor_h36m_correct", torch.tensor(np.load(J_regressor_h36m_correct_fname), dtype=torch.float32)
        )
        self.register_buffer("J_regressor_coco", torch.tensor(np.load(J_regressor_coco_fname), dtype=torch.float32))

    def kps_num(self) -> int:
        return len(self.joint_name)

    def forward(self, betas, pose, gender: str = None):
        r"""
        Args:
            betas: shape: N,10
            pose: shape N,72  or N,24,3 or N,24,3,3

        Return:
            vertices: shape: N,6890,3
            joints: shape: N,49,3
        """
        bs = betas.shape[0]
        if pose.shape == (bs, 72):
            pose = pose.reshape([bs, 24, 3])

        gender = get_gender(gender) or self.gender
        smpl_output = self.smpl_dict[gender].forward(
            betas=betas,
            body_pose=pose[:, 1:],
            global_orient=pose[:, :1],
            pose2rot=len(pose.shape) == 3,
        )
        joints = smpl_output.joints
        vertices = smpl_output.vertices
        extra_joints = vertices2joints(self.J_regressor_extra, vertices)
        joints = torch.cat([joints, extra_joints], dim=1)
        joints = joints[:, self.joint_map, :]
        return vertices, joints

    def get_h36m_joints(self, vertices):
        """
        This method is used to get the joint locations from the SMPL mesh
        Input:
            vertices: size = (B, 6890, 3)
        Output:
            3D joints: size = (B, 17, 3)
        """
        joints = torch.einsum("bik,ji->bjk", [vertices, self.J_regressor_h36m_correct])
        return joints

    def get_coco_joints(self, vertices):
        """
        Return:
            3D joints: size = (B, 17, 3)
        """
        joints = torch.einsum("bik,ji->bjk", [vertices, self.J_regressor_coco])
        return joints

    def tpose(self, gender: str = None):
        r"""TPose

        Return:
            vertices: 6890,3
            joints: 49,3

        Example::
            >>> from human_cver.models.smpl.smpl import SMPL
            >>> from human_cver.io.obj_file import save_obj
            >>> smpl = SMPL(model_path="data")
            >>> vertices, joints = smpl.tpose()
            >>> h36m = smpl.get_h36m_joints(vertices[None])[0]
            >>> save_obj("tpose.obj", vertices, smpl.faces)
            >>> save_obj("joints.obj", joints)
            >>> save_obj("h36m.obj", h36m)
        """
        gender = get_gender(gender) or self.gender
        smpl_output = self.smpl_dict[gender].forward(
            betas=torch.zeros([1, 10]),
            body_pose=torch.zeros([1, 23, 3]),
            global_orient=torch.zeros([1, 1, 3]),
            pose2rot=True,
        )
        joints = smpl_output.joints
        vertices = smpl_output.vertices
        extra_joints = vertices2joints(self.J_regressor_extra, vertices)
        joints = torch.cat([joints, extra_joints], dim=1)
        joints = joints[:, self.joint_map, :]
        return vertices[0], joints[0]
