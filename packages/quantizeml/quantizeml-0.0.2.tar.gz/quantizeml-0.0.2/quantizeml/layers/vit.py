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

import tensorflow as tf

from .layers import deserialize_quant_object
from ..tensors import QTensor, FixedPoint, MAX_BUFFER_BITWIDTH


# Restrict list of exported symbols on default import
__all__ = ["ClassToken", "QuantizedClassToken",
           "AddPositionEmbs", "QuantizedAddPositionEmbs"]


@tf.keras.utils.register_keras_serializable()
class ClassToken(tf.keras.layers.Layer):
    """Append a class token to an input layer."""

    def build(self, input_shape):
        super().build(input_shape)
        cls_init = tf.keras.initializers.TruncatedNormal(stddev=0.02)
        self.hidden_size = input_shape[-1]
        self.cls = tf.Variable(
            name="cls",
            initial_value=cls_init(
                shape=(1, 1, self.hidden_size), dtype="float32"),
            trainable=True,
        )

    def call(self, inputs, training=None):
        batch_size = tf.shape(inputs)[0]
        cls_broadcasted = tf.cast(
            tf.broadcast_to(self.cls, [batch_size, 1, self.hidden_size]),
            dtype=inputs.dtype,
        )
        return tf.concat([cls_broadcasted, inputs], 1)


@tf.keras.utils.register_keras_serializable()
class AddPositionEmbs(tf.keras.layers.Layer):
    """Adds (optionally learned) positional embeddings to the inputs."""

    def build(self, input_shape):
        assert len(
            input_shape) == 3, f"Number of dimensions should be 3, got {len(input_shape)}"
        super().build(input_shape)
        pe_init = tf.keras.initializers.TruncatedNormal(stddev=0.02)
        self.pe = tf.Variable(
            name="pos_embedding",
            initial_value=pe_init(shape=(1, input_shape[1], input_shape[2])),
            dtype="float32",
            trainable=True,
        )

    def call(self, inputs, training=None):
        return inputs + tf.cast(self.pe, dtype=inputs.dtype)


@tf.keras.utils.register_keras_serializable()
class QuantizedClassToken(ClassToken):
    """Quantize the :class:`ClassToken` layer, allowing quantization of the output.
    """

    def __init__(self, *args, quant_config={}, **kwargs):
        super().__init__(*args, **kwargs)
        self.quant_config = quant_config
        self.out_quantizer = deserialize_quant_object(
            self.quant_config, "output_quantizer", False)

    def call(self, inputs, training=None):
        if isinstance(inputs, QTensor):
            inputs = inputs.to_float()
        outputs = super().call(inputs, training)
        if self.out_quantizer is not None:
            outputs = self.out_quantizer(outputs, training=training)
        return outputs

    def get_config(self):
        config = super().get_config()
        config["quant_config"] = self.quant_config
        return config


@tf.keras.utils.register_keras_serializable()
class QuantizedAddPositionEmbs(AddPositionEmbs):
    """Quantize the :class:`AddPositionEmbs` layer, allowing operations in FixedPoint domain.
    """

    def __init__(self, *args, quant_config={}, **kwargs):
        super().__init__(*args, **kwargs)
        self.quant_config = quant_config
        self.out_quantizer = deserialize_quant_object(
            self.quant_config, "output_quantizer", False)
        self.pe_quantizer = deserialize_quant_object(
            self.quant_config, "pe_quantizer", True)
        self.buffer_bitwidth = self.quant_config.get(
            "buffer_bitwidth", MAX_BUFFER_BITWIDTH) - 1

    def call(self, inputs, training=None):
        # raise an error if the inputs are not FixedPoint
        if not isinstance(inputs, FixedPoint):
            raise TypeError(f"QuantizedAddPositionEmbs only accepts FixedPoint\
                              inputs. Receives {type(inputs)} inputs.")

        inputs = inputs.promote(self.buffer_bitwidth)
        outputs = inputs + self.pe_quantizer(self.pe, training=training)

        if self.out_quantizer is not None:
            outputs = self.out_quantizer(outputs)
        return outputs

    def get_config(self):
        config = super().get_config()
        config["quant_config"] = self.quant_config
        return config
