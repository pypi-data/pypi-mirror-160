import glob
import os
from logging import Logger
from typing import Dict

from torchvision.datasets import Flowers102
from yacs.config import CfgNode


class FlowerDownloader(object):
    def __init__(self, cfg: CfgNode, logger: Logger):
        self.cfg = cfg
        self.logger = logger

    def download(self) -> Dict:
        address = os.path.join(os.getcwd(), self.cfg.ADDRESS.DATA)

        file = glob.glob(os.path.join(self.cfg.ADDRESS.DATA, 'flowers-102/*.mat'))

        if len(file) == 0:
            self.logger.info('download files')

        else:
            self.logger.info('skip download')

        data = {
            'train': Flowers102(root=address, split='train', download=True),
            'val': Flowers102(root=address, split='val', download=True),
            'test': Flowers102(root=address, split='test', download=True),
        }

        return data

    def print_min_height_width(self, data: Flowers102):
        min_width = 1e10
        min_height = 1e10

        for i in range(len(data)):
            width, height = data[i][0].size

            if width < min_width:
                min_width = width
            if height < min_height:
                min_height = height

        self.logger.info(f'Min Width: {min_width}, Min Height: {min_height}')
