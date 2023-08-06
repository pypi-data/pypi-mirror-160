from typing import Dict

from torch import Tensor
from torchmetrics.functional import accuracy, f1_score
from yacs.config import CfgNode


def calculate_metrics(cfg: CfgNode, preds: Tensor, target: Tensor) -> Dict:
    metrics = {
        'acc': accuracy(preds=preds, target=target),
        'f1_macro': f1_score(preds, target, average='macro', num_classes=cfg.DATA.NUM_CLASSES),
    }

    return metrics
