import tensorflow as tf
from keras.layers import Conv2D
from .layers import deserialize_quant_object
from ..tensors import FixedPoint, MAX_BUFFER_BITWIDTH


__all__ = ["QuantizedConv2D"]


@tf.keras.utils.register_keras_serializable()
class QuantizedConv2D(Conv2D):
    """A convolutional layer that operates on quantized inputs and weights
    """

    def __init__(self, *args, quant_config=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.quant_config = quant_config
        self.out_quantizer = deserialize_quant_object(
            self.quant_config, "output_quantizer", False)
        self.weight_quantizer = deserialize_quant_object(
            self.quant_config, "weight_quantizer", True)
        if self.use_bias:
            self.bias_quantizer = deserialize_quant_object(
                self.quant_config, "bias_quantizer", True)
        self.buffer_bitwidth = self.quant_config.get(
            "buffer_bitwidth", MAX_BUFFER_BITWIDTH) - 1
        assert self.buffer_bitwidth > 0, "The buffer_bitwidth must be a strictly positive integer."

    def call(self, inputs, training=None):
        # raise an error if the inputs are not FixedPoint or tf.Tensor
        if not isinstance(inputs, (FixedPoint, tf.Tensor)):
            raise TypeError(f"QuantizedConv2D only accepts FixedPoint or tf.Tensor\
                              inputs. Receives {type(inputs)} inputs.")

        # Quantize the weights
        kernel = self.weight_quantizer(self.kernel, training)

        if isinstance(inputs, tf.Tensor):
            # Assume the inputs are integer stored as float, which is the only tf.Tensor
            # inputs that are allowed
            inputs = FixedPoint.quantize(inputs, 0, 8)

        inputs = inputs.promote(self.buffer_bitwidth)

        outputs = self.convolution_op(inputs, kernel)

        if self.use_bias:
            bias = self.bias_quantizer(self.bias, training)
            outputs = tf.add(outputs, bias)

        if self.out_quantizer is not None:
            outputs = self.out_quantizer(outputs, training)
        return outputs

    def get_config(self):
        config = super().get_config()
        config["quant_config"] = self.quant_config
        return config
