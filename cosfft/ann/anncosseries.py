from typing import Dict, Tuple

import numpy
from cosfft.ann.net import Net
from model.sde import Sde
import numpy as np
import pandas as pd
import torch
import torch.nn as nn

class AnnCosSeries:
    __range = {'r':(), 's':(), 'tau':()}

    def __init__(self, sde: Sde) -> None:
        numpy.random.seed(123)
        net = Net()
        criterion = nn.MSELoss
        optimizer = torch.optim.Adam(net.parameters(), lr = 0.01)
        
    @classmethod
    def set_range(cls, range_info: Dict[str, Tuple[float, float]]) -> None:
        for par_name in ['r', 's', 'tau']:
            if par_name in range_info:
                cls.__range[par_name] = range_info[par_name]