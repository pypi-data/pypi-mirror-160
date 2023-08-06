import os
import sys
import logging

# pylint: disable=invalid-name
logger = logging.getLogger("ModelLoad")

class ModelLoadException(Exception):
        """Model Load Exception"""
class ModelLoad:
    def __init__(self, path, device):
        self.path = path
        self.device = device

    def onnx(self):
        shape_dict  = {}
        dtype_dict  = {}
        # import onnx front
        from onnx import load
        # set network path
        num_file = len(self.path)
        if num_file == 1:
            # load the model from the path
            onnx_model = load(self.path[0])
            # configure the model input ,shape and type
            in_node = onnx_model.graph.input[0]
            input_name = in_node.name
            input_elem_type = in_node.type.tensor_type.elem_type
            input_dim       = in_node.type.tensor_type.shape.dim
            input_shape     = [d.dim_value if d.dim_value != 0 else 1 for d in input_dim]
            if input_elem_type == 1:
                input_dtype = "float32"
            elif input_elem_type == 2:
                input_dtype = "uint8"
            elif input_elem_type == 3:
                input_dtype = "int8"
            elif input_elem_type == 4:
                input_dtype = "uint16"
            elif input_elem_type == 5:
                input_dtype = "int16"
            elif input_elem_type == 6:
                input_dtype = "int32"
            elif input_elem_type == 7:
                input_dtype = "int64"
            else:
                print("undefine input type index:", input_elem_type)
                sys.exit(1)
            shape_dict.update({input_name: input_shape})
            dtype_dict.update({input_name: input_dtype})
        else:
            print("[ModelLoad]: Model File Number Err:", num_file)
            sys.exit(1)

        return onnx_model, shape_dict, dtype_dict


    def caffe(self):
        shape_dict = {}
        dtype_dict = {}
        from google.protobuf import text_format
        from caffe.proto import caffe_pb2 as pb
        init_net = pb.NetParameter()
        predict_net = pb.NetParameter()
        # set network path
        num_file = len(self.path)
        if num_file == 2:
            # load the model from the path
            if self.path[0].endswith(".caffemodel"):
                blob_file = self.path[0]  # [.caffemodel]
                proto_file = self.path[1] # [.prototxt]
            else:
                blob_file = self.path[1]  # [.caffemodel]
                proto_file = self.path[0] # [.prototxt]
            # step1: load blob
            with open(blob_file, "rb") as f:
                init_net.ParseFromString(f.read())
            # step2: load model
            with open(proto_file, "r") as f:
                text_format.Merge(f.read(), predict_net)
            if predict_net.input:# NetParameter
                input_name  = predict_net.input[0]
                input_dtype = "float32"
                input_shape = [s for s in predict_net.input_shape[0].dim]
                shape_dict.update({input_name: input_shape})
                dtype_dict.update({input_name: input_dtype})
            else: # LayerParameter
                for node in predict_net.layer:
                    if node.type == "Input":
                        input_name  = node.name
                        shape_dim   = node.input_param.shape[0].dim
                        input_shape = [s for s in node.input_param.shape[0].dim]
                        input_dtype = "float32"
                        shape_dict.update({input_name: input_shape})
                        dtype_dict.update({input_name: input_dtype})
        else:
            print("[ModelLoad]: Model File Number Err:", num_file)
            sys.exit(1)
        return init_net, predict_net, shape_dict, dtype_dict

    def tf(self):
        shape_dict = {}
        dtype_dict = {}
        # Tensorflow imports
        # pylint: disable=C0415
        import tensorflow as tf
        import tvm.relay.testing.tf as tf_testing
        # set network path
        num_file = len(self.path)
        if num_file == 1:
            # load the model from the path
            if self.path[0].endswith(".pb"):
                with tf.io.gfile.GFile(self.path[0], "rb") as tf_graph:
                    content = tf_graph.read()

                graph_def = tf.compat.v1.GraphDef()
                graph_def.ParseFromString(content)
                graph_def = tf_testing.ProcessGraphDefParam(graph_def)

                for node in graph_def.node:
                    if node.op == "Placeholder":
                        input_name  = node.name
                        for s in node.attr['shape'].shape.dim:
                            if s.size == -1:
                                s.size=1
                        #input_shape = [s.size if s.size != -1 else 1 for s in node.attr['shape'].shape.dim]
                        input_shape = [s.size for s in node.attr['shape'].shape.dim]
                        input_elem_type = node.attr['dtype'].type
                        if input_elem_type == 1:
                            input_dtype = "float32"
                        elif input_elem_type == 2:
                            input_dtype = "double"
                        elif input_elem_type == 3:
                            input_dtype = "int32"
                        elif input_elem_type == 4:
                            input_dtype = "uint8"
                        elif input_elem_type == 5:
                            input_dtype = "int16"
                        elif input_elem_type == 6:
                            input_dtype = "int8"
                        elif input_elem_type == 9:
                            input_dtype = "int64"
                        else:
                            print("undefine input type index:", input_elem_type)
                            sys.exit(1)

                        shape_dict.update({input_name: input_shape})
                        dtype_dict.update({input_name: input_dtype})
        return graph_def, shape_dict, dtype_dict

    def _decode_type(self, n):
        _tflite_m = {
                0: "float32",
                1: "float16",
                2: "int32",
                3: "uint8",
                4: "int64",
                5: "string",
                6: "bool",
                7: "int16",
                8: "complex64",
                9: "int8",
        }
        return _tflite_m[n]

    def tflite(self):
        shape_dict = {}
        dtype_dict = {}
        # pylint: disable=C0415
        import tflite.Model as model
        # set network path
        num_file = len(self.path)
        if num_file == 1:
            if self.path[0].endswith(".tflite"):
                with open(self.path[0], "rb") as tf_graph:
                    content = tf_graph.read()
                # tflite.Model.Model is tflite.Model in 1.14 and 2.1.0
                try:
                    tflite_model = model.Model.GetRootAsModel(content, 0)
                except AttributeError:
                    tflite_model = model.GetRootAsModel(content, 0)
                try:
                    version = tflite_model.Version()
                    logger.debug("tflite version %s", version)
                except Exception:
                    ModelLoadException("input file not tflite")
                if version != 3:
                    ModelLoadException("input file not tflite version 3")
                logger.debug("parse TFLite model and convert into Relay computation graph")
        subgraph_count = tflite_model.SubgraphsLength()
        assert subgraph_count > 0
        for subgraph_index in range(subgraph_count):
            subgraph = tflite_model.Subgraphs(subgraph_index)
            inputs_count = subgraph.InputsLength()
            assert inputs_count >= 1
            for input_index in range(inputs_count):
                input_ = subgraph.Inputs(input_index)
                assert subgraph.TensorsLength() > input_
                tensor = subgraph.Tensors(input_)
                input_shape = tuple(tensor.ShapeAsNumpy())
                tensor_type = tensor.Type()
                input_name = tensor.Name().decode("utf8")
                shape_dict[input_name] = input_shape
                dtype_dict[input_name] = self._decode_type(tensor_type)
        return tflite_model, shape_dict, dtype_dict
