# -*- encoding: utf-8 -*-
"""
Filename         :core.py
Description      :
Time             :2022/07/10 09:37:51
Author           :daniel
Version          :1.0
"""

from impactEffects.instances.ImpactorClass import *
from impactEffects.instances.TargetClass import *
from impactEffects.core.config import *
from impactEffects.core.core_collins import *


def kinetic_energy(
    impactor: Impactor, type: Choices = Choices.Collins
) -> float:
    """

    Arguments
    ---------
    impactor: Instance of Impactor, containning

    Returns
    -------

    """
    if type is Choices.Collins:
        return collins_kinetic_energy(impactor)

    return None


def kinetic_energy_megatons(
    impactor: Impactor, type: Choices = Choices.Collins
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if type is Choices.Collins:
        return collins_kinetic_energy_megatons(impactor)

    return None


def rec_time(impactor: Impactor, type: Choices = Choices.Collins) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """

    if type is Choices.Collins:
        return collins_rec_time(impactor)

    return None


def iFactor(
    impactor: Impactor, target: Target, type: Choices = Choices.Collins
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """

    if type is Choices.Collins:
        return collins_cal_iFactor(impactor, target)

    return None


def burst_velocity_at_zero(
    impactor: Impactor, target: Target, type: Choices = Choices.Collins
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if type is Choices.Collins:
        return collins_burst_velocity_at_zero(impactor, target)

    return None


def altitude_of_breakup(
    impactor: Impactor,
    target: Target,
    collins_iFactor: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """

    if type is Choices.Collins:
        return collins_altitude_of_breakup(
            impactor, target, collins_iFactor
        )

    return None


def velocity_at_breakup(
    impactor: Impactor,
    target: Target,
    av: float = None,
    altitudeBU: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """

    if type is Choices.Collins:
        return collins_velocity_at_breakup(
            impactor, target, av, altitudeBU
        )

    return None


def dispersion_length_scale(
    impactor: Impactor,
    target: Target,
    altitudeBU: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if type is Choices.Collins:
        return collins_dispersion_length_scale(
            impactor, target, altitudeBU
        )

    return None


def airburst_altitude(
    impactor: Impactor,
    target: Target,
    alpha2: float = None,
    lDisper: float = None,
    altitudeBU: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if type is Choices.Collins:
        return collins_airburst_altitude(
            impactor, target, alpha2, lDisper, altitudeBU
        )

    return None


def brust_velocity(
    impactor: Impactor,
    target: Target,
    altitudeBurst: float = None,
    altitudeBU: float = None,
    vBu: float = None,
    lDisper: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """

    if type is Choices.Collins:
        return collins_brust_velocity(
            impactor, target, altitudeBurst, altitudeBU, vBu, lDisper
        )

    return None


def dispersion_of_impactor(
    impactor: Impactor,
    target: Target,
    l_disper: float = None,
    altitude_bu: float = None,
    altitude_burst: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """

    if type is Choices.Collins:
        return collins_dispersion_of_impactor(
            impactor, target, l_disper, altitude_bu, altitude_burst
        )

    return None


def fraction_of_momentum(
    impactor: Impactor,
    target: Target,
    velocity: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """

    if type is Choices.Collins:
        return collins_fraction_of_momentum(impactor, target, velocity)

    return None


def cal_trot_change(
    impactor: Impactor,
    target: Target,
    velocity: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """

    if type is Choices.Collins:
        return collins_cal_trot_change(impactor, target, velocity)

    return None


def cal_energy_atmosphere(
    impactor: Impactor,
    target: Target,
    velocity: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """

    if type is Choices.Collins:
        return collins_cal_energy_atmosphere(impactor, target, velocity)

    return None


def cal_energy_blast_surface(
    impactor: Impactor,
    target: Target,
    velocity: float = None,
    altitudeBurst: float = None,
    energy_atmosphere: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if type is Choices.Collins:
        return collins_cal_energy_blast_surface(
            impactor, target, velocity, altitudeBurst, energy_atmosphere
        )

    return None


def cal_mass_of_water(
    impactor: Impactor, target: Target, type: Choices = Choices.Collins
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """

    if type is Choices.Collins:
        return collins_cal_mass_of_water(impactor, target)

    return None


def cal_velocity_projectile(
    impactor: Impactor,
    target: Target,
    velocity: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """

    if type is Choices.Collins:
        return collins_cal_velocity_projectile(impactor, target, velocity)

    return None


def cal_energy_at_seafloor(
    impactor: Impactor,
    target: Target,
    vseafloor: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if type is Choices.Collins:
        return collins_cal_energy_at_seafloor(impactor, target, vseafloor)

    return None


def cal_ePIcentral_angle(
    target: Target, type: Choices = Choices.Collins
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """

    if type is Choices.Collins:
        return collins_cal_ePIcentral_angle(target)

    return None


def cal_scaling_diameter_constant(
    target: Target, type: Choices = Choices.Collins
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """

    if type is Choices.Collins:
        return collins_cal_scaling_diameter_constant(target=target)

    return None


def cal_anglefac(
    impactor: Impactor, type: Choices = Choices.Collins
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """

    if type is Choices.Collins:
        return collins_cal_anglefac(impactor)

    return None


def cal_wdiameter(
    impactor: Impactor,
    target: Target,
    anglefac: float = None,
    velocity: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if type is Choices.Collins:
        return collins_cal_wdiameter(impactor, target, anglefac, velocity)

    return None


def cal_transient_crater_diameter(
    impactor: Impactor,
    target: Target,
    Cd: float = None,
    beta: float = None,
    anglefac: float = None,
    vseafloor: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if type is Choices.Collins:
        return collins_cal_transient_crater_diameter(
            impactor, target, Cd, beta, anglefac, vseafloor
        )

    return None


def cal_depthr(
    impactor: Impactor,
    target: Target,
    Dtr: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if type is Choices.Collins:
        return collins_cal_depthr(impactor, target, Dtr)

    return None


def cal_cdiamater(
    impactor: Impactor,
    target: Target,
    Dtr: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if type is Choices.Collins:
        return collins_cal_cdiamater(impactor, target, Dtr)

    return None


def cal_depthfr(
    impactor: Impactor,
    target: Target,
    Dtr: float = None,
    depthtr: float = None,
    cdiameter: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if type is Choices.Collins:
        return collins_cal_depthfr(
            impactor, target, Dtr, depthtr, cdiameter
        )

    return None


def cal_vCrater(
    impactor: Impactor,
    target: Target,
    Dtr: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if type is Choices.Collins:
        return collins_cal_vCrater(impactor, target, Dtr)

    return None


def cal_vratio(
    impactor: Impactor,
    target: Target,
    vCrater: float = None,
    Dtr: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if type is Choices.Collins:
        return collins_cal_vratio(impactor, target, vCrater, Dtr)

    return None


def cal_vCrater_vRation(
    impactor: Impactor,
    target: Target,
    Dtr: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if type is Choices.Collins:
        return collins_cal_vCrater_vRation(impactor, target, Dtr)

    return None


def cal_vMelt(
    impactor: Impactor,
    target: Target,
    velocity: float = None,
    energy_seafloor: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if type is Choices.Collins:
        return collins_cal_vMelt(
            impactor, target, velocity, energy_seafloor
        )

    return None


def cal_mratio_and_mcratio(
    impactor: Impactor,
    target: Target,
    velocity: float = None,
    vMelt: float = None,
    vCrater: float = None,
    Dtr: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if type is Choices.Collins:
        return collins_cal_mratio_and_mcratio(
            impactor, target, velocity, vMelt, vCrater, Dtr
        )

    return None


def cal_eject_arrival(
    impactor: Impactor,
    target: Target,
    altitudeBurst: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if type is Choices.Collins:
        return collins_cal_eject_arrival(impactor, target, altitudeBurst)

    return None


def cal_ejecta_thickness(
    impactor: Impactor,
    target: Target,
    altitudeBurst: float = None,
    Dtr: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if type is Choices.Collins:
        return collins_cal_ejecta_thickness(
            impactor, target, altitudeBurst, Dtr
        )

    return None


def cal_d_frag(impactor: Impactor, target: Target, cdiameter: float = None, altitudeBurst: float = None, Dtr: float = None, type: Choices = Choices.Collins) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if type is Choices.Collins:
        return collins_cal_d_frag(impactor, target, cdiameter, altitudeBurst, Dtr)

    return None


def cal_themal(
    impactor: Impactor,
    target: Target,
    energy_surface: float = None,
    altitudeBurst: float = None,
    delta: float = None,
    velocity: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if type is Choices.Collins:
        return collins_cal_themal(
            impactor,
            target,
            energy_surface,
            altitudeBurst,
            delta,
            velocity,
        )

    return None


def cal_magnitude(
    impactor: Impactor,
    target: Target,
    altitudeBurst: float = None,
    energy_seafloor: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if type is Choices.Collins:
        return collins_cal_magnitude(
            impactor, target, altitudeBurst, energy_seafloor
        )

    return None


def cal_magnitude2(
    impactor: Impactor,
    target: Target,
    energy_seafloor: float = None,
    altitudeBurst: float = None,
    distance: float = None,
    surface_wave_v: float = None,
    delta: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if type is Choices.Collins:
        return collins_cal_magnitude2(
            impactor, target, altitudeBurst, energy_seafloor, delta
        )

    return None


def cal_shock_arrival(
    impactor: Impactor,
    target: Target,
    altitudeBurst: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if type is Choices.Collins:
        return collins_cal_shock_arrival(impactor, target, altitudeBurst)

    return None


def cal_vmax(
    impactor: Impactor,
    target: Target,
    energy_blast: float = None,
    altitudeBurst: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if type is Choices.Collins:
        return collins_cal_vmax(
            impactor, target, energy_blast, altitudeBurst
        )

    return None


def cal_shock_damage(impactor: Impactor, target: Target, opressure: float = None,
                     vmax: float = None, type: Choices = Choices.Collins,) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if type is Choices.Collins:
        return collins_cal_shock_damage(
            impactor, target, opressure, vmax
        )

    return None


def cal_dec_level(
    impactor: Impactor,
    target: Target,
    energy_blast: float = None,
    altitudeBurst: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if type is Choices.Collins:
        return collins_cal_dec_level(
            impactor, target, energy_blast, altitudeBurst
        )

    return None


def cal_TsunamiArrivalTime(
    impactor: Impactor,
    target: Target,
    wdiameter: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if type is Choices.Collins:
        return collins_cal_TsunamiArrivalTime(impactor, target, wdiameter)
    elif type is Choices.Example:
        return NotImplementedError("Error")

    return None


def cal_WaveAmplitudeUpperLimit(
    impactor: Impactor,
    target: Target,
    wdiameter: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if type is Choices.Collins:
        return collins_cal_WaveAmplitudeUpperLimit(
            impactor, target, wdiameter
        )

    return None


def cal_WaveAmplitudeLowerLimit(
    impactor: Impactor,
    target: Target,
    wdiameter: float = None,
    type: Choices = Choices.Collins,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if type is Choices.Collins:
        return collins_cal_WaveAmplitudeLowerLimit(
            impactor, target, wdiameter
        )

    return None
