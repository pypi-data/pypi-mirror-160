import gc
import os

import numpy as np
import pytorch_lightning as pl
import torch
import wandb
from pytorch_lightning.callbacks import EarlyStopping, ModelCheckpoint
from pytorch_lightning.loggers import WandbLogger
from torch.utils.data import DataLoader
from tqdm import tqdm

from flower_classifier.configs.config import get_cfg_defaults
from flower_classifier.dataload.dataload import FlowerDataModule, FlowerDataset
from flower_classifier.model.learner import FlowerLearner
from flower_classifier.utils.logging import make_logger
from flower_classifier.utils.metrics import calculate_metrics
from flower_classifier.utils.utils import get_device


class Orchestrator:
    def __init__(self, run_mode: str = 'train'):
        self.cfg = get_cfg_defaults()
        self.logger = make_logger(name=self.cfg.LOG.NAME)
        self.run_mode = run_mode

    def make_dirs(self):
        dirs = [self.cfg.ADDRESS.DATA, self.cfg.ADDRESS.CHECK]

        for d in dirs:
            if not os.path.exists(d):
                os.mkdir(d)
                self.logger.info(f'mkdir {d}')

    def train(self):
        self.logger.info('+ Train +')
        self.logger.info(f'configuration: \n {self.cfg}')

        data_module = FlowerDataModule(self.cfg, self.logger)
        train_loader, val_loader, test_data = data_module.build()

        learner = FlowerLearner(cfg=self.cfg)

        wandb_logger = WandbLogger(project='flower_classifier', name=self.cfg.TRAIN.RUN_NAME)

        callbacks = [
            ModelCheckpoint(
                dirpath=self.cfg.ADDRESS.CHECK,
                filename=f'{self.cfg.MODEL.NAME}_' + '{epoch}-{val_acc:.2f}',
                mode='max',
                every_n_epochs=1,
            ),
            EarlyStopping(monitor='val_acc', patience=self.cfg.TRAIN.PATIENCE, mode='max'),
        ]

        trainer = pl.Trainer(
            max_epochs=self.cfg.TRAIN.EPOCHS, gpus=self.cfg.TRAIN.GPUS, logger=wandb_logger, callbacks=callbacks
        )

        trainer.fit(learner, train_loader, val_loader)

        self.logger.info('+ Test +')

        test_dataset = FlowerDataset(cfg=self.cfg, data=test_data)

        test_loader = DataLoader(
            test_dataset,
            batch_size=self.cfg.TRAIN.BATCH_SIZE,
            shuffle=False,
            num_workers=0,
            pin_memory=True,
        )

        device = get_device()
        model = learner.model.to(device)
        model.eval()

        loop = tqdm(test_loader, total=int(len(test_loader)))

        pred_list = []

        for batch in loop:
            batch = {'image': batch['image'].to(device)}

            pred = list(model(batch).detach().cpu().numpy())
            pred_list.extend(pred)

        preds = torch.as_tensor(np.array(pred_list, dtype=torch.float32).reshape(-1, 1))
        target = test_dataset[:]['label'].type(torch.int32)

        del pred_list
        gc.collect()

        metrics = calculate_metrics(self.cfg, preds, target)

        self.logger.info(
            f'''
            Acc: {metrics['acc']}
            F1-macro: {metrics['f1_macro']}
            '''
        )

    def upload_best_weights(self, weight_name: str):
        run = wandb.init(project='flower_classifier')

        artifact = wandb.Artifact(
            name='best_flower_classifier',
            type='model',
            description=f'{weight_name}',
            metadata=None,
        )
        artifact.add_file(os.path.join(self.cfg.ADDRESS.CHECK, 'best_model.ckpt'))

        run.log_artifact(artifact)
        run.finish()

    def run(self):
        if self.run_mode == 'train':
            self.train()

        # TODO: other run modes

        else:
            raise ValueError('run_mode must be train')
