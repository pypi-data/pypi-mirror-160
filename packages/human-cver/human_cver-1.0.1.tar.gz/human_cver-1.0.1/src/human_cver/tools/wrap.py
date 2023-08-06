import torch
import numpy as np


def list2numpy(a: list):
    return np.array(a, dtype=np.float32)


def list2tensor(a: list):
    return torch.from_numpy(list2numpy(a))


def numpy2tensor(a: np.ndarray):
    return torch.from_numpy(a)
