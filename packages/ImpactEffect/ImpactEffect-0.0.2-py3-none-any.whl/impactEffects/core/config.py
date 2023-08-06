# -*- encoding: utf-8 -*-
"""
Filename         :config.py
Description      :
Time             :2022/07/10 09:38:07
Author           :daniel
Version          :1.0
"""

import math
from enum import Enum, unique

# PI
PI = math.pi
joules2megatones = 1 / (4.186 * 10 ** 15)

# rename the functions
exp = math.exp
log = math.log
cos = math.cos
sin = math.sin
tan = math.tan
tanh = math.tanh
atan = math.atan
acos = math.acos
sqrt = math.sqrt


@unique
class Choices(Enum):
    Collins = 0
    Example = 256
