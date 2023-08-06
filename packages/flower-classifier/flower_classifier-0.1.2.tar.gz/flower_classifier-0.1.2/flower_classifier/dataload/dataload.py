from logging import Logger
from typing import Dict, Tuple

import albumentations as A
import numpy as np
import torch
from albumentations.pytorch import ToTensorV2
from torch.utils.data import DataLoader, Dataset
from torchvision.datasets.flowers102 import Flowers102
from yacs.config import CfgNode

from flower_classifier.dataload.download import FlowerDownloader


class FlowerDataset(Dataset):
    def __init__(self, cfg, data, transform=None):
        self.cfg = cfg
        self.data = data
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx) -> Dict:
        image, label = self.data[idx]
        image = np.array(image)

        if self.transform is not None:
            image = self.transform(image=image)["image"]

        image = torch.as_tensor(image, dtype=torch.float32)
        label = torch.as_tensor(label, dtype=torch.int64)

        return {'image': image, 'label': label}


class FlowerDataModule:
    def __init__(self, cfg: CfgNode, logger: Logger):
        super().__init__()
        self.cfg = cfg
        self.logger = logger

    def prepare_data(self) -> Dict:
        self.logger.info('prepare data')

        downloader = FlowerDownloader(self.cfg, self.logger)
        data = downloader.download()
        downloader.print_min_height_width(data['test'])

        return data

    def create_dataloader(self, data: Dict) -> Tuple[DataLoader, DataLoader, Flowers102]:
        self.logger.info('create dataloader')

        # SmallestMaxSize: img의 짧은 면의 최대 size를 max_size로 제한함
        # ShiftScaleRotate: 이동, 크기 조절, 회전
        # RandomBrightnessContrast: 밝기 조절
        # Normalize: (img - mean * max_pixel_value) / (std * max_pixel_value)
        # ToTensorV2: img, mask를 pytorch tensor로 바뀜 (ToTensor는 deprecated)
        # -> (C, H, W) = (channle, height, width) 또는 (H, W) 형태로 바뀜

        train_transform = A.Compose(
            [
                A.SmallestMaxSize(max_size=500),
                A.ShiftScaleRotate(shift_limit=0.05, scale_limit=0.05, rotate_limit=15, p=0.5),
                A.RandomCrop(height=256, width=256),
                A.RGBShift(r_shift_limit=15, g_shift_limit=15, b_shift_limit=15, p=0.5),
                A.RandomBrightnessContrast(p=0.5),
                A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
                ToTensorV2(),
            ]
        )
        train_dataset = FlowerDataset(cfg=self.cfg, data=data['train'], transform=train_transform)

        val_transform = A.Compose(
            [
                A.SmallestMaxSize(max_size=500),
                A.CenterCrop(height=256, width=256),
                A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
                ToTensorV2(),
            ]
        )
        val_dataset = FlowerDataset(cfg=self.cfg, data=data['val'], transform=val_transform)

        train_loader = DataLoader(
            train_dataset,
            batch_size=self.cfg.TRAIN.BATCH_SIZE,
            shuffle=True,
            num_workers=self.cfg.TRAIN.NUM_WORKERS,
            pin_memory=True,
            drop_last=True,
        )

        val_loader = DataLoader(
            val_dataset,
            batch_size=self.cfg.TRAIN.BATCH_SIZE,
            shuffle=False,
            num_workers=self.cfg.TRAIN.NUM_WORKERS,
            pin_memory=True,
            drop_last=False,
        )

        return train_loader, val_loader, data['test']

    def build(self) -> Tuple[DataLoader, DataLoader, Flowers102]:
        data = self.prepare_data()
        train_loader, val_loader, test_data = self.create_dataloader(data)

        return train_loader, val_loader, test_data
