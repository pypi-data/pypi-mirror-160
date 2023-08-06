# -*- encoding: utf-8 -*-
"""
Filename         :Impactor.py
Description      :
Time             :2022/07/10 09:38:24
Author           :daniel
Version          :1.0
"""

from impactEffects.core.config import *


class Impactor:
    """
    __init__
    """

    def __init__(self, diameter, density, velocity, theta):
        self.pdiameter = diameter
        self.density = density
        self.velocity = velocity
        self.theta = theta
        # self.ttype = ttype

        self.mass = None
        self.energy0 = None
        self.energy0_megatons = None
        self.rec_time = None

        return

    def calculate_mass(self):
        self.mass = ((PI * self.pdiameter ** 3) / 6) * self.density

    def calculate_energy0(self):
        if self.mass is None:
            self.calculate_mass()

        self.energy0 = 0.5 * self.mass * (self.velocity * 1000) ** 2

    def calcualte_energy0_megatons(self):
        if self.energy0 is None:
            self.calculate_energy0()

        self.energy0_megatons = self.energy0 * joules2megatones

    def calculate_recTime(self):
        mass = self.get_mass()

        # Compute the recurrence interval for this energy impact
        # New model (after Bland and Artemieva (2006) MAPS 41 (607-621).
        if mass < 3:
            self.rec_time = 10 ** (-4.568) * mass ** 0.480
        elif mass < 1.7e10:
            self.rec_time = 10 ** (-4.739) * mass ** 0.926
        elif mass < 3.3e12:
            self.rec_time = 10 ** (0.922) * mass ** 0.373
        elif mass < 8.4e14:
            self.rec_time = 10 ** (-0.086) * mass ** 0.454
        else:
            self.rec_time = 10 ** (-3.352) * mass ** 0.672

        energy0_megatons = self.get_energy0_megatons()
        self.rec_time = max(self.rec_time, 110 * energy0_megatons ** 0.77)

    def get_energy0(self) -> float:
        if self.energy0 is None:
            self.calculate_energy0()
        return self.energy0

    def get_energy0_megatons(self) -> float:
        if self.energy0_megatons is None:
            self.calcualte_energy0_megatons()

        return self.energy0_megatons

    def get_rec_time(self):
        if self.rec_time is None:
            self.calculate_recTime()
        return self.rec_time

    def get_pdiameter(self) -> float:
        return self.pdiameter

    def get_density(self) -> float:
        return self.density

    def get_velocity(self) -> float:
        return self.velocity

    def get_mass(self) -> float:
        if self.mass is None:
            self.calculate_mass()

        return self.mass

    def get_theta(self):
        return self.theta


if __name__ == "__main__":
    impactor = Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    print(impactor.get_pdiameter())
