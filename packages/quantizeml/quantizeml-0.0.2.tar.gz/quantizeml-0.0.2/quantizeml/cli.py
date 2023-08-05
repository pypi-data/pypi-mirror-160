#!/usr/bin/env python
# ******************************************************************************
# Copyright 2022 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
"""
quantizeml main command-line interface.
"""

import argparse
import json
import os
import sys

from .models import load_model, quantize
from .transforms import fold_rescaling


def main():
    """ CLI entry point.

    Contains an argument parser with specific arguments depending on the model to be created.
    Complete arguments lists available using the -h or --help argument.

    """
    parser = argparse.ArgumentParser()
    sp = parser.add_subparsers(dest="action")
    sp.add_parser("version", help="Display quantizeml version.")
    q_parser = sp.add_parser("quantize", help="Display quantizeml version.")
    q_parser.add_argument("-m", "--model", type=str, required=True, help="Model to quantize")
    q_parser.add_argument("-c", "--quantization_config", type=str,
                          required=True, help="Quantization configuration file")
    q_parser.add_argument("-n", "--name", action="store_true",
                          help="Print quantized output model filename")
    q_parser.add_argument("-f", "--fold", action="store_true",
                          help="Collapse foldable layers before quantizing")

    args = parser.parse_args()

    if args.action == "version":
        # importlib.metadata was introduced in Python 3.8 and is available to older versions as the
        # importlib-metadata project
        if sys.version_info >= (3, 8):
            from importlib import metadata
        else:
            import importlib_metadata as metadata
        print(metadata.version('quantizeml'))
    elif args.action == "quantize":
        # Build name for the output model
        model_name = os.path.splitext(args.model)[0]
        config_name = os.path.splitext(os.path.basename(args.quantization_config))[0]
        output_name = f"{model_name}_{config_name}.h5"

        # When arg.name is requested, simply print out the output model name
        if args.name:
            print(output_name)
            exit(0)

        # Load the configuration file and the model
        with open(args.quantization_config) as f:
            config = json.load(f)
        model = load_model(args.model)

        # Fold layers
        if args.fold:
            print(f"Collapsing foldable layers of {args.model}.")
            model = fold_rescaling(model)

        # Quantize the model and save it
        print(f"Quantizing model {args.model} with configuration file {args.quantization_config}.")
        model_q = quantize(model, config)
        model_q.save(output_name, include_optimizer=False)
        print(f"Saved quantized model to {output_name}.")
