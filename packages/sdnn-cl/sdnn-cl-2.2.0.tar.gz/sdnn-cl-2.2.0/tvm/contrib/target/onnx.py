# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
# pylint: disable=invalid-name, import-self, len-as-condition, unused-argument, too-many-lines, redefined-builtin
"""Relay to ONNX codegen """

import os
import struct
import copy
import numpy
import onnx
import onnx.utils
from onnx import numpy_helper, OperatorSetIdProto, defs
from onnx import TensorProto
import tvm
from tvm import relay
import tvm._ffi
from tvm.relay.expr_functor import ExprVisitor
from tvm.relay.ty import TupleType, TensorType

#*BEGIN*#
## Add "relay.ext.to_onnx" function for SlimAI codegen
## data: 21-10-13
from tvm import nd as _nd, autotvm, register_func
from tvm.runtime import _ffi_api
from tvm.relay import expr as _expr
import tvm.contrib.target.slimai as slimai

slimai_onnx = False # produce normal onnx as default
##*END*

ONNX_OPSET_VERSONS_SUPPORTED = [11]


def run_onnx_optimizer(onnx_model):
    """Run ONNX's optimization routines.

    ONNX Optimizer was moved to an external library in
    version 1.9.  Attempt to use the optimizer in onnx if
    it is available, fall back to the standalone
    onnxoptimizer otherwise, and return the model
    unoptimized if neither are available.

    """
    # try:
    #     onnx_polish_model = onnx.utils.polish_model
    # except AttributeError:
    #     pass
    # else:
    #     return onnx_polish_model(onnx_model)

    try:
        # pylint: disable=import-outside-toplevel
        import onnxoptimizer
    except ImportError:
        pass
    else:
        return onnxoptimizer.optimize(onnx_model)

    #*BEGIN*#
    ## fix the bug "name 'model' is not defined" when the onnxoptimizer not install
    ## data: 21-10-26
    return onnx_model
    ###*END*


def tvm_array_to_list(arr):
    return tuple(x.value for x in arr)


def get_onnx_version():
    return onnx.__version__


def get_node_shape(node):
    return tuple("Any" if isinstance(i, tvm.tir.Any) else int(i) for i in node.shape)


def infer_type(node):
    """A method to infer the type of a relay expression."""
    mod = tvm.IRModule.from_expr(node)
    mod = relay.transform.InferType()(mod)
    entry = mod["main"]
    return entry if isinstance(node, relay.Function) else entry.body


def call_node_infer_type(node):
    """infer the output types of call node"""
    infer_out = infer_type(node)
    out_type = infer_out._checked_type_
    if isinstance(out_type, TensorType):
        types = [out_type]
    elif isinstance(out_type, TupleType):
        types = list(out_type.fields)
    else:
        raise RuntimeError(
            "Unsupported output type %s in operator %s" % (type(out_type), node.op.nae)
        )

    return types


def add_input(data, name, prefix, model_container):
    input_name = "{}_{}".format(prefix, name)
    dtype = onnx.mapping.NP_TYPE_TO_TENSOR_TYPE[data.dtype]
    tensor_value_info = onnx.helper.make_tensor_value_info(input_name, dtype, shape=data.shape)
    model_container.add_inputs([tensor_value_info])
    data_tensor = numpy_helper.from_array(data, input_name)
    model_container.add_initializers([data_tensor])
    return input_name


class OpConverter(object):
    """Operator converter Base Class."""

    @classmethod
    def convert_attributes(cls, attrs):
        """convert Relay attributes to ONNX attributes.
        The derived classes should implement this method
        if attributes are required by the operator
        otherwise by default no attributes are passed
        """
        return {}

    @classmethod
    def convert(cls, node_entry, model_container, node_dict):
        attrs = cls.convert_attributes(node_entry["relay_node"].attrs)
        onnx_node = onnx.helper.make_node(
            cls.__name__, node_entry["input_names"], node_entry["output_names"], **attrs
        )
        model_container.add_nodes([onnx_node])


def rename(op_name):
    """This method creates dynamic operator of name op_name with empty attributes"""
    return type(op_name, (OpConverter,), {})


class Reshape(object):
    """Operator converter for Reshape."""

    @classmethod
    def convert(cls, node_entry, model_container, node_dict):
        """Converts Relay operator Reshape to ONNX operator.
        Relay operator accepts shape as attribute but ONNX operator
        accepts it as a input.
        """
        name = node_entry["name"]
        shape = numpy.asarray(
            [a.value for a in node_entry["relay_node"].attrs.newshape], dtype=numpy.int64
        )

        input_names = [
            node_entry["input_names"][0],
            add_input(shape, name, "shape", model_container),
        ]

        node = onnx.helper.make_node(cls.__name__, input_names, node_entry["output_names"])
        model_container.add_nodes([node])


class Conv(OpConverter):
    """Operator converter for Conv."""

    @classmethod
    def convert_attributes(cls, attrs):
        return {
            "group": attrs.get_int("groups"),
            "pads": attrs.get_int_tuple("padding"),
            "strides": attrs.get_int_tuple("strides"),
            "dilations": attrs.get_int_tuple("dilation"),
            "kernel_shape": attrs.get_int_tuple("kernel_size"),
        }


##*BEGIN*#
## Add ConvTranspose 1D and 3D input convert support
## data: 21-12-09
class ConvTranspose(OpConverter):
    """Operator converter for ConvTranspose."""

    @classmethod
    def convert_attributes(cls, attrs):
        return {
            "group": attrs.get_int("groups"),
            "pads": attrs.get_int_list("padding"),
            "strides": attrs.get_int_list("strides"),
            "dilations": attrs.get_int_list("dilation"),
            "kernel_shape": attrs.get_int_list("kernel_size"),
            "output_padding": attrs.get_int_list("output_padding"),
        }

    @classmethod
    def convert(cls, node_entry, model_container, node_dict):
        attrs = cls.convert_attributes(node_entry["relay_node"].attrs)
        if attrs["pads"] == [0]:
            attrs["pads"] = None

        onnx_node = onnx.helper.make_node(
            cls.__name__, node_entry["input_names"], node_entry["output_names"], **attrs
        )
        model_container.add_nodes([onnx_node])
##*END*

##*BEGIN*#
## fix some issue form tvm convert test
## data: 21-12-23
class MaxPool(OpConverter):
    """Operator converter for MaxPool."""

    @classmethod
    def convert_attributes(cls, attrs):
        ceil_mode = 1 if attrs.ceil_mode else 0
        ori_pads = attrs.get_int_tuple("padding")
        pads = [0] * len(ori_pads)
        for i in range(len(ori_pads)):
            pads[i] = ori_pads[i]
        strides = attrs.get_int_tuple("strides")
        # xnnc does not handle ceil_mode correctly, workaround
        global slimai_onnx
        if slimai_onnx and ceil_mode == 1:
            for i in range(len(strides)):
                pads[len(strides)+i] += strides[i] - 1
            ceil_mode = 0
        return {
            "pads": pads,
            "strides": attrs.get_int_tuple("strides"),
            "kernel_shape": attrs.get_int_tuple("pool_size"),
            "ceil_mode": ceil_mode,
            "dilations": attrs.get_int_tuple("dilation"),
        }
##*END*


class Transpose(OpConverter):
    """Operator converter for Transpose."""

    @classmethod
    def convert_attributes(cls, attrs):
        return {"perm": attrs.get_int_tuple("axes")} if attrs["axes"] else {}


class MatMul(OpConverter):
    """Operator converter for MatMul."""

    @classmethod
    def convert(cls, node_entry, model_container, node_dict):
        inter_output_name = "inter{}".format(node_entry["name"])
        transpose_node = onnx.helper.make_node(
            Transpose.__name__, [node_entry["input_names"][1]], [inter_output_name], perm=(1, 0)
        )
        model_container.add_nodes([transpose_node])

        inputs = [node_entry["input_names"][0], inter_output_name]
        matmul_node = onnx.helper.make_node(cls.__name__, inputs, node_entry["output_names"])
        model_container.add_nodes([matmul_node])


class Flatten(OpConverter):
    """Operator converter for Flatten."""

    @classmethod
    def convert_attributes(cls, attrs):
        return {
            "axis": 1,
        }


class BatchNormalization(OpConverter):
    """Operator converter for BatchNormalization."""

    @classmethod
    def convert_attributes(cls, attrs):
        return {
            "epsilon": float(attrs.get_str("epsilon")),
            "axis": float(attrs.get_int("axis")),
        }

    @classmethod
    def convert(cls, node_entry, model_container, node_dict):
        """Converts Relay operator batch_norm to ONNX operator.
        Relay operator has property axis to handle data in NHWC format.
        """
        attrs = cls.convert_attributes(node_entry["relay_node"].attrs)
        transpose_out_name = node_entry["input_names"][0]
        inter_output_names = [node_entry["output_names"][0]]
        # axis==3 means channel is specified along the 3rd axis
        if attrs["axis"] == 3:
            transpose_out_name = "transpose_{}".format(node_entry["name"])
            node_transposed = onnx.helper.make_node(
                Transpose.__name__,
                [node_entry["input_names"][0]],
                [transpose_out_name],
                perm=[0, 3, 1, 2],
            )
            model_container.add_nodes([node_transposed])
            inter_output_names = ["batch_norm_{}".format(node_entry["name"])]

        input_names = [transpose_out_name] + node_entry["input_names"][1:]
        batch_norm_node = onnx.helper.make_node(
            cls.__name__, input_names, inter_output_names, epsilon=attrs["epsilon"]
        )
        model_container.add_nodes([batch_norm_node])

        if attrs["axis"] == 3:
            node_transposed = onnx.helper.make_node(
                Transpose.__name__,
                inter_output_names,
                [node_entry["output_names"][0]],
                perm=[0, 2, 3, 1],
            )
            model_container.add_nodes([node_transposed])


class Dropout(OpConverter):
    """Operator converter for Dropout."""

    @classmethod
    def convert_attributes(cls, attrs):
        return {
            "ratio": float(attrs.get_str("rate")),
        }


class AveragePool(MaxPool):
    """Operator converter for AveragePool."""

    @classmethod
    def convert_attributes(cls, attrs):
        return {
            "pads": attrs.get_int_tuple("padding"),
            "strides": attrs.get_int_tuple("strides"),
            "kernel_shape": attrs.get_int_tuple("pool_size"),
            "ceil_mode": 1 if attrs.ceil_mode else 0,
            "count_include_pad": 1 if attrs.count_include_pad else 0,
        }


class Concat(OpConverter):
    """Operator converter for Concat."""

    @classmethod
    def convert_attributes(cls, attrs):
        return {
            "axis": attrs.get_int("axis"),
        }


class BiasAdd(OpConverter):
    """Operator converter for BiasAdd."""

    @classmethod
    def convert(cls, node_entry, model_container, node_dict):
        input_node = node_dict[node_entry["inputs"][0]]
        assert len(input_node) == 1, "input node_entry can not be a Tuple"
        input_node = input_node[0]
        data_ndim = len(input_node["types"][0].shape)
        axis = node_entry["relay_node"].attrs.get_int("axis")
        if axis < 0:
            axis = axis + data_ndim
        new_axes = data_ndim - axis - 1
        if new_axes:
            inter_output_name = "inter{}".format(node_entry["name"])
            unsqueeze_node = onnx.helper.make_node(
                "Unsqueeze",
                [node_entry["input_names"][1]],
                [inter_output_name],
                axes=tuple(range(1, new_axes + 1)),
            )
            model_container.add_nodes([unsqueeze_node])
        else:
            inter_output_name = node_entry["input_names"][1]

        inputs = [node_entry["input_names"][0], inter_output_name]
        matmul_node = onnx.helper.make_node("Add", inputs, node_entry["output_names"])
        model_container.add_nodes([matmul_node])

#*BEGIN*#
## add tvm max op and sum op convert to onnx support
## data: 21-10-19
class Reduce(OpConverter):
    """Operator converter for Reduce class operator."""

    @classmethod
    def convert(cls, node_entry, model_container, node_dict):
        input_node = node_dict[node_entry["inputs"][0]]
        assert len(input_node) == 1, "input node can not be a Tuple"
        input_node = input_node[0]
        shape = input_node["types"][0].shape
        axis = node_entry["relay_node"].attrs.axis
        axis = list(range(len(shape))) if not axis else tvm_array_to_list(axis)
        exclude = 0 if not bool(node_entry["relay_node"].attrs.exclude) else 1
        keepdims = 0 if not bool(node_entry["relay_node"].attrs.keepdims) else 1
        if exclude:
            all_axis = list(range(len(shape)))
            axis = set(all_axis) - set(axis)

        node = onnx.helper.make_node(
            cls.__name__,
            node_entry["input_names"],
            node_entry["output_names"],
            axes=axis,
            keepdims=keepdims,
        )
        model_container.add_nodes([node])

class ReduceMax(Reduce):
    """ Operator converter for ReduceMax"""

class ReduceMin(Reduce):
    """ Operator converter for ReduceMin"""

class ReduceSum(Reduce):
    """ Operator converter for ReduceSum"""

class ReduceMean(Reduce):
    """ Operator converter for ReduceMean"""

class ReduceProd(Reduce):
    """ Operator converter for ReduceProd"""

class ReduceLogSumExp(Reduce):
    """ Operator converter for ReduceLogSumExp"""
##*END*

class Pad(OpConverter):
    """Operator converter for Pad."""

    @classmethod
    def convert_attributes(cls, attrs):
        before = []
        after = []
        for axis_pads in attrs.pad_width:
            before.append(axis_pads[0])
            after.append(axis_pads[1])
        pads = before + after
        pads = numpy.asarray(pads, dtype=pads[0].dtype)
        return {
            "pads": pads,
            "mode": attrs.get_str("pad_mode"),
        }

    @classmethod
    def convert(cls, node_entry, model_container, node_dict):
        """Converts Relay operator Pad to ONNX operator.
        Relay operator accepts pads as attribute but ONNX operator
        accepts it as a input.
        """
        attrs = cls.convert_attributes(node_entry["relay_node"].attrs)

        name = node_entry["name"]
        pad_data = numpy.asarray(attrs["pads"], dtype=attrs["pads"][0].dtype).astype(numpy.int64)

        input_names = [
            node_entry["input_names"][0],
            add_input(pad_data, name, "pads", model_container),
            node_entry["input_names"][1],
        ]

        node = onnx.helper.make_node(
            cls.__name__, input_names, node_entry["output_names"], mode=attrs["mode"]
        )
        model_container.add_nodes([node])


class Softmax(OpConverter):
    """Operator converter for SoftMax."""

    @classmethod
    def convert_attributes(cls, attrs):
        return {
            "axis": attrs.axis,
        }


class Squeeze(OpConverter):
    """Operator converter for Squeeze."""

    @classmethod
    def convert_attributes(cls, attrs):
        return {
            "axes": attrs.axis,
        }

    @classmethod
    def convert(cls, node_entry, model_container, node_dict):
        input_node = node_dict[node_entry["inputs"][0]]
        assert len(input_node) == 1, "input node can not be a Tuple"
        input_node = input_node[0]
        shape = input_node["types"][0].shape
        axis = node_entry["relay_node"].attrs.get_int("axis")
        if not axis:
            axis = []
            for axis_idx, val in enumerate(shape):
                if val.value == 1:
                    axis.append(axis_idx)
        else:
            axis = node_entry["relay_node"].attrs.get_int_tuple("axis")

        node = onnx.helper.make_node(
            cls.__name__, node_entry["input_names"], node_entry["output_names"], axes=axis
        )
        model_container.add_nodes([node])


class Slice(OpConverter):
    """Operator converter for Slice."""

    ##*BEGIN*#
    ## Add slice op axes input support, fix tvm load onnx slice op issue:
    ## tvm not handle the case that axes don't like [0, 1, 2, ..., N].
    ## data: 21-11-18
    @classmethod
    def convert_attributes(cls, attrs):
        if attrs.axes is None:
            axes = list(range(len(attrs.begin)))
        else:
            axes = attrs.get_int_tuple("axes")

        return {
            "starts": attrs.get_int_tuple("begin"),
            "ends": attrs.get_int_tuple("end"),
            "steps": attrs.get_int_tuple("strides"),
            "axes": axes,
            "slice_mode": attrs.get_str("slice_mode"),
        }

    @classmethod
    def convert(cls, node_entry, model_container, node_dict):
        attrs = cls.convert_attributes(node_entry["relay_node"].attrs)

        name = node_entry["name"]
        input_node = node_dict[node_entry["inputs"][0]]
        assert len(input_node) == 1, "input node can not be a Tuple"
        input_node = input_node[0]
        shape = input_node["types"][0].shape

        starts = list(attrs["starts"])
        ends = list(attrs["ends"])
        steps = list(attrs["steps"])
        attr_axes = list(attrs["axes"])
        starts += [0] * (len(shape) - len(starts))

        ends_all_axes = list(shape)
        for i in attr_axes:
            ends_all_axes[i] = ends.pop(0)
        ends = ends_all_axes

        axes = list(range(len(shape)))

        if attrs["slice_mode"] == "size":
            ends = [
                starts[i] + (shape[i] + 1 if ends[i] < 0 else ends[i]) for i in range(len(shape))
            ]
            steps = [1] * len(shape)
        else:
            steps_all_axes = [1] * len(shape)
            for i in attr_axes:
                if len(steps) == 0:
                    steps_all_axes[i] = 1
                else:
                    steps_all_axes[i] = steps.pop(0)
            steps = steps_all_axes
    ##*END*

        starts = numpy.asarray(starts).astype(numpy.int64)
        ends = numpy.asarray(ends).astype(numpy.int64)
        axes = numpy.asarray(axes).astype(numpy.int64)
        steps = numpy.asarray(steps).astype(numpy.int64)

        input_names = []
        input_names.append(add_input(starts, name, "starts", model_container))
        input_names.append(add_input(ends, name, "ends", model_container))
        input_names.append(add_input(axes, name, "axes", model_container))
        input_names.append(add_input(steps, name, "steps", model_container))

        input_names = [node_entry["input_names"][0]] + input_names

        #*BEGIN*#
        ## convert to "Custom_Slice" if any steps is 2 or above
        ## data: 21-12-13
        global slimai_onnx
        if slimai_onnx and numpy.amax(steps) > 1:
            slice_attrs = {
                "starts": starts,
                "ends": ends,
                "axes": axes,
                "steps": steps,
            }
            slice_inputs = []
            slice_inputs.append(add_input(starts.astype(numpy.float32), name, "starts", model_container))
            slice_inputs.append(add_input(ends.astype(numpy.float32), name, "ends", model_container))
            slice_inputs.append(add_input(axes.astype(numpy.float32), name, "axes", model_container))
            slice_inputs.append(add_input(steps.astype(numpy.float32), name, "steps", model_container))
            slice_inputs = [node_entry["input_names"][0]] + slice_inputs

            slice_node = onnx.helper.make_node("Custom_Slice", slice_inputs, node_entry["output_names"], **slice_attrs)
        else:
            slice_node = onnx.helper.make_node(cls.__name__, input_names, node_entry["output_names"])
        #*END*#

        model_container.add_nodes([slice_node])


class Split(OpConverter):
    """Operator converter for Split."""

    @classmethod
    def convert_attributes(cls, attrs):
        indices_or_sections = attrs["indices_or_sections"]

        if isinstance(indices_or_sections, (list, tvm.ir.container.Array)):
            indices_or_sections = attrs.get_int_tuple("indices_or_sections")
        if isinstance(indices_or_sections, tvm.ir.PrimExpr):
            indices_or_sections = indices_or_sections.value

        return {
            "indices_or_section": indices_or_sections,
            "axis": attrs.get_int("axis"),
        }

    @classmethod
    def convert(cls, node_entry, model_container, node_dict):
        attrs = cls.convert_attributes(node_entry["relay_node"].attrs)

        input_node = node_dict[node_entry["inputs"][0]]
        assert len(input_node) == 1, "input node can not be a Tuple"
        input_node = input_node[0]
        shape = get_node_shape(input_node["types"][0])

        indices_or_sect = attrs["indices_or_section"]
        axis = attrs["axis"]
        axis_length = shape[axis]

        if isinstance(indices_or_sect, int):
            split = [axis_length // indices_or_sect] * indices_or_sect
        else:
            split = []
            for i in range(len(indices_or_sect) + 1):
                if i == 0:
                    split.append(indices_or_sect[0])
                elif i == len(indices_or_sect):
                    split.append(axis_length - indices_or_sect[-1])
                else:
                    split.append(indices_or_sect[i] - indices_or_sect[i - 1])

        slice_node = onnx.helper.make_node(
            cls.__name__,
            node_entry["input_names"],
            node_entry["output_names"],
            split=split,
            axis=axis,
        )
        model_container.add_nodes([slice_node])


class LayoutTransform(OpConverter):
    """Operator converter for Layouttransform"""

    @classmethod
    def convert_attributes(cls, attrs):
        src_layout = attrs.get_str("src_layout")
        dst_layout = attrs.get_str("dst_layout")

        perm = [src_layout.index(c) for c in dst_layout]
        return {"perm": tuple(perm)}

    @classmethod
    def convert(cls, node_entry, model_container, node_dict):
        attrs = cls.convert_attributes(node_entry["relay_node"].attrs)
        onnx_node = onnx.helper.make_node(
            "Transpose", node_entry["input_names"], node_entry["output_names"], **attrs
        )
        model_container.add_nodes([onnx_node])


class Clip(OpConverter):
    """Operator converter for Clip."""

    @classmethod
    def convert_attributes(cls, attrs):
        return {"min": attrs.a_min, "max": attrs.a_max}

    @classmethod
    def convert(cls, node_entry, model_container, node_dict):
        attrs = cls.convert_attributes(node_entry["relay_node"].attrs)

        name = node_entry["name"]

        min_val = numpy.asarray(attrs["min"]).astype(numpy.float32)
        max_val = numpy.asarray(attrs["max"]).astype(numpy.float32)

        input_names = []
        input_names.append(add_input(min_val, name, "min", model_container))
        input_names.append(add_input(max_val, name, "max", model_container))

        input_names = [node_entry["input_names"][0]] + input_names

        node = onnx.helper.make_node(cls.__name__, input_names, node_entry["output_names"])
        model_container.add_nodes([node])


class Expand(OpConverter):
    """Operator converter for Expand_dims."""

    @classmethod
    def convert_attributes(cls, attrs):
        return {"axis": attrs.axis, "num_newaxis": attrs.num_newaxis}

    @classmethod
    def convert(cls, node_entry, model_container, node_dict):
        attrs = cls.convert_attributes(node_entry["relay_node"].attrs)

        name = node_entry["name"]

        input_node = node_dict[node_entry["inputs"][0]]
        assert len(input_node) == 1, "input node_entry can not be a Tuple"
        input_node = input_node[0]
        data_shape = input_node["types"][0].shape
        new_shape = list(data_shape)

        for _ in range(attrs["num_newaxis"]):
            new_shape.insert(attrs["axis"], 1)

        new_shape = numpy.asarray(new_shape).astype(numpy.int64)
        input_names = []
        input_names.append(add_input(new_shape, name, "shape", model_container))

        input_names = [node_entry["input_names"][0]] + input_names

        node = onnx.helper.make_node(cls.__name__, input_names, node_entry["output_names"])
        model_container.add_nodes([node])

##*BEGIN*#
## fix some issue form tvm convert test
## data: 21-12-23
class Unsqueeze(OpConverter):
    """Operator converter for Unsqueeze."""

    @classmethod
    def convert_attributes(cls, attrs):
        return {"axes": [attrs.axis]}


class ArgMax(OpConverter):
    """Operator converter for ArgMax."""

    @classmethod
    def convert_attributes(cls, attrs):
        return {
            "axis": int(attrs.axis[0]),
            "keepdims": 1 if attrs.keepdims else 0,
        }


class SpaceToDepth(OpConverter):
    """ Operator converter for SpaceToDepth."""

    @classmethod
    def convert_attributes(cls, attrs):
        return {
            "blocksize": attrs.block_size,
        }
##*END*

class ConstantOfShapeZeros(OpConverter):
    """Operator converter for ConstantOfShape."""

    @classmethod
    def convert_attributes(cls, attrs):
        return {"value": 0}

    @classmethod
    def convert(cls, node_entry, model_container, node_dict):
        attrs = cls.convert_attributes(node_entry["relay_node"].attrs)
        input_node = node_dict[node_entry["inputs"][0]]
        assert len(input_node) == 1, "input node can not be a Tuple"
        input_node = input_node[0]
        dtype = input_node["types"][0].dtype

        name = node_entry["name"]
        shape = [val.value for val in input_node["types"][0].shape]
        shape = numpy.asarray(shape).astype(numpy.int64)

        input_names = []
        input_names.append(add_input(shape, name, "shape", model_container))

        dtype = onnx.mapping.NP_TYPE_TO_TENSOR_TYPE[numpy.dtype(dtype)]
        tensor_value = onnx.helper.make_tensor("value", dtype, [1], [attrs["value"]])

        node = onnx.helper.make_node(
            "ConstantOfShape", input_names, node_entry["output_names"], value=tensor_value
        )
        model_container.add_nodes([node])


class ConstantOfShapeOnes(ConstantOfShapeZeros):
    """Operator converter for ConstantOfShape."""

    @classmethod
    def convert_attributes(cls, attrs):
        return {"value": 1}


class LRN(OpConverter):
    """Operator converter for LRN."""

    @classmethod
    def convert_attributes(cls, attrs):
        """axis attr is not supported as an argument in onnx.
        Onnx only supports axis=1 (channels)."""
        if attrs.get_int("axis") != 1:
            raise RuntimeError(
                "Unsupported axis %s in operator relay lrn operator. "
                "Only axis = 1 is supported by Onnx." % (attrs.get_int("axis"))
            )

        return {"alpha": attrs.alpha, "beta": attrs.beta, "bias": attrs.bias, "size": attrs.size}


class Cast(OpConverter):
    """Operator converter for Cast."""

    @classmethod
    def convert_attributes(cls, attrs):
        return {"to": onnx.mapping.NP_TYPE_TO_TENSOR_TYPE[numpy.dtype(attrs.dtype)]}


class Resize(OpConverter):
    """Operator converter for Resize."""

    @classmethod
    def convert_attributes(cls, attrs):
        method = attrs.get_str("method")
        if method == "nearest_neighbor":
            mode = b"nearest"
        elif "linear" in method:  # linear / bilinear
            mode = b"linear"
        elif "cubic" in method:  # cubic / bicubic
            mode = b"cubic"
        else:
            raise RuntimeError("Unsupported method %s in operator Resize" % method)

        coord_trans = attrs.get_str("coordinate_transformation_mode")
        if coord_trans == "half_pixel":
            coord_trans = b"half_pixel"
        elif coord_trans == "align_corners":
            coord_trans = b"align_corners"
        elif coord_trans == "asymmetric":
            coord_trans = b"asymmetric"
        else:
            raise RuntimeError(
                "Unsupported coordinate transform mode %s in operator Resize" % coord_trans
            )

        #*BEGIN*#
        ## bugfix: resize-11 nearest_mode only exist when mode attr is nearest, and have a deafault value "round_prefer_floor"
        ## data: 21-10-30
        if method == "nearest_neighbor":
            rounding_method = attrs.get_str("rounding_method")
            if rounding_method == "round":
                rounding_method = b"round_prefer_ceil"
            elif rounding_method == "floor":
                rounding_method = b"floor"
            elif rounding_method == "ceil":
                rounding_method = b"ceil"
            else:
                rounding_method = b"round_prefer_floor"
        else:
            # although its only valid in nearest mode, this attribute still needs to be there
            # let the backend to handle it
            rounding_method = attrs.get_str("rounding_method")
        ##*END*

        size = attrs.get_int_tuple("size")

        return {
            "mode": mode,
            "coord_trans": coord_trans,
            "size": size,
            "nearest_mode": rounding_method,
        }

    @classmethod
    def convert(cls, node_entry, model_container, node_dict):
        attrs = cls.convert_attributes(node_entry["relay_node"].attrs)

        name = node_entry["name"]
        input_node = node_dict[node_entry["inputs"][0]]
        assert len(input_node) == 1, "input node can not be a Tuple"
        input_node = input_node[0]
        input_shape = input_node["types"][0].shape

        # (TBD) needed in opset 11
        roi = [0] * len(input_shape) + [1] * len(input_shape)
        roi_array = numpy.asarray(roi).astype(numpy.float32)
        roi_node = add_input(roi_array, name, "roi", model_container)

        out_size = attrs["size"]

        # (onnx) rank of scale / size must match rank of X
        # relay size node contains only spatial dimensions
        # pad with 1s to match rank
        match_rank_pad = len(input_shape) - len(out_size)
        out_size_full_rank = input_shape[:match_rank_pad] + list(out_size)
        out_size_array = numpy.asarray(out_size_full_rank).astype(numpy.int64)

        input_size_array = numpy.asarray(list(input_shape)).astype(numpy.int64)

        scale_array = numpy.divide(out_size_array, input_size_array).astype(numpy.float32)
        scale_node = add_input(scale_array, name, "scales", model_container)

        input_names = [node_entry["input_names"][0], roi_node, scale_node]

        resize_node = onnx.helper.make_node(
            cls.__name__,
            input_names,
            node_entry["output_names"],
            mode=attrs["mode"],
            coordinate_transformation_mode=attrs["coord_trans"],
            nearest_mode=attrs["nearest_mode"],
        )
        model_container.add_nodes([resize_node])

#*BEGIN*#
## Add some tvm op convert support by conv attr.
## data: 21-10-28
class LeakyRelu(OpConverter):
    """Operator converter for LeakyRelu."""

    @classmethod
    def convert_attributes(cls, attrs):
        return {
            "alpha": attrs.alpha,
        }


class InstanceNormalization(OpConverter):
    """ Operator converter for InstanceNormalization."""

    @classmethod
    def convert_attributes(cls, attrs):
        return {"epsilon": attrs.epsilon}


class DepthToSpace(OpConverter):
    """ Operator converter for DepthToSpace."""

    @classmethod
    def convert_attributes(cls, attrs):
        return {
            "mode": attrs.get_str("mode"),
            "blocksize": attrs.block_size,
        }


class ExpandShape(OpConverter):
    """ Operator converter for Expand."""

    @classmethod
    def convert(cls, node_entry, model_container, node_dict):
        attrs = cls.convert_attributes(node_entry["relay_node"].attrs)

        name = node_entry["name"]

        shape_node = node_dict[node_entry["inputs"][1]]
        assert len(shape_node) == 1, "input node_entry can not be a Tuple"
        shape_node = shape_node[0]
        data_shape = shape_node["types"][0].shape
        new_shape = list(data_shape)

        new_shape = numpy.asarray(new_shape).astype(numpy.int64)
        input_names = []
        input_names.append(add_input(new_shape, name, "shape", model_container))
        input_names = [node_entry["input_names"][0]] + input_names

        node = onnx.helper.make_node("Expand", input_names, node_entry["output_names"])
        model_container.add_nodes([node])


class ScatterElements(OpConverter):
    """ Operator converter for ScatterElements."""

    @classmethod
    def convert_attributes(cls, attrs):
        return {
            "axis": int(attrs.axis),
        }


class ScatterND(OpConverter):
    """ Operator converter for ScatterND."""

    @classmethod
    def convert(cls, node_entry, model_container, node_dict):
        inter_output_name = "inter{}".format(node_entry["name"])

        indices_node = node_dict[node_entry["inputs"][1]]
        assert len(indices_node) == 1, "input node_entry can not be a Tuple"
        indices_node = indices_node[0]
        try:
            data_shape = indices_node["types"][0].shape
        except:
            # for constant node
            data_shape = indices_node["inputs"][0].data.shape
        indices_dim = len(data_shape)
        axes = list(range(indices_dim))

        transpose_node = onnx.helper.make_node(
            Transpose.__name__, [node_entry["input_names"][1]], [inter_output_name], perm=tuple(axes[1:] + axes[:1])
        )
        model_container.add_nodes([transpose_node])

        inputs = [node_entry["input_names"][0], inter_output_name, node_entry["input_names"][2]]
        scatternd_node = onnx.helper.make_node(cls.__name__, inputs, node_entry["output_names"])
        model_container.add_nodes([scatternd_node])

##*END*


##*BEGIN*#
## add some tvm op convert support and fix bug when model has two outputs
## data: 21-11-02
class ExpandBroadcastTo(OpConverter):
    """ Operator converter for tvm broadcast_to."""

    @classmethod
    def convert(cls, node_entry, model_container, node_dict):
        name = node_entry["name"]

        shape = node_entry["relay_node"].attrs.shape
        shape_list = tvm_array_to_list(shape)
        new_shape = numpy.asarray(shape_list).astype(numpy.int64)
        input_names = []
        input_names.append(add_input(new_shape, name, "shape", model_container))
        input_names = [node_entry["input_names"][0]] + input_names

        node = onnx.helper.make_node("Expand", input_names, node_entry["output_names"])
        model_container.add_nodes([node])


class BatchMatMul(OpConverter):
    """Operator converter for MatMul."""

    # TODO: the transpose_a and transpose_b not used
    @classmethod
    def convert_attributes(cls, attrs):
        return {
            "transpose_a": int(attrs.transpose_a),
            "transpose_b": int(attrs.transpose_b),
        }

    @classmethod
    def convert(cls, node_entry, model_container, node_dict):
        attrs = cls.convert_attributes(node_entry["relay_node"].attrs)

        inter_output_name = "inter{}".format(node_entry["name"])
        transpose_node = onnx.helper.make_node(
            Transpose.__name__, [node_entry["input_names"][1]], [inter_output_name], perm=(0, 2, 1)
        )
        model_container.add_nodes([transpose_node])

        input_names = [node_entry["input_names"][0], inter_output_name]

        node = onnx.helper.make_node("MatMul", input_names, node_entry["output_names"])
        model_container.add_nodes([node])


class Gather(OpConverter):
    """Operator converter for Gather."""

    @classmethod
    def convert_attributes(cls, attrs):
        try:
            axis = int(attrs.axis)
        except:
            axis = 0
        return {
            "axis": axis,
        }


class Tile(OpConverter):
    """Operator converter for Tile."""

    @classmethod
    def convert(cls, node_entry, model_container, node_dict):
        name = node_entry["name"]

        tiles_input = node_entry["relay_node"].attrs.reps
        tiles_list = tvm_array_to_list(tiles_input)
        tiles = numpy.asarray(tiles_list).astype(numpy.int64)
        input_names = []
        input_names.append(add_input(tiles, name, "tiles", model_container))
        input_names = [node_entry["input_names"][0]] + input_names

        node = onnx.helper.make_node(cls.__name__, input_names, node_entry["output_names"])
        model_container.add_nodes([node])


class ConstantZeros(OpConverter):
    """Operator converter for tvm zeros."""

    @classmethod
    def convert_attributes(cls, attrs):
        return {"value": 0, "dtype": attrs.dtype}

    @classmethod
    def convert(cls, node_entry, model_container, node_dict):
        name = node_entry["name"]
        attrs = cls.convert_attributes(node_entry["relay_node"].attrs)

        dtype = attrs["dtype"]
        shape = node_entry["types"]
        shape_array = shape[0].shape
        shape_list = tvm_array_to_list(shape_array)
        shape = numpy.asarray(shape_list).astype(numpy.int64)

        input_names = []
        input_names.append(add_input(shape, name, "shape", model_container))

        dtype = onnx.mapping.NP_TYPE_TO_TENSOR_TYPE[numpy.dtype(dtype)]
        tensor_value = onnx.helper.make_tensor("value", dtype, [1], [attrs["value"]])

        node = onnx.helper.make_node(
            "ConstantOfShape", input_names, node_entry["output_names"], value=tensor_value
        )
        model_container.add_nodes([node])


# TODO: this op can't to be the zhe last node of the graph, because the the output is dynamic shape
class NonZero(OpConverter):
    """Operator converter for tvm NonZero."""

    @classmethod
    def convert(cls, node_entry, model_container, node_dict):
        inter_output_name = "inter{}".format(node_entry["name"])
        attrs = cls.convert_attributes(node_entry["relay_node"].attrs)
        onnx_node = onnx.helper.make_node(
            cls.__name__, node_entry["input_names"][0], [inter_output_name]
        )
        model_container.add_nodes([onnx_node])

        transpose_node = onnx.helper.make_node(
            Transpose.__name__, [inter_output_name], node_entry["output_names"], perm=(1, 0)
        )
        model_container.add_nodes([transpose_node])


class TopK(OpConverter):
    """Operator converter for TopK."""

    @classmethod
    def convert_attributes(cls, attrs):
        # TODO: only support largest attr
        return {"axis": attrs.axis, "largest": 1}

    @classmethod
    def convert(cls, node_entry, model_container, node_dict):
        attrs = cls.convert_attributes(node_entry["relay_node"].attrs)
        name = node_entry["name"]

        k_input = node_entry["relay_node"].attrs.k
        k = numpy.asarray([k_input.value]).astype(numpy.int64)
        input_names = []
        input_names.append(add_input(k, name, "k", model_container))
        input_names = [node_entry["input_names"][0]] + input_names

        node = onnx.helper.make_node(cls.__name__, input_names, node_entry["output_names"],  **attrs)
        model_container.add_nodes([node])


# The Upsample op has deprecated since version 10
class Upsample(OpConverter):
    """Operator converter for tvm Upsample."""

    @classmethod
    def convert_attributes(cls, attrs):
        return {"scales": [1.0, 1.0, attrs.scale_h, attrs.scale_w]}

    @classmethod
    def convert(cls, node_entry, model_container, node_dict):
        name = node_entry["name"]
        attrs = cls.convert_attributes(node_entry["relay_node"].attrs)

        scales_list = attrs["scales"]
        scales = numpy.asarray(scales_list).astype(numpy.float32)
        input_names = []
        input_names.append(add_input(scales, name, "scales", model_container))
        input_names = [node_entry["input_names"][0]] + input_names

        node = onnx.helper.make_node(cls.__name__, input_names, node_entry["output_names"])
        model_container.add_nodes([node])
##*END*

##*BEGIN*#
## Unsample operator not support in onnx 11 operator sets,using resize to replace
## upsample operator as follow to realize
## data: 22-2-14
class UpsampleResize(OpConverter):
    """Operator converter for Resize to replace Upsample."""

    @classmethod
    def convert_attributes(cls, attrs):
        #scale_h', 'scale_w', 'layout', 'method', 'align_corners
        method = attrs.get_str("method")
        if method == "nearest_neighbor":
            mode = b"nearest"
        elif "linear" in method:  # linear / bilinear
            mode = b"linear"
        elif "cubic" in method:  # cubic / bicubic
            mode = b"cubic"
        else:
            raise RuntimeError("Unsupported method %s in operator Resize" % method)

        coord_trans = b"align_corners"
        rounding_method = b"floor"

        scale_h = attrs.get_str("scale_h")
        scale_w = attrs.get_str("scale_w")
        scale = [1.0, 1.0, scale_h, scale_w]

        return {
            "mode": mode,
            "coord_trans": coord_trans,
            "scale": scale,
            "nearest_mode": rounding_method,
        }

    @classmethod
    def convert(cls, node_entry, model_container, node_dict):
        attrs = cls.convert_attributes(node_entry["relay_node"].attrs)

        name = node_entry["name"]
        input_node = node_dict[node_entry["inputs"][0]]
        assert len(input_node) == 1, "input node can not be a Tuple"

        scale_array = numpy.asarray(attrs["scale"]).astype(numpy.float32)
        scale_node = add_input(scale_array, name, "scales", model_container)

        input_names = [node_entry["input_names"][0], '', scale_node]

        resize_node = onnx.helper.make_node(
            "Resize",
            input_names,
            node_entry["output_names"],
            mode=attrs["mode"],
            coordinate_transformation_mode=attrs["coord_trans"],
            nearest_mode=attrs["nearest_mode"],
        )
        model_container.add_nodes([resize_node])
##*END*


##*BEGIN*#
## add support for If and NonMaxSuppression convert, and some other op.
## data: 21-11-20
class NonMaxSuppression(OpConverter):
    """ Operator converter for NonMaxSuppression."""

    @classmethod
    def convert(cls, node_entry, model_container, node_dict):
        attrs = cls.convert_attributes(node_entry["relay_node"].attrs)

        onnx_node = onnx.helper.make_node(
            cls.__name__, node_entry["input_names"], [node_entry["output_names"][0]], **attrs
        )
        model_container.add_nodes([onnx_node])

        shape_output_name = "shape_{}".format(node_entry["name"])
        shape_node = onnx.helper.make_node("Shape", [node_entry["output_names"][0]], [shape_output_name])
        model_container.add_nodes([shape_node])

        name = node_entry["name"] + "_scalar"

        starts = [0]
        ends = [1]
        steps = [1]
        axes = [0]
        starts = numpy.asarray(starts).astype(numpy.int64)
        ends = numpy.asarray(ends).astype(numpy.int64)
        axes = numpy.asarray(axes).astype(numpy.int64)
        steps = numpy.asarray(steps).astype(numpy.int64)
        input_names = []
        input_names.append(add_input(starts, name, "starts", model_container))
        input_names.append(add_input(ends, name, "ends", model_container))
        input_names.append(add_input(axes, name, "axes", model_container))
        input_names.append(add_input(steps, name, "steps", model_container))

        input_names = [shape_output_name] + input_names

        slice_output_name = "slice_{}".format(node_entry["name"])
        slice_node = onnx.helper.make_node("Slice", input_names, [slice_output_name])
        model_container.add_nodes([slice_node])

        dtype = onnx.mapping.NP_TYPE_TO_TENSOR_TYPE[numpy.dtype("int32")]

        cast_node = onnx.helper.make_node(
            "Cast", [slice_output_name],
            [node_entry["output_names"][1]],
            to=dtype
        )
        model_container.add_nodes([cast_node])


class CastLike(OpConverter):
    """ Operator converter for tvm cast_like."""

    @classmethod
    def convert(cls, node_entry, model_container, node_dict):
        input_node = node_dict[node_entry["inputs"][1]]
        assert len(input_node) == 1, "input node can not be a Tuple"
        input_node = input_node[0]
        try:
            dtype = input_node["types"][0].dtype
        except:
            dtype = input_node["inputs"][0].data.dtype
            dtype = onnx.mapping.NP_TYPE_TO_TENSOR_TYPE[numpy.dtype(dtype)]

        node = onnx.helper.make_node(
            "Cast", [node_entry["input_names"][0]],
            [node_entry["output_names"][0]],
            to=dtype
        )
        model_container.add_nodes([node])


class SliceLike(OpConverter):
    """Operator converter for tvm slice_like."""

    @classmethod
    def convert_attributes(cls, attrs):
        if attrs.axes is None:
            axes = None
        else:
            axes = attrs.get_int_tuple("axes")

        return {
            "axes": axes,
        }

    @classmethod
    def convert(cls, node_entry, model_container, node_dict):
        attrs = cls.convert_attributes(node_entry["relay_node"].attrs)

        name = node_entry["name"]
        input_node = node_dict[node_entry["inputs"][0]]
        assert len(input_node) == 1, "input node can not be a Tuple"
        input_node = input_node[0]
        input_shape = input_node["types"][0].shape

        like_node = node_dict[node_entry["inputs"][1]]
        assert len(like_node) == 1, "input node can not be a Tuple"
        like_node = like_node[0]
        try:
            like_shape = like_node["types"][0].shape
        except:
            like_shape = like_node["inputs"][0].data.shape

        starts = [0] * len(input_shape)
        ends = list(input_shape)
        steps = [1] * len(input_shape)
        axes = list(range(len(input_shape)))

        if attrs["axes"] is None:
            attr_axes = list(range(len(input_shape)))
        else:
            attr_axes = list(attrs["axes"])

        like_ends = list(like_shape)
        for i in attr_axes:
            ends[i] = like_ends[i]

        starts = numpy.asarray(starts).astype(numpy.int64)
        ends = numpy.asarray(ends).astype(numpy.int64)
        axes = numpy.asarray(axes).astype(numpy.int64)
        steps = numpy.asarray(steps).astype(numpy.int64)

        input_names = []
        input_names.append(add_input(starts, name, "starts", model_container))
        input_names.append(add_input(ends, name, "ends", model_container))
        input_names.append(add_input(axes, name, "axes", model_container))
        input_names.append(add_input(steps, name, "steps", model_container))

        input_names = [node_entry["input_names"][0]] + input_names

        slice_node = onnx.helper.make_node("Slice", input_names, node_entry["output_names"])
        model_container.add_nodes([slice_node])


# Note: this node can't be the the graph's last node,
# because this op's output shape is dynamic.
class DynSlice(OpConverter):
    """Operator converter for tvm dyn.strided_slice."""

    @classmethod
    def convert_attributes(cls, attrs):
        if attrs.axes is None:
            axes = None
        else:
            axes = attrs.get_int_tuple("axes")

        return {
            "axes": axes,
            "slice_mode": attrs.get_str("slice_mode"),
        }

    @classmethod
    def convert(cls, node_entry, model_container, node_dict):
        attrs = cls.convert_attributes(node_entry["relay_node"].attrs)
        assert attrs["slice_mode"] == "end", "only support end slice_mode"

        name = node_entry["name"]
        input_node = node_dict[node_entry["inputs"][0]]
        assert len(input_node) == 1, "input node can not be a Tuple"
        input_node = input_node[0]
        shape = input_node["types"][0].shape

        input_node = node_dict[node_entry["inputs"][1]]
        assert len(input_node) == 1, "input node can not be a Tuple"
        input_node = input_node[0]
        try:
            start_dtype = input_node["types"][0].dtype
            start_shape = input_node["types"][0].shape
        except:
            start_dtype = input_node["inputs"][0].data.dtype
            start_shape = input_node["inputs"][0].data.shape

        axes = attrs["axes"]
        if axes is None:
            axes = list(range(len(start_shape)))
        else:
            axes = attrs.get_int_tuple("axes")
        axes = numpy.asarray(axes).astype(start_dtype)

        axex_input_name = add_input(axes, name, "axes", model_container)

        input_names = [
            node_entry["input_names"][0],
            node_entry["input_names"][1],
            node_entry["input_names"][2],
            axex_input_name,
            node_entry["input_names"][3]
        ]

        slice_node = onnx.helper.make_node("Slice", input_names, node_entry["output_names"])
        model_container.add_nodes([slice_node])
##*END*

class PriorBox(OpConverter):
    """Operator converter for PriorBox."""

    @classmethod
    def convert_attributes(cls, attrs):
        ar = tvm_array_to_list(attrs.aspect_ratios)
        img_sizes = tvm_array_to_list(attrs.img_sizes)
        max_sizes = tvm_array_to_list(attrs.max_sizes)
        min_sizes = tvm_array_to_list(attrs.min_sizes)
        offset = tvm_array_to_list(attrs.offsets)
        steps = tvm_array_to_list(attrs.steps)
        variances = tvm_array_to_list(attrs.variances)
        return {
            "aspect_ratios": ar,
            "clip": int(attrs.clip),
            "flip": int(attrs.flip),
            "img_sizes": img_sizes,
            "max_sizes": max_sizes,
            "min_sizes": min_sizes,
            "offset": offset,
            "steps": steps,
            "variances": variances
        }

    @classmethod
    def convert(cls, node_entry, model_container, node_dict):
        attrs = cls.convert_attributes(node_entry["relay_node"].attrs)

        input_names = [node_entry["input_names"][0], node_entry["input_names"][1]]

        node = onnx.helper.make_node("PriorBox", input_names, node_entry["output_names"], **attrs)
        model_container.add_nodes([node])

relay_to_onnx_op_mapping = {
    "reshape": Reshape,
    "nn.conv2d": Conv,
    ##*BEGIN*#
    ## Add ConvTranspose 1D and 3D input convert support
    ## data: 21-12-09
    "nn.conv1d_transpose": ConvTranspose,
    "nn.conv2d_transpose": ConvTranspose,
    "nn.conv3d_transpose": ConvTranspose,
    ##*END*
    "add": rename("Add"),
    "nn.relu": rename("Relu"),
    "transpose": Transpose,
    "nn.dense": MatMul,
    ##*BEGIN*#
    ## fix some issue form tvm convert test
    ## data: 21-12-23
    "nn.max_pool1d": MaxPool,
    "nn.max_pool2d": MaxPool,
    "nn.max_pool3d": MaxPool,
    ##*END*
    "nn.batch_flatten": Flatten,
    "multiply": rename("Mul"),
    "nn.bias_add": BiasAdd,
    "nn.batch_norm": BatchNormalization,
    "nn.global_avg_pool2d": rename("GlobalAveragePool"),
    "concatenate": Concat,
    "nn.dropout": Dropout,
    "nn.avg_pool1d": AveragePool,
    "nn.avg_pool2d": AveragePool,
    "nn.avg_pool3d": AveragePool,
    "divide": rename("Div"),
    "mean": ReduceMean,
    #*BEGIN*#
    ## add tvm max op and sum op convert to onnx support
    ## data: 21-10-19
    "max": ReduceMax,
    "min": ReduceMin,
    "sum": ReduceSum,
    "prod": ReduceProd,
    "logsumexp": ReduceLogSumExp,
    ##*END*
    "nn.pad": Pad,
    "nn.softmax": Softmax,
    "squeeze": Squeeze,
    "strided_slice": Slice,
    "greater": rename("Greater"),
    "less": rename("Less"),
    "equal": rename("Equal"),
    "zeros_like": ConstantOfShapeZeros,
    "ones_like": ConstantOfShapeOnes,
    "subtract": rename("Sub"),
    "split": Split,
    "exp": rename("Exp"),
    "layout_transform": LayoutTransform,
    "clip": Clip,
    ##*BEGIN*#
    ## fix some issue form tvm convert test
    ## data: 21-12-23
    #"expand_dims": Unsqueeze,
    "expand_dims": Expand,
    "argmax": ArgMax,
    "nn.space_to_depth": SpaceToDepth,
    ##*END*
    "nn.lrn": LRN,
    "sigmoid": rename("Sigmoid"),
    "copy": rename("Identity"),
    "round": rename("Round"),
    "cast": Cast,
    "image.resize2d": Resize,
    #*BEGIN*#
    ## Add some tvm op convert support for slimai backend.
    ## data: 21-10-28
    "abs" : rename("Abs"),
    "ceil": rename("Ceil"),
    "sin": rename("Sin"),
    "cos": rename("Cos"),
    "tanh": rename("Tanh"),
    "floor": rename("Floor"),
    "power": rename("Pow"),
    "log": rename("Log"),
    "negative": rename("Neg"),
    "sqrt": rename("Sqrt"),
    "maximum": rename("Max"),
    "minimum": rename("Min"),
    "nn.prelu": rename("PRelu"),
    "nn.leaky_relu": LeakyRelu,
    "nn.instance_norm": InstanceNormalization,
    "nn.depth_to_space": DepthToSpace,
    "broadcast_to_like": ExpandShape,
    "scatter": ScatterElements,
    "scatter_nd": ScatterND,
    ##*END*
    ##*BEGIN*#
    ## add some tvm op convert support and fix bug when model has two outputs
    ## data: 21-11-02
    "broadcast_to": ExpandBroadcastTo,
    "where": rename("Where"),
    "nn.batch_matmul": BatchMatMul,
    "nn.global_avg_pool1d": rename("GlobalAveragePool"),
    "nn.global_avg_pool3d": rename("GlobalAveragePool"),
    "shape_of": rename("Shape"),
    "take" : Gather,
    "tile" : Tile,
    "zeros" : ConstantZeros,
    "floor_divde": rename("Div"),
    "argwhere": NonZero,
    "topk": TopK,
    #"nn.upsampling": Upsample,
    "nn.upsampling": UpsampleResize,
    ##*END*
    ##*BEGIN*#
    ## add support for If and NonMaxSuppression convert, and some other op.
    ## data: 21-11-20
    "vision.all_class_non_max_suppression": NonMaxSuppression,
    "cast_like": CastLike,
    "slice_like": SliceLike,
    "greater_equal": rename("Greater"),
    "dyn.strided_slice": DynSlice,
    ##*END*
    "vision.ssd_priorbox": PriorBox,
}


class ModelContainer(object):
    """A container class to hold  different attributes of ONNX model graph"""

    def __init__(self, name, opset_version):
        self._name = name
        self._opset_version = opset_version
        self._inputs = []
        self._outputs = []
        self._nodes = []
        self._initializers = []

    def add_inputs(self, inputs):
        self._inputs.extend(inputs)

    def add_outputs(self, outputs):
        self._outputs.extend(outputs)

    def add_nodes(self, nodes):
        self._nodes.extend(nodes)

    def add_initializers(self, initializers):
        self._initializers.extend(initializers)

    def _get_opsets(self):
        opsets = []
        imp = OperatorSetIdProto()
        imp.version = self._opset_version
        opsets.append(imp)
        return opsets

    def make_model(self):
        """Creates the onnx model from the graph"""
        onnx_graph = onnx.helper.make_graph(
            self._nodes, self._name, self._inputs, self._outputs, self._initializers
        )
        kwargs = {}
        kwargs["opset_imports"] = self._get_opsets()
        kwargs["producer_name"] = "TVM Relay"
        kwargs["producer_version"] = tvm.__version__

        return onnx.helper.make_model(onnx_graph, **kwargs)


class RelayToONNXConverter(ExprVisitor):
    """A helper class to traverse the Relay graph and convert Relay nodes to ONNX model

    Parameters
    ----------
    name : str
       name of the model

    params : dict
        dict of the parameter names and NDarray values

    opset_version : int
        target onnx opset version

    """

    def __init__(self, name, params, opset_version):
        super().__init__()
        self._name = name
        self._mc = ModelContainer(name, opset_version)
        self._params = params
        self._node_dict = {}
        self._node_count = 0
        self.last_node = None

    @classmethod
    def _get_node_entry(cls, relay_node, name):
        return {
            "relay_node": relay_node,
            "inputs": [relay_node],  # inputs in the form of relay nodes
            "types": [],  # output types in case of call nodes else self type
            "name": name,  # name of the node
            "input_names": [name],  # input names in case of call nodes else self name
            "output_names": [name],  # output names in case of call nodes else self name
            "op": None,  # op name in case of call node else None
        }

    def convert_to_onnx(self, func):
        """Traverse Relay graph and generate a ONNX model"""
        self.visit(func)
        self._add_output(self._node_dict[self.last_node])
        model = self._mc.make_model()
        return run_onnx_optimizer(model)

    def visit(self, expr):
        self._node_count += 1
        super().visit(expr)

    def visit_constant(self, const):
        node_index = self._node_count
        name = self._name + "_const_" + str(node_index)
        node_entry = self._get_node_entry(const, name)
        #*BEGIN*#
        ## Fixed an issue when const nodes not populated with checked_type, can infer node types with value data type
        ## data: 21-10-09
        ##*END*
        node_entry["types"] =  const.data.dtype

        self._add_constant_input(node_entry, node_index)
        self._node_dict[const] = [node_entry]

    def visit_var(self, var):
        node_index = self._node_count
        node_entry = self._get_node_entry(var, var.name_hint)
        node_entry["types"] = [var.type_annotation]

        self._add_input(node_entry, node_index)
        self._node_dict[var] = [node_entry]

    def visit_tuple(self, tup):
        self._node_dict[tup] = []
        for f in tup.fields:
            self.visit(f)
            self._node_dict[tup].extend(self._node_dict[f])

        self.last_node = tup

    def visit_tuple_getitem(self, t):
        self.visit(t.tuple_value)
        tup_node = self._node_dict[t.tuple_value]
        if len(tup_node) > 1:
            self._node_dict[t] = tup_node[t.index]
        else:
            node_entry = copy.deepcopy(tup_node[0])
            output_names = [node_entry["output_names"][t.index]]
            node_entry["output_names"] = output_names
            self._node_dict[t] = [node_entry]
        self.last_node = t

    def visit_call(self, call):
        node_index = self._node_count
        op = call.op
        name = "{}_{}".format(op, node_index)
        node_entry = self._get_node_entry(call, name)

        node_entry["op"] = op
        node_entry["input_names"] = []
        node_entry["inputs"] = []
        node_entry["output_names"] = None
        for input_arg in call.args:
            self.visit(input_arg)
            input_names = []
            for arg_node_entry in self._node_dict[input_arg]:
                input_names.extend(arg_node_entry["output_names"])
            node_entry["input_names"].extend(input_names)
            node_entry["inputs"].extend([input_arg])

        node_entry["types"] = call_node_infer_type(call)
        node_entry["output_names"] = []
        for i in range(len(node_entry["types"])):
            node_entry["output_names"].append(name + str(i))
        self.last_node = call
        self._add_node(node_entry, node_index)
        self._node_dict[call] = [node_entry]

    ##*BEGIN*#
    ## add some tvm op convert support and fix bug when model has two outputs
    ## data: 21-11-20
    def visit_if(self, if_node):
        node_index = self._node_count
        cond = if_node.cond
        op = "if"
        name = "{}_{}".format(op, node_index)
        node_entry = self._get_node_entry(if_node, name)

        for input_arg in [cond, if_node.true_branch, if_node.false_branch]:
            self.visit(input_arg)
            input_names = []
            for arg_node_entry in self._node_dict[input_arg]:
                input_names.extend(arg_node_entry["output_names"])
            node_entry["input_names"].extend(input_names)
            node_entry["inputs"].extend([input_arg])

        node_entry["types"] = call_node_infer_type(if_node)
        node_entry["output_names"] = []
        for i in range(len(node_entry["types"])):
            node_entry["output_names"].append(name + str(i))

        # TODO: subgraph only support constant node, need rebuild the then_branch and else_branch sub graph
        for initializer in self._mc._initializers:
            if initializer.name ==  node_entry["input_names"][2]:
                then_value = initializer

            if initializer.name ==  node_entry["input_names"][3]:
                else_value = initializer

        then_out = onnx.helper.make_tensor_value_info('then_out', then_value.data_type, then_value.dims)
        else_out = onnx.helper.make_tensor_value_info('else_out', else_value.data_type, else_value.dims)

        then_const_node = onnx.helper.make_node(
            'Constant',
            inputs=[],
            outputs=['then_out'],
            value=then_value
        )

        else_const_node = onnx.helper.make_node(
            'Constant',
            inputs=[],
            outputs=['else_out'],
            value=else_value
        )

        then_body = onnx.helper.make_graph(
            [then_const_node],
            'then_body',
            [],
            [then_out]
        )

        else_body = onnx.helper.make_graph(
            [else_const_node],
            'else_body',
            [],
            [else_out]
        )

        input_names = [node_entry["input_names"][1]]

        node = onnx.helper.make_node(
            'If',
            input_names,
            node_entry["output_names"],
            then_branch=then_body,
            else_branch=else_body,
        )

        self.last_node = if_node
        self._mc.add_nodes([node])
        self._node_dict[if_node] = [node_entry]
    ##*END*

    def _add_node(self, node_entry, idx):
        """Convert Relay operator node to ONNX operator and add it to container nodes list"""
        if node_entry["op"].name not in relay_to_onnx_op_mapping:
            raise NotImplementedError(
                "Currently the operator '{0}' is " "not supported.".format(node_entry["op"].name)
            )
        converter = relay_to_onnx_op_mapping[node_entry["op"].name]()

        return converter.convert(node_entry, self._mc, self._node_dict)

    def _add_params(self, node_entry, idx):
        """Add param value to initializer and name to inputs"""
        param_name = node_entry["name"]
        assert (
            param_name in self._params
        ), "The parameter {0} is not present" "in params dict provided.".format(param_name)
        value = self._params[param_name]
        numpy_array = value.numpy()
        tensor = numpy_helper.from_array(numpy_array, param_name)
        self._mc.add_initializers([tensor])
        dtype = onnx.mapping.NP_TYPE_TO_TENSOR_TYPE[numpy_array.dtype]
        input = onnx.helper.make_tensor_value_info(param_name, dtype, shape=numpy_array.shape)
        self._mc.add_inputs([input])

    def _add_constant_input(self, node_entry, idx):
        """Create named input for constant and add it to container inputs.
        If input is a parameter then add to param
        """
        node = node_entry["relay_node"]
        param_name = node_entry["name"]
        self._params[param_name] = node.data
        self._add_params(node_entry, idx)

    def _add_input(self, node_entry, idx):
        """Add input node to container inputs. If input is a parameter then add to param"""
        if node_entry["name"] in self._params:
            self._add_params(node_entry, idx)
        else:
            node_type = node_entry["types"][0]
            dtype = onnx.mapping.NP_TYPE_TO_TENSOR_TYPE[numpy.dtype(node_type.dtype)]
            input = onnx.helper.make_tensor_value_info(
                node_entry["name"], dtype, shape=get_node_shape(node_type)
            )
            self._mc.add_inputs([input])

    ##*BEGIN*#
    ## add some tvm op convert support and fix bug when model has two outputs
    ## data: 21-11-02
    def _add_output(self, node_entries):
        """Add output node to container outputs."""

        types_index = 0
        for node_entry in node_entries:
            if not len(node_entry["output_names"]) == len(node_entry["types"]):
                node_type = node_entry["types"][types_index]
                for output_name in node_entry["output_names"]:
                    dtype = onnx.mapping.NP_TYPE_TO_TENSOR_TYPE[numpy.dtype(node_type.dtype)]
                    output = onnx.helper.make_tensor_value_info(
                        output_name, dtype, shape=get_node_shape(node_type)
                    )
                    self._mc.add_outputs([output])
                    types_index = types_index + 1
            else:
                for node_type, output_name in zip(node_entry["types"], node_entry["output_names"]):
                    dtype = onnx.mapping.NP_TYPE_TO_TENSOR_TYPE[numpy.dtype(node_type.dtype)]
                    output = onnx.helper.make_tensor_value_info(
                        output_name, dtype, shape=get_node_shape(node_type)
                    )
                    self._mc.add_outputs([output])
    ##*END*


def to_onnx(relay_ir, params, name, opset_version=11, path=None):
    """Convert a Relay Function Module into an equivalent ONNX and serialize it to the path

    Parameters
    ----------
    relay_ir : tvm.ir.IRModule or tvm.relay.Function
        The relay module object

    params : dict
        dict of the parameter names and NDarray values

    name : str
        name of the output ONNX graph

    opset_version : int
        target onnx opset version

    path : str
        The path where ONNX model will be saved

    Returns
    -------
    onnx_model : onnx.ModelProto
        converted ONNX model as a ModelProto.

    """

    if opset_version not in ONNX_OPSET_VERSONS_SUPPORTED:
        raise NotImplementedError("Currently only opset version 11 is supported.")

    if opset_version > defs.onnx_opset_version():
        raise Exception(
            "The ONNX package installed of version {} does not support the opset "
            "version {}. Upgrade the ONNX package to latest version.".format(
                get_onnx_version(), opset_version
            )
        )

    func = relay_ir["main"] if isinstance(relay_ir, tvm.ir.IRModule) else relay_ir

    converter = RelayToONNXConverter(name, params, opset_version)
    onnx_model = converter.convert_to_onnx(func)

    if path:
#*BEGIN*#
## output graph output_names to txt
## data: 21-10-13
        ocnt = len(onnx_model.graph.output)
        if not os.path.exists("/root/.tvm/slimai_workspace/output/build_dir"):
            os.system("mkdir -p /root/.tvm/slimai_workspace/output/build_dir")
        with open("/root/.tvm/slimai_workspace/output/build_dir/output_names.txt", "w") as fp:
            for o in range(ocnt):
                fp.writelines(onnx_model.graph.output[o].name + '\n')
##*END*
        onnx.save(onnx_model, path)
    return onnx_model

#*BEGIN*#
## Add "relay.ext.to_onnx" function for SlimAI codegen
## data: 21-10-13
@tvm._ffi.register_func("relay.ext.builder_count")
def builder_count():
    if os.path.exists("/root/.tvm/slimai_workspace/output/build_dir/build_count.txt"):
        fi = open("/root/.tvm/slimai_workspace/output/build_dir/build_count.txt", "r")
        lines = fi.readlines()
        fi.close()
        retval = int(lines[0].strip())+1
        fo = open("/root/.tvm/slimai_workspace/output/build_dir/build_count.txt", "w")
        fo.writelines(str(retval) + "\n")
        fo.close()
    else:
        fo = open("/root/.tvm/slimai_workspace/output/build_dir/build_count.txt", "w")
        fo.writelines("0\n")
        fo.close()
        retval = 0
    return retval

@tvm._ffi.register_func("relay.ext.build_from")
def build_from():
    model_path = os.getenv('SLIMAI_MODEL_PATH')
    if model_path is not None and os.path.splitext(model_path)[-1] == ".tflite":
        return "tflite"
    else:
        return "relay"

def relay_to_xnnc_base(func, params):
    """Convert relay to ONNX for XNNC to use

    :param func: Relay function
    :return: XNNC generated elf file path
    """

    assert isinstance(func, tvm.relay.function.Function)
    fname = str(func.attrs.global_symbol)
    inputs = {}
    for name, param in params.items():
        if isinstance(param, numpy.ndarray):
            param = _nd.array(param)
        inputs[name] = param

    if not os.path.exists("/root/.tvm/slimai_workspace"):
        os.system("mkdir -p /root/.tvm/slimai_workspace")

    model_path = os.getenv('SLIMAI_MODEL_PATH')
    if model_path is not None and os.path.splitext(model_path)[-1] == ".tflite":
        tflite_model = model_path
        os.system("cp " + tflite_model + " /root/.tvm/slimai_workspace/" + fname + ".tflite")
        # get TFLite model from buffer
        tflite_model_buf = open(tflite_model, "rb").read()
        try:
            import tflite
            model = tflite.Model.GetRootAsModel(tflite_model_buf, 0)
        except AttributeError:
            import tflite.Model
            model = tflite.Model.Model.GetRootAsModel(tflite_model_buf, 0)
        subgraph = model.Subgraphs(0)
        # model inputs / outputs
        model_inputs = subgraph.InputsAsNumpy()
        model_outputs = subgraph.OutputsAsNumpy()
        net_feed_input = [subgraph.Tensors(i).Name().decode("utf-8") for i in model_inputs]
        #output = [subgraph.Tensors(i).Name().decode("utf-8") for i in model_outputs]
        output = []
        scales = []
        zero_points = []
        for i in model_outputs:
            output.append(subgraph.Tensors(i).Name().decode("utf-8"))
            # Check if the tensors are quantized. Parse if yes.
            tflite_quant_params = subgraph.Tensors(i).Quantization()
            if tflite_quant_params is not None:
                tflite_scale = tflite_quant_params.ScaleAsNumpy()
                tflite_zero_point = tflite_quant_params.ZeroPointAsNumpy()
                if tflite_scale.size == 1 and tflite_zero_point.size == 1:
                        scale = float(tflite_scale[0])
                        zero_point = int(tflite_zero_point[0])
                        scales.append(scale)
                        zero_points.append(zero_point)
                else:
                    raise SystemExit('only support per-tensor activation quantization')
            else:
                scales.append(0.0)
                zero_points.append(0.0)

        model_ext = '.tflite'
        ## output graph output_names to txt
        ocnt = len(output)
        if not os.path.exists("/root/.tvm/slimai_workspace/output/build_dir"):
            os.system("mkdir -p /root/.tvm/slimai_workspace/output/build_dir")
        with open("/root/.tvm/slimai_workspace/output/build_dir/output_names.txt", "w") as fp:
            for o in range(ocnt):
                fp.writelines(output[o] + '\n')

        with open("/root/.tvm/slimai_workspace/output/build_dir/output_scales.txt", "w") as fp:
            for o in range(ocnt):
                fp.writelines(str(scales[o]) + '\n')

        with open("/root/.tvm/slimai_workspace/output/build_dir/output_zps.txt", "w") as fp:
            for o in range(ocnt):
                fp.writelines(str(zero_points[o]) + '\n')

    else:
        global slimai_onnx
        slimai_onnx = True # produce onnx for slimai
        model = to_onnx(func, inputs, fname, 11, "/root/.tvm/slimai_workspace/" + fname + ".onnx")
        slimai_onnx = False
        # return fname, "", "", "", ""

        output =[node.name for node in model.graph.output]
        input_all = [node.name for node in model.graph.input]
        input_initializer =  [node.name for node in model.graph.initializer]
        net_feed_input = list(set(input_all)  - set(input_initializer))
        model_ext = '.onnx'

    print('Input:   ', net_feed_input)
    print('Outputs: ', output)

    # get dtype from func
    ret_dtype = []
    if isinstance(func.ret_type, TensorType):
        ret_dtype.append(func.ret_type.dtype)
    elif isinstance(func.ret_type, TupleType):
        for field in func.ret_type.fields:
            if isinstance(field, TensorType):
                ret_dtype.append(field.dtype)
            else:
                print("recursive tuple not supported")

    print('Func ret:', ret_dtype)
    with open("/root/.tvm/slimai_workspace/output/build_dir/output_dtypes.txt", "w") as fp:
        for i in ret_dtype:
            fp.writelines(i + '\n')

    cfg_path = os.getenv('SLIMAI_CFG_FILE')
    compile_disable = os.getenv('SLIMAI_COMPILE_DISABLE')
    if cfg_path is None:
        raise SystemExit('SLIMAI_CFG_FILE environment variable not defined')

    netname, nettype, usrout = slimai.rewrite_cfg(cfg_path,
        fname + model_ext, net_feed_input, output)
    if not os.path.exists(usrout):
        os.system("mkdir -p "+ usrout)
    os.system("cp /root/.tvm/slimai_workspace/" + fname + model_ext + " " + usrout + "/" + fname + model_ext)
    if compile_disable is None:
        cpath = slimai.xnnc_codegen(netname, usrout)
        return fname, cpath, netname, nettype, usrout

    return fname, "", netname, nettype, usrout

@tvm._ffi.register_func("relay.ext.to_onnx")
def relay_to_onnx(func, params):
    """Convert relay to ONNX for XNNC to use

    :param func: Relay function
    :return: XNNC generated elf file path
    """
    def condense_elf_name(fname):
        """set elf name to shorter string(< 23 chars)"""
        ns = fname.split('_')
        p = -1
        c = 0
        for i in range(len(ns)):
            c += (len(ns[i]) + 1)
            if c < 22:
                p = i
            else:
                break
        fname = '_'.join(ns[:p+1])
        if len(fname) > 22:
            fname = fname[len(fname)-22:]
        return fname
    fname, cpath, netname, nettype, usrout = relay_to_xnnc_base(func, params)
    # fname, _, _, _, _ = relay_to_onnx_base(func, params) #save "/root/.tvm/slimai_workspace/temp/BestProfile.txt"
    # cpath, netname, nettype, usrout =  os.getcwd(), "yolov3_tiny", "Detection", "/workspace/fengfeng.tang/customer_models/custom_cfg/facedet/output"
    # os.chdir("/root/.tvm/slimai_workspace")
    ## call slimAI target-end codegen
    #fname = condense_elf_name(fname)
    build_elf = os.getenv('SLIMAI_BUILD_ELF')
    compile_disable = os.getenv('SLIMAI_COMPILE_DISABLE')
    if build_elf is None: #not mulit mode, should compile immediately
        build_elf = '1'

    print("build_elf", build_elf)
    if build_elf == '0':
        print("skip build elf process")

    if compile_disable is None:
        slimai.rewrite_code(netname, nettype, cpath)
        if build_elf != '0':
            slimai.build_firmware(fname + ".elf", cpath, usrout)
            #clean_build()

    #return elf file
    if build_elf == '0':
        ret = "skip_elf"
    else:
        ret = "/root/.tvm/slimai_workspace/elf/" + fname + ".elf"
    return _ffi_api.String(ret)

@tvm._ffi.register_func("relay.ext.to_onnx_for_ISS")
def relay_to_onnx_for_ISS(func, params):
    """Convert relay to ONNX for XNNC ISS to use

    :param func: Relay function
    :return: XNNC generated inderence file path
    """
    fname, cpath, netname, nettype, usrout = relay_to_xnnc_base(func, params)
    compile_disable = os.getenv('SLIMAI_COMPILE_DISABLE')

    if compile_disable is None:
        slimai.build_for_iss(netname, nettype, cpath)

    ret = "/root/.tvm/slimai_workspace/iss/test_inference"

    return _ffi_api.String(ret)
##*END*

@tvm._ffi.register_func("relay.ext.onnx")
def onnx_compiler(func):
    """Create a runtime module for ONNX from Relay Function

    :param func: Relay function
    :return: runtime module for ONNX
    """

    assert isinstance(func, tvm.relay.function.Function)
    name = str(func.attrs.global_symbol)
    model = to_onnx(func, {}, name)
    const_vars = [const.name for const in model.graph.initializer]
    name_bytes = bytes(name, "utf-8")
    name_size = struct.pack("I", len(name_bytes))
    model_serialized = model.SerializeToString()
    model_size = struct.pack("I", model.ByteSize())
    data = b"" + name_size + name_bytes + model_size + model_serialized

    runtime_func = "runtime.ONNXModuleCreate"
    fcreate = tvm._ffi.get_global_func(runtime_func)
    return fcreate(data.hex(), name, const_vars)


@tvm._ffi.register_func("relay.ext.onnx.save_to_file")
def save_to_file(hex_str, path=None, fmt="onnx"):
    """Store the ONNX subgraphs in the path folder

    :param hex_str: Subgrah names and corresponding serialized onnx hex string
    :param path: path to which ONNX files to be stored
                It is assumed that path exists
    :param fmt: extension of the files to be stored
    """
    onnx_ir = bytes.fromhex(hex_str)

    offset = 0
    while offset < len(onnx_ir):
        stop = offset + 4
        (name_size,) = struct.unpack("I", onnx_ir[offset:stop])
        name = onnx_ir[stop : stop + name_size].decode("utf-8")
        stop = stop + name_size
        (model_size,) = struct.unpack("I", onnx_ir[stop : stop + 4])
        stop = stop + 4
        model_serialized = onnx_ir[stop : stop + model_size]
        offset = stop + model_size

        model_onnx = onnx.load_model_from_string(model_serialized)
        onnx.save(model_onnx, "{}{}{}.{}".format(path, os.path.sep, name, fmt))
