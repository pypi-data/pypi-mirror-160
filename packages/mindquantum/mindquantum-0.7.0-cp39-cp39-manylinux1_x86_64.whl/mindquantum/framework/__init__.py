# Copyright 2021 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Quantum neural networks operators and cells."""
import warnings

__all__ = []
try:
    import mindspore

    from .layer import MQAnsatzOnlyLayer, MQLayer, MQN2AnsatzOnlyLayer, MQN2Layer
    from .operations import (
        MQAnsatzOnlyOps,
        MQEncoderOnlyOps,
        MQN2AnsatzOnlyOps,
        MQN2EncoderOnlyOps,
        MQN2Ops,
        MQOps,
    )

    __all__.extend(
        [
            "MQAnsatzOnlyLayer",
            "MQN2AnsatzOnlyLayer",
            "MQLayer",
            "MQN2Layer",
            "MQOps",
            "MQN2Ops",
            "MQAnsatzOnlyOps",
            "MQN2AnsatzOnlyOps",
            "MQEncoderOnlyOps",
            "MQN2EncoderOnlyOps",
        ]
    )
except ImportError:
    warnings.warn(
        "MindSpore not installed, you may not be able to use hybrid quantum classical neural network.",
        stacklevel=2,
    )

__all__.sort()
