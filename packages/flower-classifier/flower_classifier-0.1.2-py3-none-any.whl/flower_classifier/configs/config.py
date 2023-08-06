import argparse

from yacs.config import CfgNode as CN

_C = CN()

# directories
_C.ADDRESS = CN()
_C.ADDRESS.DATA = 'data/'
_C.ADDRESS.CHECK = 'checkpoints/'

# log
_C.LOG = CN()
_C.LOG.NAME = 'vision'

# data
_C.DATA = CN()
_C.DATA.NUM_CLASSES = 102

# model
_C.MODEL = CN()
_C.MODEL.NAME = 'resnet50d'
# 'resnest26d', 'res2net50_14w_8s'

# train
_C.TRAIN = CN()
_C.TRAIN.RUN_NAME = 'resnet50d'

_C.TRAIN.BATCH_SIZE = 32
_C.TRAIN.NUM_WORKERS = 0
_C.TRAIN.GPUS = 1
_C.TRAIN.EPOCHS = 100
_C.TRAIN.PATIENCE = 10

_C.TRAIN.OPTIMIZER = 'radam'

_C.TRAIN.LR = 1e-4
_C.TRAIN.WEIGHT_DECAY = 1e-4

_C.TRAIN.FIRST_CYCLE_STEPS = 100
_C.TRAIN.CYCLE_MULT = 0.5
_C.TRAIN.MAX_LR = 1e-3
_C.TRAIN.MIN_LR = 1e-5
_C.TRAIN.WARMUP_STEPS = 20
_C.TRAIN.GAMMA = 1.0

# inference
_C.INFERENCE = CN()


def get_cfg_defaults():
    """
    get a yacs CfgNode object with default values
    """
    return _C.clone()


def parse_arguments():
    parser = argparse.ArgumentParser(description='parser')
    parser.add_argument('--run_mode', '-r', type=str, default='train', help='run mode')

    args = parser.parse_args()

    return args
