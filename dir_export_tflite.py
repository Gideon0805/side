"""
inference model export
 python pb_export_tflite.py \
--pb_graph 'PE_MOBILENET_V2_0.5_MSE_OHEM_F4_320_256_v2.pb' \
--input_node=cropped_image \
--output_nodes 'output/BiasAdd' \
--converter_type 'int'
model : the path of ckpt folder, must include 4 files:
    1. checkpoint 
    2. ckpt_name.data-00000-of-00001
    3. ckpt_name.index
    4. ckpt_name.meta
export file order
.pb
.h5
"""


import os
import logging
import numpy as np
import tensorflow as tf
from tensorflow.python.tools.freeze_graph import freeze_graph
from tensorflow.python.tools import optimize_for_inference_lib


slim = tf.contrib.slim
flags = tf.app.flags
flags.DEFINE_string(
    'savemodel_dir',
    '',
    'SAVEMODEL DIR PATH'
)
flags.DEFINE_string(
    'input_node',
    'input',
    'Node name of input'
)
flags.DEFINE_string(
    'output_node',
    'mobilefacenet/embedding',
    'Nodes of output, seperated by comma'
)
flags.DEFINE_string(
    'converter_type',
    'float',
    'Tflite Converter Type. (float, int, awaring)'
)

FLAGS = flags.FLAGS

'''
optimize inference model
Remove the indentity ops that are in the original model.
'''
def optimize_inference_model(frozen_graph_path,
                             optimized_graph_path,
                             input_node_names,
                             output_node_names):
    print('Reading frozen graph...')
    input_graph_def = tf.GraphDef()
    with tf.gfile.Open(frozen_graph_path, 'rb') as f:
        data2read = f.read()
        input_graph_def.ParseFromString(data2read)

    print('Optimizing frozen graph...')
    output_graph_def = optimize_for_inference_lib.optimize_for_inference(
        input_graph_def,
        input_node_names.split(','),  # an array of the input node(s)
        output_node_names.split(','),  # an array of the output nodes
        tf.float32.as_datatype_enum
    )

    print('Saving the optimized graph .pb file...')
    with tf.gfile.FastGFile(optimized_graph_path, 'w') as f:
        f.write(output_graph_def.SerializeToString())
        

def main(_):

    # pb_path = FLAGS.pb_path
    saved_model_dir = FLAGS.savemodel_dir
    # opt_pb_path = FLAGS.pb_path
    # optimize_inference_model(FLAGS.pb_path, opt_pb_path, FLAGS.input_node, FLAGS.output_node)

    ############# tflite file saving #############
    print('======================================')
    print('Saving .tflite file...')
    # tflite_path = pb_path.replace('.pb', '.tflite') # tflite file path
    tflite_path = saved_model_dir + '/savemodel.tflite'

    input_arrays = FLAGS.input_node.split(',')
    output_arrays = FLAGS.output_node.split(',')

    print(input_arrays)
    ### converter setting ###
# ==== FROM PB
    # converter = tf.lite.TFLiteConverter.from_frozen_graph(pb_path,
    #                                                       input_arrays,
    #                                                       output_arrays)
# ==== FROM save model
    with tf.Session() as sess:
        model = tf.saved_model.load(sess, tags=['serve'], export_dir=saved_model_dir)
        concrete_func = model.signatures[
            tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY]
        concrete_func.inputs[0].set_shape([1, 256, 256, 3])
        converter = TFLiteConverter.from_concrete_functions([concrete_func])
        # converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
        # ==== 
        if FLAGS.converter_type == 'float':
            print('======================================')
            print('Post Training.')
            # tflite_path = tflite_path.replace('.tflite', '_float.tflite')
            # ==== not completely quanize, below command will gen hybrid (int8, float) model
            # converter.post_training_quantize = True
            # converter.optimizations = [tf.lite.Optimize.DEFAULT]
            # converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS, tf.lite.OpsSet.SELECT_TF_OPS]

        tflite_model = converter.convert()

        with open(tflite_path, 'wb') as tflite_f:
            tflite_f.write(tflite_model)
        print('***.tflite file has been saving to', tflite_path)



if __name__ == '__main__':
    # logging.basicConfig(
    #     filename=FLAGS.pb_path.replace('.pb', '_tflite.log'),
    #     level=logging.INFO
    # )
    tf.app.run()
