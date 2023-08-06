import sys

import pytorch_lightning as pl
from torch.utils.data import DataLoader

from ..datasets.split_dataset import RandomSplitDataset
from ..tools.logger import Logger
from .config import instantiate_from_config


class LightningDataset(pl.LightningDataModule):
    def __init__(self, train=None, validation=None, test=None):
        super().__init__()
        self.configs = {
            "train": train,
            "validation": validation,
            "test": test,
        }
        if train is not None:
            self.train_dataloader = self._train_dataloader
        if validation is not None:
            self.val_dataloader = self._val_dataloader
        if test is not None:
            self.test_dataloader = self._test_dataloader

    def _train_dataloader(self):
        return self.__get_dataloader(self.configs["train"])

    def _val_dataloader(self):
        return self.__get_dataloader(self.configs["validation"])

    def _test_dataloader(self):
        return self.__get_dataloader(self.configs["test"])

    def __get_dataloader(self, config) -> DataLoader:
        random_split = float(config["random_split"])
        if not (0 < random_split <= 1.0):
            Logger.error("random_split: (0.0, 1.0]")
            sys.exit(0)

        dataset = instantiate_from_config(config)
        if random_split != 1.0:
            Logger.info(f"RandomSplitDataset, random_split:{random_split:.4f}")
            dataset = RandomSplitDataset(dataset, random_split=random_split)

        return DataLoader(dataset=dataset, **config["data_loader"])


# def single_to_batch(data_dict):
#     batch = dict()
#     for key, value in data_dict.items():
#         if isinstance(value, torch.FloatTensor):
#             batch[key] = value.unsqueeze(0)
#         elif isinstance(value, int):
#             batch[key] = torch.LongTensor(value).unsqueeze(0)
#         elif isinstance(value, np.ndarray):
#             batch[key] = torch.from_numpy(value).unsqueeze(0)
#         else:
#             Logger.error(f"key:{key}, {type(value)}")
#     return batch
