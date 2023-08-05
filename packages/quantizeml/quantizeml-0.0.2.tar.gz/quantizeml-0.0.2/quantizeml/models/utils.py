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
Common utility methods used in quantization models.
"""

import tensorflow_addons as tfa
from keras.models import clone_model, load_model as kload_model

__all__ = ['load_model', 'deep_clone_model']


def load_model(model_path, custom_layers={}, compile_model=True):
    """Loads a model with Vision Transformer custom layers.

    Args:
        model_path (str): path of the model to load
        custom_layers (dict, optional): custom layers to add to the model. Defaults to {}.
        compile_model (bool, optional): whether to compile the model. Defaults to True.

    Returns:
        :class:`keras.models.Model`: the loaded model
    """
    # Given that all layers were imported in __init__.py, they are registered.
    # Therefore, we just need append GroupNormalization in the custom layers.
    custom_layers.update({'GroupNormalization': tfa.layers.GroupNormalization})
    return kload_model(model_path, custom_objects=custom_layers, compile=compile_model)


def deep_clone_model(model, *args, **kwargs):
    """Clone a model, assign variable to variable. Useful when a clone function is used,
    and new layers have not the same number of parameters as the original layer.

    Args:
        model (:class:`keras.models.Model`): model to be cloned
        args, kwargs (optional): arguments pass to :func:`keras.models.clone_model` function

    Returns:
        :class:`keras.models.Model`: the cloned model
    """
    def _assign_variables(src_layer, dst_layer):
        for dst_v in dst_layer.variables:
            for src_v in src_layer.variables:
                if dst_v.name == src_v.name:
                    dst_v.assign(src_v)
                    break

    new_model = clone_model(model, *args, **kwargs)
    for layer in model.layers:
        new_layer = new_model.get_layer(layer.name)
        _assign_variables(layer, new_layer)
    return new_model
