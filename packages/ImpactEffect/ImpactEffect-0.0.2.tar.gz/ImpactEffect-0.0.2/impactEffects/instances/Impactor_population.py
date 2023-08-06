# -*- encoding: utf-8 -*-
"""
Filename         :Impactor_population.py
Description      :
Time             :2022/07/10 09:38:36
Author           :daniel
Version          :1.0
"""

import random


class Distribution:
    def __init__(self):
        return


class nomal_distribution(Distribution):
    def __init__(self, mean, std):
        super().__init__()
        self.mean = mean
        self.std = std
        return

    def get_value(self):
        return random.normalvariate(self.mean, self.std)


# class Impactor_population:
#     def __init__(self):
#         return
