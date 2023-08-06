import numpy as np
from torch.utils.data import Dataset


class RandomSplitDataset(Dataset):
    """随机划分部分数据集"""

    def __init__(self, dataset: Dataset, random_split: float = 1.0) -> None:
        super().__init__()

        self.dataset = dataset
        self.random_split = random_split

        N = len(self.dataset)
        n = int(N * float(random_split))
        self.__index_list = np.random.permutation(N)[:n].tolist()

    def __len__(self):
        return len(self.__index_list)

    def __getitem__(self, index):
        real_index = self.__index_list[index]
        return self.dataset.__getitem__(real_index)
