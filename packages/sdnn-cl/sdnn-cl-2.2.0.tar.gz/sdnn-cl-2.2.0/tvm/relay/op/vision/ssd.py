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
"""SSD operations."""
from tvm.relay import expr
from . import _make


def ssd_priorbox(
    featuremap, data, min_sizes, max_sizes, img_sizes=(0, 0), aspect_ratios=(1.0,),
    steps=(0.0, 0.0), offsets=(0.5, 0.5), variances=(0.1, 0.1, 0.2, 0.2), clip=False, flip=True
):
    """Generate the prior boxes of designated sizes and aspect ratios.

    Parameters
    ----------
    featuremap : relay.Expr
        The feature map input data tensor.

    data : relay.Expr
        The image data tensor.

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

    offsets : tuple of float, optional
        Priorbox center offsets, y and x respectively.

    flip : boolean, optional
        Whether to consider reverse aspect ratios.

    variances : Array of float, optional
        List of variances for x, y, w, h.

    clip : boolean, optional
        Whether to clip the prior's coordinates such that they are within [0, 1].

    Returns
    -------
    out : relay.Expr
        2-D tensor with shape [2, h_in * w_in * (num_min_sizes * num_ratios + num_max_sizes) * 4]
    """
    return _make.ssd_priorbox(featuremap, data, img_sizes, min_sizes, max_sizes, aspect_ratios, steps, offsets, variances, clip, flip)

