#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from absl import flags
from absl import app as absl_app

import numpy as np
import tensorflow as tf
from sys import argv

if __name__ == "__main__":
    model_dir = argv[1]
    print('Model dir set to: {}'.format(model_dir))
    with tf.Session() as sess:
        saver = tf.train.import_meta_graph(model_dir + 'model.ckpt-18426.meta')
        saver.restore(sess, tf.train.latest_checkpoint(model_dir))
        print('ops')
        for op in sess.graph.get_operations():
            print(op)
