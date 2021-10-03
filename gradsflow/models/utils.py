#  Copyright (c) 2021 GradsFlow. All rights reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from typing import Any, Callable, Dict, List, Union

import numpy as np
import torch
import torchmetrics
from torch import nn
from torchmetrics import Metric

from gradsflow.utility.common import module_to_cls_index

_nn_classes = module_to_cls_index(nn)
_tm_classes = module_to_cls_index(torchmetrics, lower_key=False)

losses: Dict[str, Callable] = {k: v for k, v in _nn_classes.items() if "loss" in k}

metrics: Dict[str, Metric] = {k: v for k, v in _tm_classes.items() if 65 <= ord(k[0]) <= 90}
metrics = {k.lower(): v for k, v in metrics.items()}


def get_device():
    return "cuda" if torch.cuda.is_available() else "cpu"


def to_item(data: Union[torch.Tensor, Any]) -> Union[int, float, str, np.ndarray]:
    if torch.is_tensor(data):
        if data.requires_grad:
            data = data.detach()
        data.cpu()

        if len(data.shape) > 1:
            data = data.numpy()
        else:
            data = data.item()

    return data


def available_losses() -> List[str]:
    return list(losses.keys())


def available_metrics() -> List[str]:
    return list(metrics.keys())
