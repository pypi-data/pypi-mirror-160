import logging
import os
from pathlib import Path

import numpy as np
import pytorch_lightning as pl
import torch
from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_lightning.utilities import rank_zero_only
from pytorch_lightning.utilities import rank_zero_info


def count_trainable_parameters(model):
    model_parameters = filter(lambda p: p.requires_grad, model.parameters())
    params = sum([np.prod(p.size()) for p in model_parameters])
    return params


logger = logging.getLogger(__name__)


class Seq2SeqLoggingCallback(pl.Callback):
    @rank_zero_only
    def _write_logs(
        self,
        trainer: pl.Trainer,
        pl_module: pl.LightningModule,
        type_path: str,
        save_generations=True,
    ) -> None:
        logger.info(
            f"***** {type_path} results at step {trainer.global_step:05d} *****"
        )
        metrics = trainer.callback_metrics
        trainer.logger.log_metrics(
            {
                k: v
                for k, v in metrics.items()
                if k not in ["log", "progress_bar", "preds"]
            }
        )
        # Log results
        od = Path(pl_module.config.output_dir)
        if type_path == "test":
            results_file = od / "test_results.txt"
            generations_file = od / "test_generations.txt"
        else:
            # this never gets hit. I prefer not to save intermediate generations, and results are in metrics.json
            # If people want this it will be easy enough to add back.
            results_file = od / f"{type_path}_results/{trainer.global_step:05d}.txt"
            generations_file = (
                od / f"{type_path}_generations/{trainer.global_step:05d}.txt"
            )
            results_file.parent.mkdir(exist_ok=True)
            generations_file.parent.mkdir(exist_ok=True)
        with open(results_file, "a+") as writer:
            for key in sorted(metrics):
                if key in ["log", "progress_bar", "preds"]:
                    continue
                val = metrics[key]
                if isinstance(val, torch.Tensor):
                    val = val.item()
                msg = f"{key}: {val:.6f}\n"
                writer.write(msg)

        if not save_generations:
            return

        if "preds" in metrics:
            content = "\n".join(metrics["preds"])
            generations_file.open("w+").write(content)

    @rank_zero_only
    def on_train_start(self, trainer, pl_module):
        try:
            npars = pl_module.model.model.num_parameters()
        except AttributeError:
            npars = pl_module.model.num_parameters()

        n_trainable_pars = count_trainable_parameters(pl_module)
        # mp stands for million parameters
        trainer.logger.log_metrics(
            {"n_params": npars, "mp": npars / 1e6, "grad_mp": n_trainable_pars / 1e6}
        )

    @rank_zero_only
    def on_test_end(self, trainer: pl.Trainer, pl_module: pl.LightningModule):
        return self._write_logs(trainer, pl_module, "test")


def get_checkpoint_callback(output_dir, metric):
    """Saves the best model by validation ROUGE2 score."""
    if metric == "rouge2":
        exp = "{val_avg_rouge2:.4f}-{step_count}"
    elif metric == "bleu":
        exp = "{val_avg_bleu:.4f}-{step_count}"
    else:
        raise NotImplementedError(
            f"seq2seq callbacks only support rouge2 and bleu, got {metric},"
            "You can make your own by adding to this function."
        )

    checkpoint_callback = ModelCheckpoint(
        dirpath=output_dir,
        filename=exp,
        monitor=f"val_{metric}",
        mode="max",
        save_top_k=1,
    )
    return checkpoint_callback


class LoggingCallback(pl.Callback):
    def on_batch_end(self, trainer, pl_module):
        lrs = {f"lr_group_{i}": lr for i, lr in enumerate(self.lr_scheduler.get_lr())}
        pl_module.logger.log_metrics(lrs)

    def on_validation_end(self, trainer: pl.Trainer, pl_module: pl.LightningModule):
        rank_zero_info("***** Validation results *****")
        metrics = trainer.callback_metrics
        # Log results
        for key in sorted(metrics):
            if key not in ["log", "progress_bar"]:
                rank_zero_info("{} = {}\n".format(key, str(metrics[key])))

    def on_test_end(self, trainer: pl.Trainer, pl_module: pl.LightningModule):
        rank_zero_info("***** Test results *****")
        metrics = trainer.callback_metrics
        # Log and save results to file
        output_test_results_file = os.path.join(
            pl_module.base_config.output_dir, "test_results.txt"
        )
        with open(output_test_results_file, "w") as writer:
            for key in sorted(metrics):
                if key not in ["log", "progress_bar"]:
                    rank_zero_info("{} = {}\n".format(key, str(metrics[key])))
                    writer.write("{} = {}\n".format(key, str(metrics[key])))
