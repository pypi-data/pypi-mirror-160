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
import keras
import tensorflow as tf

from ..tensors import FixedPoint, MAX_BUFFER_BITWIDTH


__all__ = ["Add", "QuantizedAdd", "deserialize_quant_object"]


def deserialize_quant_object(quant_config, object_name, mandatory=True):
    """Wrapper function of tf.keras.utils.deserialize_keras_object.
    It allows to select the right config from the config file dict,
    and raises an error if no config found or set to None.
    If one is found, it returns the corresponding deserialized Keras
    object.

    Args:
        quant_config (dict): quantization config dictionnary.
        object_name (str): keras object name to deserialize.
        mandatory (bool, optional): flag to specify if the object to
            deserialize is mandatory. If yes raises an Error otherwise
            returns None. Defaults to True.

    Returns:
        :obj:`tensorflow.keras.class`: the targeted deserialized keras
            object.
    """
    object_dict = quant_config.get(object_name)
    if object_dict is None and mandatory:
        raise KeyError(f"{object_name} should be specified.")
    elif object_dict is None and not mandatory:
        return None
    deserialize_obj = tf.keras.utils.deserialize_keras_object(object_dict)
    return deserialize_obj


@tf.keras.utils.register_keras_serializable()
class Add(keras.layers.Layer):
    """Wrapper class of `keras.layers.Add` that allows to average inputs.
    We only support a tuple of two inputs with same shape.

    Args:
        average (bool, optional): if `True`, compute the average across all inputs.
            Defaults to `False`.
    """

    def __init__(self, *args, average=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.average = average

    def build(self, input_shape):
        if not isinstance(input_shape, (list, tuple)) or len(input_shape) != 2:
            raise ValueError(f"{self.__class__.__name__} expects two input tensors")

    def call(self, inputs, training=False):
        a, b = inputs
        output = tf.add(a, b)
        if self.average:
            output /= 2
        return output

    def get_config(self):
        config = super().get_config()
        config["average"] = self.average
        return config


@tf.keras.utils.register_keras_serializable()
class QuantizedAdd(Add):
    """Sums two inputs and quantize the output.

    The two inputs must be provided as a list or tuple of FixedPoint or Tensors.

    The outputs are quantized according to the specified quantization configuration.

    Args:
        quant_config (dict, optional): the serialized quantization configuration.
            Defaults to empty configuration.
    """

    def __init__(self, *args, quant_config={}, **kwargs):
        super().__init__(*args, **kwargs)
        self.quant_config = quant_config
        self.buf_bits = self.quant_config.get(
            "buffer_bitwidth", MAX_BUFFER_BITWIDTH) - 1
        self.out_quantizer = deserialize_quant_object(
            self.quant_config, "output_quantizer", False)

    def call(self, inputs, training=None):
        a, b = inputs
        if not (isinstance(a, FixedPoint) and isinstance(b, FixedPoint)):
            # If any of the inputs is not a FixedPoint, raise an error
            raise TypeError(f"QuantizedAdd only accepts FixedPoint\
                              inputs. Receives {(type(a), type(b))} inputs.")

        # Promote a before performing the addition
        a = a.promote(self.buf_bits)
        outputs = tf.add(a, b)
        if self.average:
            outputs //= 2
        if self.out_quantizer is not None:
            outputs = self.out_quantizer(outputs, training=training)
        return outputs

    def get_config(self):
        config = super().get_config()
        config["quant_config"] = self.quant_config
        return config
