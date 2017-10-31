import numpy as np
import tensorflow as tf

from .base_net import BaseNet
from .operations import *


class RGBNet(BaseNet):
    def __init__(self, x: tf.Tensor, image_shape: np.ndarray, num_classes: int, keep_prob: float, *args, **kwargs):
        super(self.__class__, self).__init__(x=x, image_shape=image_shape, num_classes=num_classes, name="RGBNet")
        self.keep_probability = keep_prob

        self.create()

    def create(self):
        with tf.variable_scope(self.name):
            current_shape = self.flat_shape
            with tf.variable_scope('conv_1'):
                h_conv1_0 = conv_relu(x=self.x, kernel_shape=[3, 3, self.channels, 12], bias_shape=[12], name="_0")
                h_pool1 = max_pool_4x4(name="max_pool", x=h_conv1_0)
                current_shape = self.update_shape(current_shape, 4)
                # 24 30
            with tf.variable_scope('conv_2'):
                h_conv2_0 = conv_relu(x=h_pool1, kernel_shape=[3, 3, 12, 24], bias_shape=[24], name="_0")
                h_pool2 = max_pool_4x4(name="max_pool", x=h_conv2_0)
                current_shape = self.update_shape(current_shape, 4)
                # 6 8

            with tf.variable_scope('full_connected_1'):
                h_pool1_flat = tf.reshape(h_pool2, [-1, np.prod(current_shape) * 24])

                W_fc1 = weight_variable(name="W", shape=[np.prod(current_shape) * 24, 512])
                b_fc1 = bias_variable(name="b", shape=[512])

                h_fc1 = tf.nn.relu(tf.matmul(h_pool1_flat, W_fc1 + b_fc1))

                with tf.variable_scope('drop_out_1'):
                    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob=self.keep_probability, name="dropout")

            with tf.variable_scope('full_connected_2'):
                W_fc2 = weight_variable(name="W", shape=[512, 32])
                b_fc2 = bias_variable(name="b", shape=[32])

                h_fc2 = tf.nn.relu(tf.matmul(h_fc1_drop, W_fc2 + b_fc2))

                with tf.variable_scope('drop_out_2'):
                    h_fc2_drop = tf.nn.dropout(h_fc2, keep_prob=self.keep_probability, name="dropout")

            with tf.variable_scope('full_connected_3'):
                W_fc3 = weight_variable(name="W", shape=[32, self.num_classes])
                b_fc3 = bias_variable(name="b", shape=[self.num_classes])

                self.logits = tf.matmul(h_fc2_drop, W_fc3) + b_fc3
