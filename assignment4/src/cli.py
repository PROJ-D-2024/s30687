from __future__ import annotations

import argparse
import json

from src.evaluate import run_evaluation
from src.preprocess import run_preprocessing
from src.train import run_training


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Unified entry point for Assignment 4 reproducibility pipeline.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command_name, help_text in {
        "preprocess": "Build the processed analytical dataset.",
        "train": "Train one configured experiment and store traceable artifacts.",
        "evaluate": "Read the stored metrics/metadata for one configured experiment.",
    }.items():
        command_parser = subparsers.add_parser(command_name, help=help_text)
        command_parser.add_argument("--config", required=True, help="Path to YAML configuration file.")

    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "preprocess":
        payload = run_preprocessing(args.config)
    elif args.command == "train":
        payload = run_training(args.config)
    else:
        payload = run_evaluation(args.config)

    print(json.dumps(payload, indent=2))