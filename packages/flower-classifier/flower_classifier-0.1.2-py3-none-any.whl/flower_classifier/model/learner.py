from typing import Dict, Tuple

import pytorch_lightning as pl
import torch
from timm import create_model
from torch import Tensor
from torchmetrics.functional import accuracy, f1_score
from yacs.config import CfgNode

from flower_classifier.model.scheduler import CosineAnnealingWarmupRestarts


class FlowerLearner(pl.LightningModule):
    def __init__(self, cfg: CfgNode):
        super().__init__()
        self.save_hyperparameters()

        self.cfg = cfg

        self.model = create_model(
            model_name=cfg.MODEL.NAME,
            pretrained=True,
            num_classes=cfg.DATA.NUM_CLASSES,
        )

    def forward(self, inputs):
        pred = self.model(inputs)

        return pred

    def training_step(self, batch, batch_idx):
        loss, metrics = self._calculate_loss_and_metrics(batch, 'train')
        self.log_dict(metrics)

        return loss

    def validation_step(self, batch, batch_idx):
        loss, metrics = self._calculate_loss_and_metrics(batch, 'val')
        self.log_dict(metrics)

        return loss

    def predict_step(self, batch, batch_idx):
        pred = self.model(batch).squeeze(dim=1)

        return pred

    def configure_optimizers(self):
        if self.cfg.TRAIN.OPTIMIZER == 'adam':
            optimizer = torch.optim.Adam(params=self.model.parameters(), lr=0)

            scheduler = CosineAnnealingWarmupRestarts(
                optimizer=optimizer,
                first_cycle_steps=self.cfg.TRAIN.FIRST_CYCLE_STEPS,
                cycle_mult=self.cfg.TRAIN.CYCLE_MULT,
                max_lr=self.cfg.TRAIN.MAX_LR,
                min_lr=self.cfg.TRAIN.MIN_LR,
                warmup_steps=self.cfg.TRAIN.WARMUP_STEPS,
                gamma=self.cfg.TRAIN.GAMMA,
            )

            return {'optimizer': optimizer, 'lr_scheduler': {'scheduler': scheduler, 'monitor': 'train_loss'}}

        elif self.cfg.TRAIN.OPTIMIZER == 'radam':
            optimizer = torch.optim.RAdam(
                params=self.model.parameters(),
                lr=self.cfg.TRAIN.LR,
                betas=(0.9, 0.999),
                eps=1e-8,
                weight_decay=self.cfg.TRAIN.WEIGHT_DECAY,
            )

            return optimizer

        else:
            raise ValueError('optimizer must be adam or radam')

    def _calculate_loss_and_metrics(self, batch: Dict, prefix: str) -> Tuple[Tensor, Dict]:
        preds = self.model(batch['image'])
        target = batch['label']

        loss_func = torch.nn.CrossEntropyLoss()
        loss = loss_func(preds, target)

        # convert type to calculate binary classification metrics
        target = target.type(torch.int32)

        metrics = {
            f'{prefix}_loss': float(loss.detach().cpu().numpy()),
            f'{prefix}_acc': accuracy(preds=preds, target=target),
            f'{prefix}_f1_macro': f1_score(preds, target, average='macro', num_classes=self.cfg.DATA.NUM_CLASSES),
        }

        return loss, metrics
