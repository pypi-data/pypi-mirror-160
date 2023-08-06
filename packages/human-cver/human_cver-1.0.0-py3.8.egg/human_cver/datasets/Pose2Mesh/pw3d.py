import copy
import json
import os
import os.path as osp

import cv2
import numpy as np
import torch
from human_cver.vis.plot_kps import plot_kps_2d
from pycocotools.coco import COCO

from ...geometric.coord import (cam2pixel, get_bbox, process_bbox)
from ...models.smpl.smpl import SMPL


class PW3D(torch.utils.data.Dataset):
    def __init__(self, dataset_path: str, pw3d_path, mode: str = "test", smpl: SMPL = None):
        self.mode = mode  #'validation'
        self.data_path = dataset_path
        self.img_path = osp.join(pw3d_path, "imageFiles")
        self.smpl = smpl
        # SMPL joint set
        # self.mesh_model = SMPL()
        # self.smpl_root_joint_idx = self.mesh_model.root_joint_idx
        # self.face_kps_vertex = self.mesh_model.face_kps_vertex
        self.smpl_vertex_num = 6890
        self.smpl_joint_num = 24
        self.smpl_flip_pairs = ((1, 2), (4, 5), (7, 8), (10, 11), (13, 14), (16, 17), (18, 19), (20, 21), (22, 23))
        self.smpl_skeleton = (
            (0, 1),
            (1, 4),
            (4, 7),
            (7, 10),
            (0, 2),
            (2, 5),
            (5, 8),
            (8, 11),
            (0, 3),
            (3, 6),
            (6, 9),
            (9, 14),
            (14, 17),
            (17, 19),
            (19, 21),
            (21, 23),
            (9, 13),
            (13, 16),
            (16, 18),
            (18, 20),
            (20, 22),
            (9, 12),
            (12, 15),
        )
        # self.joint_regressor_smpl = self.mesh_model.layer['neutral'].th_J_regressor

        # H36M joint set
        self.human36_root_joint_idx = 0
        self.human36_eval_joint = (1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 13, 14, 15, 16)
        self.human36_skeleton = (
            (0, 7),
            (7, 8),
            (8, 9),
            (9, 10),
            (8, 11),
            (11, 12),
            (12, 13),
            (8, 14),
            (14, 15),
            (15, 16),
            (0, 1),
            (1, 2),
            (2, 3),
            (0, 4),
            (4, 5),
            (5, 6),
        )
        # self.joint_regressor_human36 = torch.Tensor(self.mesh_model.joint_regressor_h36m)

        # COCO joint set
        self.coco_joint_num = 19  # 17 + 2, manually added pelvis and neck
        self.coco_joints_name = (
            "Nose",
            "L_Eye",
            "R_Eye",
            "L_Ear",
            "R_Ear",
            "L_Shoulder",
            "R_Shoulder",
            "L_Elbow",
            "R_Elbow",
            "L_Wrist",
            "R_Wrist",
            "L_Hip",
            "R_Hip",
            "L_Knee",
            "R_Knee",
            "L_Ankle",
            "R_Ankle",
            "Pelvis",
            "Neck",
        )
        self.coco_flip_pairs = ((1, 2), (3, 4), (5, 6), (7, 8), (9, 10), (11, 12), (13, 14), (15, 16))
        self.coco_skeleton = (
            (1, 2),
            (0, 1),
            (0, 2),
            (2, 4),
            (1, 3),
            (6, 8),
            (8, 10),
            (5, 7),
            (7, 9),
            (12, 14),
            (14, 16),
            (11, 13),
            (13, 15),  # (5, 6), (11, 12))
            (17, 11),
            (17, 12),
            (17, 18),
            (18, 5),
            (18, 6),
            (18, 0),
        )
        # self.joint_regressor_coco = torch.Tensor(self.mesh_model.joint_regressor_coco)
        self.openpose_joints_name = (
            "Nose",
            "Neck",
            "R_Shoulder",
            "R_Elbow",
            "R_Wrist",
            "L_Shoulder",
            "L_Elbow",
            "L_Wrist",
            "R_Hip",
            "R_Knee",
            "R_Ankle",
            "L_Hip",
            "L_Knee",
            "L_Ankle",
            "R_Eye",
            "L_Eye",
            "R_Ear",
            "L_Ear",
            "Pelvis",
        )

        input_joint_name = "coco"
        self.joint_num, self.skeleton, self.flip_pairs = self.get_joint_setting(input_joint_name)

        self.datalist, self.video_indices = self.load_data()  # self.video_indexes: 37 video, and indices of each video

        print("3dpw data len: ", len(self.datalist))

    def get_joint_setting(self, joint_category="human36"):
        joint_num = eval(f"self.{joint_category}_joint_num")
        skeleton = eval(f"self.{joint_category}_skeleton")
        flip_pairs = eval(f"self.{joint_category}_flip_pairs")

        return joint_num, skeleton, flip_pairs

    def get_smpl_coord(self, smpl_param):
        pose, shape, trans, gender = smpl_param["pose"], smpl_param["shape"], smpl_param["trans"], smpl_param["gender"]
        smpl_pose = torch.FloatTensor(pose).view(-1, 3)
        smpl_shape = torch.FloatTensor(shape).view(1, -1)
        # translation vector from smpl coordinate to 3dpw world coordinate
        smpl_trans = torch.FloatTensor(trans).view(-1, 3)

        smpl_pose = smpl_pose.view(1, -1)
        # get mesh and joint coordinates
        smpl_mesh_coord, smpl_joint_coord = self.smpl(pose=smpl_pose, betas=smpl_shape, gender=gender)  # , smpl_trans)

        # incorporate face keypoints
        smpl_mesh_coord = smpl_mesh_coord.numpy().astype(np.float32).reshape(-1, 3)
        smpl_joint_coord = smpl_joint_coord.numpy().astype(np.float32).reshape(-1, 3)

        smpl_mesh_coord += smpl_trans.numpy()
        smpl_joint_coord += smpl_trans.numpy()
        # meter -> milimeter
        smpl_mesh_coord *= 1000
        smpl_joint_coord *= 1000
        return smpl_mesh_coord, smpl_joint_coord

    def load_data(self):
        print("Load annotations of 3DPW ")
        db = COCO(osp.join(self.data_path, "3DPW_latest_" + self.mode + ".json"))

        # get detected 2d pose
        with open(osp.join(self.data_path, f"darkpose_3dpw_{self.mode}set_output.json")) as f:  #
            pose2d_outputs = {}
            data = json.load(f)
            for item in data:
                annot_id = str(item["annotation_id"])
                pose2d_outputs[annot_id] = {"coco_joints": np.array(item["keypoints"], dtype=np.float32)[:, :3]}

        datalist = []
        custompose_count = 0
        for aid in db.anns.keys():
            aid = int(aid)
            ann = db.anns[aid]
            image_id = ann["image_id"]

            img = db.loadImgs(image_id)[0]
            img_width, img_height = img["width"], img["height"]
            sequence_name = img["sequence"]
            img_name = img["file_name"]

            img_path = osp.join(self.img_path, sequence_name, img_name)
            cam_param = {k: np.array(v, dtype=np.float32) for k, v in img["cam_param"].items()}

            smpl_param = ann["smpl_param"]
            pid = ann["person_id"]
            vid_name = sequence_name + str(pid)
            bbox = process_bbox(np.array(ann["bbox"]))
            if bbox is None:
                continue
            
            # 18, 3
            openpose = np.array(ann["openpose_result"], dtype=np.float32).reshape(-1, 3)
            openpose = self.add_pelvis_and_neck(openpose, self.openpose_joints_name, only_pelvis=True)

            # 17, 3
            custompose = np.array(pose2d_outputs[str(aid)]["coco_joints"])
            custompose = self.add_pelvis_and_neck(custompose, self.coco_joints_name)
            custompose_count += 1

            datalist.append(
                {
                    "annot_id": aid,
                    "person_id": pid,
                    "image_id": image_id,
                    "img_path": img_path,
                    "vid_name": vid_name,
                    "img_shape": (img_height, img_width),
                    "cam_param": cam_param,
                    "bbox": bbox,
                    "smpl_param": smpl_param,
                    "pred_pose2d": custompose,
                }
            )

        datalist = sorted(datalist, key=lambda x: (x["person_id"], x["img_path"]))
        valid_names = np.array([data["vid_name"] for data in datalist])
        unique_names = np.unique(valid_names)
        video_indices = []
        for u_n in unique_names:
            indexes = valid_names == u_n
            video_indices.append(indexes)

        print("num custom pose: ", custompose_count)
        return datalist, video_indices

    def add_pelvis_and_neck(self, joint_coord, joints_name, only_pelvis=False):
        lhip_idx = joints_name.index("L_Hip")
        rhip_idx = joints_name.index("R_Hip")
        pelvis = (joint_coord[lhip_idx, :] + joint_coord[rhip_idx, :]) * 0.5
        pelvis = pelvis.reshape((1, -1))

        lshoulder_idx = joints_name.index("L_Shoulder")
        rshoulder_idx = joints_name.index("R_Shoulder")
        neck = (joint_coord[lshoulder_idx, :] + joint_coord[rshoulder_idx, :]) * 0.5
        neck = neck.reshape((1, -1))

        if only_pelvis:
            joint_coord = np.concatenate((joint_coord, pelvis))
        else:
            joint_coord = np.concatenate((joint_coord, pelvis, neck))
        return joint_coord

    def __len__(self):
        return len(self.datalist)

    def render(self, index):
        d = self.__getitem__(index)

        img_path = d["img_path"]
        img = cv2.imread(img_path)

        cam_param = d["cam_param"]
        smpl_param = d["smpl_param"]
        mesh_cam, joint_cam_smpl = self.get_smpl_coord(smpl_param)
        mesh_coord = cam2pixel(mesh_cam, f=cam_param["focal"], c=cam_param["princpt"])
        plot_kps_2d(img, mesh_coord)

        return {
            "img": img,
            "pose_3d": joint_cam_smpl
        }

    def __getitem__(self, idx):
        return copy.deepcopy(self.datalist[idx])

