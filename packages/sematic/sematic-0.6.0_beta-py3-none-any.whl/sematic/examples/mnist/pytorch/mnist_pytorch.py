"""
This is an example implementation of the MNIST pipeline in PyTorch on sematic.
"""
# MNIST example
import argparse
from sematic.examples.mnist.pytorch.pipeline import (
    PipelineConfig,
    DataLoaderConfig,
    TrainConfig,
    scan_learning_rate,
)
from sematic import CloudResolver
import logging

logging.basicConfig(level=logging.INFO)


PIPELINE_CONFIG = PipelineConfig(
    dataloader_config=DataLoaderConfig(),
    train_config=TrainConfig(epochs=1),
)


TRAIN_CONFIGS = [
    TrainConfig(epochs=1, learning_rate=0.2),
    TrainConfig(epochs=5, learning_rate=0.4),
    TrainConfig(epochs=5, learning_rate=0.6),
    TrainConfig(epochs=5, learning_rate=0.8),
]


def main():
    parser = argparse.ArgumentParser("MNIST PyTorch example")
    parser.add_argument("--detach", default=False, action="store_true")
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--learning-rates", type=str, default="1")

    args = parser.parse_args()

    epochs = args.epochs
    learning_rates = map(float, args.learning_rates.split(","))

    train_configs = [
        TrainConfig(epochs=epochs, learning_rate=learning_rate)
        for learning_rate in learning_rates
    ]

    scan_learning_rate(
        dataloader_config=DataLoaderConfig(), train_configs=train_configs
    ).set(name="Scan MNIST learning rates").resolve(CloudResolver(detach=args.detach))


if __name__ == "__main__":
    main()
