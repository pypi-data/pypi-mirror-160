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
# pylint: disable=invalid-name, no-member, too-many-locals, too-many-arguments, undefined-variable
"""SSD priorbox operators"""
import tvm

from tvm.te import hybrid
from tvm.tir import sqrt

from tvm import topi

@hybrid.script
def hybrid_ssd_priorbox(featuremap, data, min_sizes, max_sizes, img_sizes, aspect_ratios,
                        steps, offsets, variances):
    """Hybrid routing for priorbox operator.
    """

    layer_height = featuremap.shape[2]
    layer_width = featuremap.shape[3]

    img_height = 0
    img_width = 0
    if img_sizes[0] == 0 or img_sizes[1] == 0:
        img_height = data.shape[2]
        img_width = data.shape[3]
    else:
        img_height = img_sizes[0]
        img_width = img_sizes[1]

    num_min_sizes = len(min_sizes)
    num_max_sizes = len(max_sizes)
    num_ratios = len(aspect_ratios)
    num_priors = num_min_sizes * num_ratios + num_max_sizes
    dim = layer_height * layer_width * num_priors * 4

    output = output_tensor((1, 2, dim), "float32")

    steps_w = 0.0
    steps_h = 0.0
    if steps[0] == 0.0 or steps[1] == 0.0:
        steps_w = img_width * 1.0 / layer_width;
        steps_h = img_height * 1.0 / layer_height;
    else:
        steps_w = steps[1] * 1.0
        steps_h = steps[0] * 1.0

    offset_h = offsets[0] * 1.0
    offset_w = offsets[1] * 1.0

    # Need to define var out of const_range + if
    box_width = 0.0
    box_height = 0.0
    min_size = 0.0
    max_size = 0.0
    ar = 0.0

    for i in parallel(layer_height):
        center_y = (i + offset_h) * steps_h
        for j in range(layer_width):
            center_x = (j + offset_w) * steps_w
            count = (
                    i * layer_width * (num_min_sizes * num_ratios + num_max_sizes) * 4
                    + j * (num_min_sizes * num_ratios + num_max_sizes) * 4
            )
            for k in const_range(num_min_sizes):
                min_size = float32(min_sizes[k])
                # first prior: aspect_ratio = 1, size = min_size
                box_width = min_size
                box_height = min_size
                output[0, 0, count] = (center_x - box_width / 2.0) / img_width
                output[0, 1, count] = variances[0]
                count = count + 1
                output[0, 0, count] = (center_y - box_height / 2.0) / img_height
                output[0, 1, count] = variances[1]
                count = count + 1
                output[0, 0, count] = (center_x + box_width / 2.0) / img_width
                output[0, 1, count] = variances[2]
                count = count + 1
                output[0, 0, count] = (center_y + box_height / 2.0) / img_height
                output[0, 1, count] = variances[3]
                count = count + 1

                if num_max_sizes > 0:
                    max_size = float32(max_sizes[k])
                    # second prior: aspect_ratio = 1, size = sqrt(min_size * max_size)
                    box_width = sqrt(min_size * max_size)
                    box_height = box_width
                    output[0, 0, count] = (center_x - box_width / 2.0) / img_width
                    output[0, 1, count] = variances[0]
                    count = count + 1
                    output[0, 0, count] = (center_y - box_height / 2.0) / img_height
                    output[0, 1, count] = variances[1]
                    count = count + 1
                    output[0, 0, count] = (center_x + box_width / 2.0) / img_width
                    output[0, 1, count] = variances[2]
                    count = count + 1
                    output[0, 0, count] = (center_y + box_height / 2.0) / img_height
                    output[0, 1, count] = variances[3]
                    count = count + 1

                for r in const_range(num_ratios):
                    ar = float32(aspect_ratios[r])
                    if ar != 1.0:
                        box_width = min_size * sqrt(ar)
                        box_height = min_size / sqrt(ar)
                        output[0, 0, count] = (center_x - box_width / 2.0) / img_width
                        output[0, 1, count] = variances[0]
                        count = count + 1
                        output[0, 0, count] = (center_y - box_height / 2.0) / img_height
                        output[0, 1, count] = variances[1]
                        count = count + 1
                        output[0, 0, count] = (center_x + box_width / 2.0) / img_width
                        output[0, 1, count] = variances[2]
                        count = count + 1
                        output[0, 0, count] = (center_y + box_height / 2.0) / img_height
                        output[0, 1, count] = variances[3]
                        count = count + 1

    return output


def ssd_priorbox(featuremap, data, min_sizes, max_sizes, img_sizes=(0, 0), aspect_ratios=(1.0,),
    steps=(0.0, 0.0), offsets=(0.5, 0.5), variances=(0.1, 0.1, 0.2, 0.2), clip=False, flip=1):
    """Generate the prior boxes of designated sizes and aspect ratios.

    Parameters
    ----------
    featuremap : tvm.te.Tensor
        4-D with shape [batch, c_in, h_in, w_in]]

    data : tvm.te.Tensor
        4-D with shape [batch, c_in, h_in, w_in]]

    aspect_ratios : tuple of float, optional
        Tuple of ratios for anchor boxes.

    img_sizes : tuple of float, optional
        Size of the input image as tuple (w, h), 0 for getting from data tensor.

    min_sizes : Array of float
        Minimum box size in pixels.

    max_sizes : Array of float, optional
        Maximum box size in pixels.

    steps : Tuple of float, optional
        Priorbox step across y and x, 0 for auto calculation.

    offsets : tuple of int, optional
        Priorbox center offsets, y and x respectively.

    flip : boolean, optional
        Whether to consider reverse aspect ratios.

    variances : Array of float, optional
        List of variances for x, y, w, h.

    clip : boolean, optional
        Whether to clip the prior's coordinates such that they are within [0, 1].

    Returns
    -------
    out : tvm.te.Tensor
        3-D tensor with shape [1, 2, h_in * w_in * (num_min_sizes * num_ratios + num_max_sizes) * 4]
    """

    ratios = [1.0]
    if aspect_ratios:
            for ar in aspect_ratios:
                if ar in ratios:
                    continue
                ratios.append(ar)
                if flip:
                    ratios.append(1.0 / ar)

    out = hybrid_ssd_priorbox(
        featuremap,
        data,
        tvm.runtime.convert(min_sizes),
        tvm.runtime.convert(max_sizes),
        tvm.runtime.convert(img_sizes),
        tvm.runtime.convert(ratios),
        tvm.runtime.convert(steps),
        tvm.runtime.convert(offsets),
        tvm.runtime.convert(variances)
    )
    if clip:
        out = topi.clip(out[0], 0, 1)

    return out

