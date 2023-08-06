import os
import os.path as osp
from collections import OrderedDict

import torch
import torch.nn as nn

from .config import get_log_dir, instantiate_from_config, load_config

__all__ = ["load_checkpoint", "get_best_checkpoint", "get_model"]


def load_checkpoint(model: nn.Module, checkpoint_file: str, remove_head: bool = True) -> nn.Module:
    """load checkpoints

    Args:
        model (nn.Module): model
        checkpoint_file (str): checkpoint filename
        remove_head (bool, optional): 是否去除[model.]. Defaults to True.

    Returns:
        nn.Module: model
    """
    state_dict = torch.load(checkpoint_file)["state_dict"]
    new_state_dict = dict()
    for name, value in state_dict.items():
        if remove_head and name[:6] == "model.":
            new_name = name[6:]
        else:
            new_name = name
        new_state_dict[new_name] = value
    model.load_state_dict(new_state_dict)
    return model


def get_best_checkpoint_from_folder(folder: str, select: str = "min") -> str:
    """从指定文件夹中获取最好的模型文件

    Args:
        folder (str): 指定文件夹
        select (str, optional): min or max. Defaults to "min".

    Returns:
        str: 最好的模型文件
    """
    assert select in ["min", "max"]

    name_list = os.listdir(folder)
    if "last.ckpt" in name_list:
        name_list.remove("last.ckpt")

    best_score = None
    best_name = None
    for name in name_list:
        score = float(name.split("=")[-1].replace(".ckpt", ""))
        if best_score is None:
            best_score, best_name = score, name

        if select == "min" and score < best_score:
            best_score, best_name = score, name
        elif select == "max" and score > best_score:
            best_score, best_name = score, name

    if best_name is None:
        return None

    return osp.join(folder, best_name)


def get_best_checkpoint(config_filename: str, select: str = "min") -> str:
    """获取当前配置下最好的模型文件

    Args:
        config_filename (str): 配置文件
        select (str, optional): min or max. Defaults to "min".

    Returns:
        str: 最好的模型文件
    """
    checkpoint_folder = osp.join(get_log_dir(config_filename), "checkpoint")
    return get_best_checkpoint_from_folder(checkpoint_folder, select=select)


def get_model(config_filename: str) -> nn.Module:
    """获取当前配置下的模型

    Args:
        config_filename (str): 配置文件

    Returns:
        nn.Module: model
    """
    config = load_config(config_filename)
    model = instantiate_from_config(config.model)
    return model


def convert_ckpt_to_pth(ckpt_filename: str, remove_head: bool = True):
    """将ckpt转换成pytorch可正常load的pth

    Args:
        ckpt_filename (str): ckpt filename
        remove_head (bool, optional): 是否去除[model.]. Defaults to True.
    """
    new_d = dict()
    new_d["state_dict"] = OrderedDict()

    d = torch.load(ckpt_filename)
    for name in d["state_dict"]:
        if remove_head and name[:6] == "model.":
            new_name = name[6:]
        else:
            new_name = name
        new_d["state_dict"][new_name] = d["state_dict"][name]
    torch.save(new_d, ckpt_filename.replace(".ckpt", ".pth"))
