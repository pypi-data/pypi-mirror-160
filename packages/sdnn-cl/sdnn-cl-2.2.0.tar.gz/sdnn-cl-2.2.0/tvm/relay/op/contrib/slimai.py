import tvm.ir
from tvm.relay import transform
from tvm.contrib.target import onnx, slimai
from ...dataflow_pattern import wildcard, is_op
from .register import register_pattern_table

def slimai_build_init():
    slimai.clean_build()

def partition_for_slimai(mod, net_name="default"):
    """Partition the graph greedily offloading supported
    operators to slimai.

    Parameters
    ----------
    mod : Module
        The module to run passes on.
    net_name: String
        The network name to partition.

    Returns
    -------
    ret : annotated and partitioned module.
    """
    seq = tvm.transform.Sequential(
        [
            transform.RemoveUnusedFunctions(),
            transform.AnnotateTarget("slimai"),
            transform.MergeCompilerRegions(),
            transform.PartitionGraph(net_name),
        ]
    )

    return seq(mod)

def partition_for_slimai_iss(mod, net_name="default"):
    """Partition the graph greedily offloading supported
    operators to slimai_iss.

    Parameters
    ----------
    mod : Module
        The module to run passes on.
    net_name: String
        The network name to partition.

    Returns
    -------
    ret : annotated and partitioned module.
    """
    seq = tvm.transform.Sequential(
        [
            transform.AnnotateTarget("slimai_iss"),
            transform.MergeCompilerRegions(),
            transform.PartitionGraph(net_name),
        ]
    )

    return seq(mod)


def _register_external_op_helper(op_name, supported=True):
    """The helper function to indicate that a given operator can be supported
    by slimai.

    Paramters
    ---------
    op_name : Str
        The name of operator that will be registered.

    Returns
    -------
    f : callable
        A function that returns if the operator is supported by slimai.
    """

    @tvm.ir.register_op_attr(op_name, "target.slimai")
    def _func_wrapper(expr):
        attrs, args = expr.attrs, expr.args
        if op_name == "nn.conv2d":
            if attrs["kernel_size"][0] > 16 or attrs["kernel_size"][1] > 16:
                return False
        return supported

    @tvm.ir.register_op_attr(op_name, "target.slimai_iss")
    def _func_wrapper(expr):
        attrs, args = expr.attrs, expr.args
        if op_name == "nn.conv2d":
            if attrs["kernel_size"][0] > 16 or attrs["kernel_size"][1] > 16:
                return False
        return supported

    return _func_wrapper


_register_external_op_helper("nn.batch_norm")
_register_external_op_helper("nn.global_avg_pool2d")
_register_external_op_helper("nn.max_pool2d")
_register_external_op_helper("nn.batch_flatten")
_register_external_op_helper("nn.bias_add")
_register_external_op_helper("nn.softmax")
_register_external_op_helper("nn.conv2d")
_register_external_op_helper("nn.depthwise_conv2d")
_register_external_op_helper("nn.dense")
_register_external_op_helper("nn.relu")
_register_external_op_helper("nn.pad")
_register_external_op_helper("nn.prelu")
_register_external_op_helper("nn.space_to_depth")
_register_external_op_helper("nn.upsampling")
_register_external_op_helper("image.resize2d")
_register_external_op_helper("round")
_register_external_op_helper("log")
_register_external_op_helper("maximum")
_register_external_op_helper("minimum")
_register_external_op_helper("max")
_register_external_op_helper("min")
_register_external_op_helper("sum")
_register_external_op_helper("mean")
_register_external_op_helper("negative")
_register_external_op_helper("power")
_register_external_op_helper("sin")
_register_external_op_helper("tan")
_register_external_op_helper("sigmoid")
_register_external_op_helper("sqrt")
_register_external_op_helper("squeeze")
_register_external_op_helper("strided_slice")
_register_external_op_helper("Custom_Slice")
_register_external_op_helper("expand_dims")
_register_external_op_helper("split")
_register_external_op_helper("tile")
_register_external_op_helper("topk")
_register_external_op_helper("where")
_register_external_op_helper("scatter_nd")
_register_external_op_helper("transpose")
_register_external_op_helper("clip")
_register_external_op_helper("reshape")
_register_external_op_helper("add")
_register_external_op_helper("subtract")
_register_external_op_helper("multiply")
_register_external_op_helper("abs")
_register_external_op_helper("argmax")
_register_external_op_helper("broadcast_to")
_register_external_op_helper("cast")
_register_external_op_helper("ceil")
_register_external_op_helper("concatenate")
_register_external_op_helper("copy")
_register_external_op_helper("cos")
_register_external_op_helper("divide")
_register_external_op_helper("exp")
_register_external_op_helper("floor")
_register_external_op_helper("greater")
_register_external_op_helper("gather")
_register_external_op_helper("If")
_register_external_op_helper("less")
_register_external_op_helper("nn.avg_pool2d")
_register_external_op_helper("nn.conv2d_transpose")
_register_external_op_helper("nn.depth_to_space")
_register_external_op_helper("nn.dropout")
_register_external_op_helper("nn.leaky_relu")
_register_external_op_helper("nn.lrn")
_register_external_op_helper("nn.instance_norm")
_register_external_op_helper("ones_like")
_register_external_op_helper("tanh")
_register_external_op_helper("zeros_like")
_register_external_op_helper("vision.ssd_priorbox")
_register_external_op_helper("slice_like")
_register_external_op_helper("shape_of")
_register_external_op_helper("take")
_register_external_op_helper("layout_transform")

# for tflite quantized model
_register_external_op_helper("qnn.conv2d")
_register_external_op_helper("qnn.requantize")
_register_external_op_helper("qnn.add")
_register_external_op_helper("qnn.mul")
_register_external_op_helper("nn.space_to_batch_nd")
_register_external_op_helper("qnn.concatenate")
_register_external_op_helper("qnn.dense")
