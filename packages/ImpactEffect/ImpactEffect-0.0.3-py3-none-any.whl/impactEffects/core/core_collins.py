# -*- encoding: utf-8 -*-
"""
Filename         :core.py
Description      :
Time             :2022/07/10 09:37:51
Author           :daniel
Version          :1.0
"""
import logging

from impactEffects.instances.ImpactorClass import *
from impactEffects.instances.TargetClass import *
from impactEffects.core.config import *


def collins_kinetic_energy(impactor: Impactor) -> float:
    """

    Arguments
    ---------
    impactor: Instance of Impactor, containning

    Returns
    -------

    """

    return impactor.get_energy0()


def collins_kinetic_energy_megatons(impactor: Impactor) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """

    return impactor.get_energy0_megatons()


def collins_rec_time(impactor: Impactor) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """

    mass = impactor.get_mass()

    # Compute the recurrence interval for this energy impact
    # New model (after Bland and Artemieva (2006) MAPS 41 (607-621).
    if mass < 3:
        rec_time = 10 ** (-4.568) * mass ** 0.480
    elif mass < 1.7e10:
        rec_time = 10 ** (-4.739) * mass ** 0.926
    elif mass < 3.3e12:
        rec_time = 10 ** (0.922) * mass ** 0.373
    elif mass < 8.4e14:
        rec_time = 10 ** (-0.086) * mass ** 0.454
    else:
        rec_time = 10 ** (-3.352) * mass ** 0.672

    energy0_megatons = impactor.get_energy0_megatons()
    rec_time = max(rec_time, 110 * (energy0_megatons) ** 0.77)

    return rec_time


def collins_cal_iFactor(impactor: Impactor, target: Target) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """

    (
        pdensity,
        dragC,
        rhoSurface,
        scaleHeight,
        pdiameter,
        velocity,
        theta,
        fp,
    ) = (
        impactor.get_density(),
        target.get_dragC(),
        target.get_rhoSurface(),
        target.get_schaleHeight(),
        impactor.get_pdiameter(),
        impactor.get_velocity(),
        impactor.get_theta(),
        target.get_fp(),
    )

    # Approximate the strength of the impactor using the density function in
    # Eq. 9 of Collins et al. (2005)
    _yield = 10 ** (2.107 + 0.0624 * pdensity ** (1 / 2))
    # Define a relative strength of the impactor compared to the
    # maximum possible stagnation pressure on entry
    _rStrength = _yield / (rhoSurface * (velocity * 1000) ** 2)
    # Define the exponent of Eq. 8 for the case of impat at the surface
    _av = (
        3
        * rhoSurface
        * dragC
        * scaleHeight
        / (4 * pdensity * pdiameter * math.sin(theta * PI / 180))
    )

    collins_iFactor = 2.7185 * _av * _rStrength
    return collins_iFactor, _av, _rStrength


def collins_burst_velocity_at_zero(
    impactor: Impactor, target: Target
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    i_factor, _av, _ = collins_cal_iFactor(impactor, target)

    # check
    if i_factor < 1:
        logging.warning("I_factor should be greater than 1!")
        return None

    # Burst altitude is zero
    altitudeBurst = 0
    # Define the terminal velocity
    # Assuming drag coefficient of 2
    _vTerminal = min(
        impactor.get_velocity(),
        (
            4
            * impactor.density
            * impactor.pdiameter
            * target.g
            / (3 * target.rhoSurface * target.dragC)
        )
        ** (1 / 2),
    )

    # Define the surface velocity assuming continual spreading using Eq. 8
    _vSurface = impactor.vInput * 1000 * math.exp(-_av)

    # Take the maximum of the extrapolated surface velocity
    # and the terminal velocity
    if _vTerminal > _vSurface:
        velocity_at_surface = _vTerminal
    else:
        velocity_at_surface = _vSurface

    return velocity_at_surface/1000


def collins_altitude_of_breakup(
    impactor: Impactor,
    target: Target,
    collins_iFactor: float = None,
    rStrength: float = None,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """

    if collins_iFactor is None or rStrength is None:
        collins_iFactor, av, rStrength = collins_cal_iFactor(
            impactor, target
        )

    # Compute the first term in Eq. 11
    altitude1 = -target.schaleHeight * log(rStrength)

    # Define the second, third and fourth terms (inside the brackets) in Eq. 11
    omega = (
        1.308
        - 0.314 * collins_iFactor
        - 1.303 * (1 - collins_iFactor) ** 0.5
    )

    # Compute the breakup altitude by
    # combining above parameters to evaluate Eq. 11
    altitudeBU = altitude1 - omega * target.schaleHeight

    return altitudeBU


def collins_velocity_at_breakup(
    impactor: Impactor,
    target: Target,
    av: float = None,
    altitudeBU: float = None,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if av is None:
        collins_iFactor, av, rStrength = collins_cal_iFactor(
            impactor, target
        )

    if altitudeBU is None:
        altitudeBU = collins_altitude_of_breakup(
            impactor, target, collins_iFactor
        )

    # m/s
    return (
        impactor.velocity
        * 1000
        * exp(-av * math.exp(-altitudeBU / target.schaleHeight))
    )


def collins_dispersion_length_scale(
    impactor: Impactor, target: Target, altitudeBU: float = None
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if altitudeBU is None:
        altitudeBU = collins_altitude_of_breakup(impactor, target)

    # Assuming drag coefficient of 2
    return (
        impactor.pdiameter
        * sin(impactor.theta * PI / 180)
        * (impactor.density / (target.dragC * target.rhoSurface)) ** 0.5
        * exp(altitudeBU / (2 * target.schaleHeight))
    )


def collins_airburst_altitude(
    impactor: Impactor,
    target: Target,
    alpha2: float = None,
    lDisper: float = None,
    altitudeBU: float = None,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if altitudeBU is None:
        i_factor, _, _rStrength = collins_cal_iFactor(impactor, target)
        altitudeBU = collins_altitude_of_breakup(
            impactor, target, i_factor, _rStrength
        )

    if lDisper is None:
        lDisper = collins_dispersion_length_scale(
            impactor, target, altitudeBU
        )

    if alpha2 is None:
        alpha2 = (target.get_fp() ** 2 - 1) ** (1 / 2)

    # Define the burst altitude using Eq. 18
    altitudePen = (
        2
        * target.get_schaleHeight()
        * log(1 + alpha2 * lDisper / (2 * target.get_schaleHeight()))
    )
    altitudeBurst = altitudeBU - altitudePen
    return altitudeBurst


def collins_brust_velocity(
    impactor: Impactor,
    target: Target,
    altitudeBurst: float = None,
    altitudeBU: float = None,
    vBu: float = None,
    lDisper: float = None,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """

    if altitudeBU is None:
        i_factor, _av, _rStrength = collins_cal_iFactor(impactor, target)
        altitudeBU = collins_altitude_of_breakup(
            impactor, target, i_factor, _rStrength
        )

    if vBu is None:
        i_factor, _av, _rStrength = collins_cal_iFactor(impactor, target)
        vBU = collins_velocity_at_breakup(impactor, target, _av, altitudeBU)

    if lDisper is None:
        lDisper = collins_dispersion_length_scale(
            impactor, target, altitudeBU
        )

    alpha2 = (target.get_fp() ** 2 - 1) ** (1 / 2)
    if altitudeBurst is None:
        altitudeBurst = collins_airburst_altitude(
            impactor, target, alpha2, lDisper, altitudeBU
        )

    # Define factor for evaluating Eq. 17
    vFac = (
        0.75
        * (
            target.get_dragC()
            * target.get_rhoSurface()
            / impactor.get_density()
        )
        ** 0.5
        * exp(-altitudeBU / (2 * target.get_schaleHeight()))
    )  # Assuming drag coefficient of 2

    if altitudeBurst > 0:
        # Evaluate Eq. 19 (without factor lL_0^2 l_disper * pdiameter**2)
        expfac = (
            1
            / 24
            * alpha2
            * (
                24
                + 8 * alpha2 ** 2
                + 6 * alpha2 * lDisper / target.get_schaleHeight()
                + 3 * alpha2 ** 3 * lDisper / target.get_schaleHeight()
            )
        )

        # Evaluate velocity at burst using Eq. 17
        # (note that factor l_disper * pdiameter**2
        # in expfac cancels with same factor in vFac)
        velocity = vBU * exp(-expfac * vFac)
    else:
        # Define (l/H) for use in Eq. 20
        altitudeScale = target.get_schaleHeight() / lDisper

        # Evaluate Eq. 20 (without factor lL_0^2 l_disper * pdiameter**2)
        # (note that this Eq. is not correct in the paper)
        integral = (
            altitudeScale ** 3
            / 3
            * (
                3
                * (4 + 1 / altitudeScale ** 2)
                * exp(altitudeBU / target.get_schaleHeight())
                + 6 * exp(2 * altitudeBU / target.get_schaleHeight())
                - 16 * exp(1.5 * altitudeBU / target.get_schaleHeight())
                - 3 / altitudeScale ** 2
                - 2
            )
        )

        # Evaluate velocity at the surface using Eq. 17
        velocity = vBU * exp(-vFac * integral)

    return velocity / 1000


def collins_dispersion_of_impactor(
    impactor: Impactor,
    target: Target,
    l_disper: float = None,
    altitude_bu: float = None,
    altitude_burst: float = None,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """

    if altitude_bu is None:
        i_factor, _av, _rStrength = collins_cal_iFactor(impactor, target)
        altitude_bu = collins_altitude_of_breakup(
            impactor, target, i_factor, _rStrength
        )

    if l_disper is None:
        l_disper = collins_dispersion_length_scale(
            impactor, target, altitude_bu
        )

    if altitude_burst is None:
        alpha2 = (target.get_fp() ** 2 - 1) ** (1 / 2)
        altitude_burst = collins_airburst_altitude(
            impactor, target, alpha2, l_disper, altitude_bu
        )

    if altitude_burst > 0:
        # raise ValueError("Impactor is not dispersionless at the surface")
        return 0

    dispersion = impactor.get_pdiameter() * (
        1
        + 4
        * (target.get_schaleHeight() / l_disper) ** 2
        * (exp(altitude_bu / (2 * target.get_schaleHeight())) - 1) ** 2
    ) ** (1 / 2)

    return dispersion


def collins_fraction_of_momentum(
    impactor: Impactor, target: Target, velocity: float = None
):
    """

    Arguments
    ---------


    Returns
    -------

    """

    if velocity is None:
        velocity = collins_brust_velocity(impactor, target)

    linmom = impactor.get_mass() * (velocity * 1000)
    angmom = (
        impactor.get_mass()
        * (velocity * 1000)
        * cos(impactor.get_theta() * PI / 180)
        * target.get_R_earth()
    )

    # relativistic effects, multiply energy by 1/sqrt(1 - v^2/c^2)
    if impactor.get_velocity() > (0.25 * 3 * 10 ** 5):
        beta = 1 / (1 - impactor.get_velocity() ** 2 / 9 * 10 ** 10) ** 0.5
        energy0 = impactor.energy0 * beta
        linmom *= beta
        angmom *= beta

    lratio = angmom / target.get_lEarth()
    pratio = linmom / target.get_pEarth()
    return lratio, pratio


def collins_cal_trot_change(
    impactor: Impactor, target: Target, velocity: float = None
):
    """

    Arguments
    ---------


    Returns
    -------

    """

    if velocity is None:
        velocity = collins_brust_velocity(impactor, target)

    mass = impactor.get_mass()
    mEarth = target.get_mEarth()
    theta = impactor.get_theta()
    R_earth = target.get_R_earth()

    return (
        (1.25 / PI)
        * (mass / mEarth)
        * cos(theta * PI / 180)
        / R_earth
        * velocity
        * (24.0 * 60.0 * 60.0) ** 2
    )


def collins_cal_energy_atmosphere(
    impactor: Impactor, target: Target, velocity: float = None
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """

    if velocity is None:
        velocity = collins_brust_velocity(impactor, target)

    # print("velocity: ", velocity, " origin_vel:", impactor.get_velocity())
    energy_atmosphere = (
        0.5
        * impactor.get_mass()
        * ((impactor.get_velocity() * 1000) ** 2 - (velocity * 1000) ** 2)
    )
    return energy_atmosphere


def collins_cal_energy_blast_surface(
    impactor: Impactor,
    target: Target,
    velocity: float = None,
    altitudeBurst: float = None,
    energy_atmosphere: float = None,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if altitudeBurst is None or velocity is None:
        i_factor, _av, _rStrength = collins_cal_iFactor(impactor, target)
        altitudeBU = collins_altitude_of_breakup(
            impactor, target, i_factor, _rStrength
        )
        lDisper = collins_dispersion_length_scale(
            impactor, target, altitudeBU
        )

        alpha2 = (target.get_fp() ** 2 - 1) ** (1 / 2)
        altitudeBurst = collins_airburst_altitude(
            impactor, target, alpha2, lDisper, altitudeBU
        )
        velocity = collins_brust_velocity(
            impactor, target, altitudeBurst, altitudeBU, None, lDisper
        )

    if energy_atmosphere is None:
        energy_atmosphere = collins_cal_energy_atmosphere(
            impactor, target, velocity
        )

    if altitudeBurst > 0:
        # Blast energy is airburst energy (kTons)
        energy_blast = energy_atmosphere / (4.186 * 10 ** 12)
        energy_surface = energy_atmosphere
    else:
        altitudeBurst = 0
        energy_surface = 0.5 * impactor.get_mass() * (velocity * 1000) ** 2
        # Blast energy is larger of airburt and impact energy (kTons)
        if energy_atmosphere > energy_surface:
            energy_blast = energy_atmosphere / (4.186 * 10 ** 12)
        else:
            energy_blast = energy_surface / (4.186 * 10 ** 12)

    return energy_blast, energy_surface


def collins_cal_mass_of_water(impactor: Impactor, target: Target) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """

    mwater = (
        (PI * impactor.get_pdiameter() ** 2 / 4)
        * (target.get_depth() / sin(impactor.get_theta() * PI / 180))
        * 1000
    )
    return mwater


def collins_cal_velocity_projectile(
    impactor: Impactor, target: Target, velocity: float = None
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """

    if velocity is None:
        velocity = collins_brust_velocity(impactor, target)

    vseafloor = velocity * exp(
        -(3 * 1000 * 0.877 * target.get_depth())
        / (
            2
            * impactor.get_density()
            * impactor.get_pdiameter()
            * sin(impactor.get_theta() * PI / 180)
        )
    )
    return vseafloor


def collins_cal_energy_at_seafloor(
    impactor: Impactor, target: Target, vseafloor: float = None
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if vseafloor is None:
        vseafloor = collins_cal_velocity_projectile(impactor, target)

    energy_seafloor = 0.5 * impactor.get_mass() * (vseafloor * 1000) ** 2
    return energy_seafloor


def collins_cal_ePIcentral_angle(target: Target) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """

    return (180 / PI) * (target.get_distance() / target.get_R_earth())


def collins_cal_scaling_diameter_constant(target: Target) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """

    if target.ttype == 1:
        Cd = 1.88
        beta = 0.22
    elif target.ttype == 2:
        Cd = 1.54
        beta = 0.165
    else:
        Cd = 1.6
        beta = 0.22
    return Cd, beta


def collins_cal_anglefac(impactor: Impactor) -> float:
    return (sin(impactor.get_theta() * PI / 180)) ** (1 / 3)


def collins_cal_wdiameter(
    impactor: Impactor,
    target: Target,
    anglefac: float = None,
    velocity: float = None,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if target.depth == 0:
        logging.warning("Target depth is 0")
        exit(0)

    if velocity is None:
        velocity = collins_brust_velocity(impactor, target)

    if anglefac is None:
        anglefac = collins_cal_anglefac(impactor)

    mass, tdensity, g, pdiameter = (
        impactor.get_mass(),
        target.get_density(),
        target.get_g(),
        impactor.get_pdiameter(),
    )

    wdiameter = (
        1.88
        * ((mass / tdensity) ** (1 / 3))
        * ((1.61 * g * pdiameter) / (velocity * 1000) ** 2) ** (-0.22)
    )
    wdiameter *= anglefac

    # update tdensity which should be return as value
    logging.log(
        logging.INFO,
        "update the impactor density for seafloor: %f".format(wdiameter),
    )

    return wdiameter


def collins_cal_transient_crater_diameter(
    impactor: Impactor,
    target: Target,
    Cd: float = None,
    beta: float = None,
    anglefac: float = None,
    vseafloor: float = None,
    dispersion: float = None,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if Cd is None or beta is None:
        Cd, beta = collins_cal_scaling_diameter_constant(target=target)

    if anglefac is None:
        anglefac = collins_cal_anglefac(impactor)

    if vseafloor is None:
        vseafloor = collins_cal_velocity_projectile(impactor, target)

    if dispersion is None:
        dispersion = collins_dispersion_of_impactor(impactor, target)

    mass, g, pdiameter = (
        impactor.get_mass(),
        target.get_g(),
        impactor.get_pdiameter(),
    )

    if target.depth != 0:
        tdensity = target.seefloor_density
    else:
        tdensity = target.density

    # print(
    #     "mass: {, tdensity: {, g: {, pdiameter: {".format(
    #         mass, tdensity, g, pdiameter
    #     )
    # )
    Dtr = (
        Cd
        * ((mass / tdensity) ** (1 / 3))
        * ((1.61 * g * pdiameter) / (vseafloor * 1000) ** 2) ** (-beta)
    )
    Dtr *= anglefac

    if (
        dispersion >= Dtr
    ):  # if crater field is formed, compute crater dimensions assuming
        Dtr /= 2
        # impact of largest fragment (with diameter = 1/2 initial diameter)

    return Dtr


def collins_cal_depthr(
    impactor: Impactor, target: Target, Dtr: float = None
):
    """

    Arguments
    ---------


    Returns
    -------

    """
    if Dtr is None:
        Dtr = collins_cal_transient_crater_diameter(impactor, target)

    return Dtr / 2.828


def collins_cal_cdiamater(
    impactor: Impactor, target: Target, Dtr: float = None
):
    """

    Arguments
    ---------


    Returns
    -------

    """
    if Dtr is None:
        Dtr = collins_cal_transient_crater_diameter(impactor, target)

    if Dtr * 1.25 >= 3200:
        cdiameter = (1.17 * Dtr ** 1.13) / (3200 ** 0.13)
    else:
        cdiameter = 1.25 * Dtr

    return cdiameter


def collins_cal_depthfr(
    impactor: Impactor,
    target: Target,
    Dtr: float = None,
    depthtr: float = None,
    cdiameter: float = None,
):
    """

    Arguments
    ---------


    Returns
    -------

    """
    if Dtr is None:
        Dtr = collins_cal_transient_crater_diameter(impactor, target)
    if depthtr is None:
        depthtr = collins_cal_depthr(impactor, target, Dtr)
    if cdiameter is None:
        cdiameter = collins_cal_cdiamater(impactor, target, Dtr)

    if Dtr * 1.25 >= 3200:
        depthfr = 37 * cdiameter ** 0.301
    else:
        # Breccia lens volume in m^3
        vbreccia = 0.032 * cdiameter ** 3  # in m^3

        # Rim height of final crater in m
        rimHeightf = 0.07 * Dtr ** 4 / cdiameter ** 3

        # Thickness of breccia lens in m
        brecciaThickness = (
            2.8
            * vbreccia
            * ((depthtr + rimHeightf) / (depthtr * cdiameter ** 2))
        )

        # Final crater depth (in m) = transient crater depth +
        # final rim height - breccia thickness
        depthfr = depthtr + rimHeightf - brecciaThickness

    return depthfr


def collins_cal_vCrater(
    impactor: Impactor, target: Target, Dtr: float = None
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if Dtr is None:
        Dtr = collins_cal_transient_crater_diameter(impactor, target)

    return (PI / 24) * (Dtr / 1000) ** 3


def collins_cal_vCrater_vRation(
    impactor: Impactor, target: Target, Dtr: float = None
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if Dtr is None:
        Dtr = collins_cal_transient_crater_diameter(impactor, target)

    vCrater = (PI / 24) * (Dtr / 1000) ** 3
    vRatio = vCrater / target.get_v_earth()
    return vCrater, vRatio


def collins_cal_vMelt(
    impactor: Impactor,
    target: Target,
    velocity: float = None,
    energy_seafloor: float = None,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if velocity is None:
        velocity = collins_brust_velocity(impactor, target)

    if energy_seafloor is None:
        energy_seafloor = collins_cal_energy_at_seafloor(impactor, target)

    if velocity < 12:
        logging.warning("Velocity is less than 12 m/s")
        return None

    vMelt = (
        target.get_melt_coeff()
        * (energy_seafloor)
        * sin(impactor.get_theta() * PI / 180)
    )
    if vMelt > target.vEarth:
        vMelt = target.get_v_earth()

    return vMelt


def collins_cal_mratio_and_mcratio(
    impactor: Impactor,
    target: Target,
    velocity: float = None,
    vMelt: float = None,
    vCrater: float = None,
    Dtr: float = None,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if velocity is None:
        velocity = collins_brust_velocity(impactor, target)

    if velocity < 12:
        logging.warning("Velocity is less than 12 m/s")
        return None, None

    if Dtr is None:
        Dtr = collins_cal_transient_crater_diameter(impactor, target)
    if vMelt is None:
        vMelt = collins_cal_vMelt(impactor, target)
    if vCrater is None:
        vCrater = collins_cal_vCrater(impactor, target, Dtr)

    mcratio = vMelt / vCrater
    mratio = vMelt / target.get_v_earth()
    return mratio, mcratio


def collins_cal_eject_arrival(
    impactor: Impactor, target: Target, altitudeBurst: float = None
):
    """

    Arguments
    ---------


    Returns
    -------

    """
    if altitudeBurst is None:
        i_factor, _av, _rStrength = collins_cal_iFactor(impactor, target)
        altitudeBU = collins_altitude_of_breakup(
            impactor, target, i_factor, _rStrength
        )
        lDisper = collins_dispersion_length_scale(
            impactor, target, altitudeBU
        )

        alpha2 = (target.get_fp() ** 2 - 1) ** (1 / 2)
        altitudeBurst = collins_airburst_altitude(
            impactor, target, alpha2, lDisper, altitudeBU
        )

    if altitudeBurst > 0:
        logging.warning("Altitude of burst is greater than 0")
        return None

    phi = (target.get_distance()) / (2 * target.get_R_earth())
    X = (2 * tan(phi)) / (1 + tan(phi))
    # eccentricity of eliptical path of the ejecta
    e = -((0.5 * (X - 1) ** 2 + 0.5) ** 0.5)
    a = (X * target.get_R_earth() * 1000) / (
        2 * (1 - e ** 2)
    )  # semi major axis of elliptical path

    part1 = (
        a ** 1.5
        / (target.get_g() * (target.get_R_earth() * 1000) ** 2) ** 0.5
    )
    term1 = 2 * atan(((1 - e) / (1 + e)) ** 0.5 * tan(phi / 2))
    term2 = e * (1 - e ** 2) ** 0.5 * sin(phi) / (1 + e * cos(phi))
    ejecta_arrival = 2 * part1 * (term1 - term2)

    return ejecta_arrival


def collins_cal_ejecta_thickness(
    impactor: Impactor,
    target: Target,
    altitudeBurst: float = None,
    Dtr: float = None,
):
    """

    Arguments
    ---------


    Returns
    -------

    """
    if altitudeBurst is None:
        i_factor, _av, _rStrength = collins_cal_iFactor(impactor, target)
        altitudeBU = collins_altitude_of_breakup(
            impactor, target, i_factor, _rStrength
        )
        lDisper = collins_dispersion_length_scale(
            impactor, target, altitudeBU
        )

        alpha2 = (target.get_fp() ** 2 - 1) ** (1 / 2)
        altitudeBurst = collins_airburst_altitude(
            impactor, target, alpha2, lDisper, altitudeBU
        )

    if Dtr is None:
        Dtr = collins_cal_transient_crater_diameter(impactor, target)

    if altitudeBurst > 0:
        logging.warning("Altitude of burst is greater than 0")
        return None

    print("Dtr: ", Dtr, " distance: ", target.distance)
    ejecta_thickness = Dtr ** 4 / (
        112 * (target.get_distance() * 1000) ** 3
    )
    return ejecta_thickness


def collins_cal_d_frag(impactor: Impactor, target: Target, cdiameter: float = None, altitudeBurst: float = None, Dtr: float = None) -> float:

    if altitudeBurst is None:
        i_factor, _av, _rStrength = collins_cal_iFactor(impactor, target)
        altitudeBU = collins_altitude_of_breakup(
            impactor, target, i_factor, _rStrength
        )
        lDisper = collins_dispersion_length_scale(
            impactor, target, altitudeBU
        )

        alpha2 = (target.get_fp() ** 2 - 1) ** (1 / 2)
        altitudeBurst = collins_airburst_altitude(
            impactor, target, alpha2, lDisper, altitudeBU
        )

    if altitudeBurst > 0:
        logging.warning("Altitude of burst is greater than 0")
        exit(1)

    if Dtr is None:
        Dtr = collins_cal_transient_crater_diameter(impactor, target)
    if cdiameter is None:
        cdiameter = collins_cal_cdiamater(impactor, target, Dtr)

    # compute mean fragment size
    a2 = 2.65
    half_diameter = (cdiameter/1000)/2  # half of final crater diameter in km
    dc = 2400 * half_diameter**-1.62

    d_frag = dc*(half_diameter/target.distance)**a2

    return d_frag


def collins_cal_themal(
    impactor: Impactor,
    target: Target,
    energy_surface: float = None,
    altitudeBurst: float = None,
    delta: float = None,
    velocity: float = None,
):
    """

    Arguments
    ---------


    Returns
    -------

    """

    if altitudeBurst is None:
        i_factor, _av, _rStrength = collins_cal_iFactor(impactor, target)
        altitudeBU = collins_altitude_of_breakup(
            impactor, target, i_factor, _rStrength
        )
        lDisper = collins_dispersion_length_scale(
            impactor, target, altitudeBU
        )

        alpha2 = (target.get_fp() ** 2 - 1) ** (1 / 2)
        altitudeBurst = collins_airburst_altitude(
            impactor, target, alpha2, lDisper, altitudeBU
        )

    if velocity is None:
        velocity = collins_brust_velocity(
            impactor,
            target,
            altitudeBurst=altitudeBurst,
            altitudeBU=altitudeBU,
            lDisper=lDisper,
        )

    if energy_surface is None:
        _, energy_surface = collins_cal_energy_blast_surface(
            impactor, target
        )

    if delta is None:
        delta = collins_cal_ePIcentral_angle(target=target)

    if altitudeBurst > 0:
        logging.warning("Altitude of burst is greater than 0")

        return (
            None, None,
            None,
            None,
            None,
            None,
            None,
        )

    energy_megatons = energy_surface / (4.186 * 10 ** 15)
    eta = 3 * 10 ** -3  # factor for scaling thermal energy
    T_star = 3000  # temperature of fireball
    Rf = 2 * 10 ** -6 * (energy_surface) ** (1 / 3)  # Rf is in km
    sigma = 5.67 * 10 ** -8  # Stephan-Boltzmann constant

    thermal_exposure = (eta * energy_surface) / (
        2 * PI * (target.get_distance() * 1000) ** 2
    )

    # h is in km, R_earth is in km
    h = (1 - cos(delta * PI / 180)) * target.get_R_earth()
    Del = acos(h / Rf)
    f = (2 / PI) * (Del - (h / Rf) * sin(Del))

    if h > Rf:
        no_radiation = 1
        return thermal_exposure, no_radiation

    no_radiation = 0
    thermal_exposure *= f

    max_rad_time = Rf / velocity  # Rf in km / velocity in km/s
    irradiation_time = (eta * energy_surface) / (
        2 * PI * (Rf * 1000) ** 2 * sigma * T_star ** 4
    )

    megaton_factor = (energy_megatons) ** (1 / 6)

    thermal_power = log(thermal_exposure) / log(10)
    thermal_power = int(thermal_power)
    thermal_exposure /= 10 ** thermal_power

    return (
        h,
        Rf,
        thermal_exposure,
        no_radiation,
        max_rad_time,
        irradiation_time,
        megaton_factor,
        thermal_power,
    )


def collins_cal_magnitude(
    impactor: Impactor,
    target: Target,
    altitudeBurst: float = None,
    energy_seafloor: float = None,
):
    """

    Arguments
    ---------


    Returns
    -------

    """
    if altitudeBurst is None:
        i_factor, _av, _rStrength = collins_cal_iFactor(impactor, target)
        altitudeBU = collins_altitude_of_breakup(
            impactor, target, i_factor, _rStrength
        )
        lDisper = collins_dispersion_length_scale(
            impactor, target, altitudeBU
        )

        alpha2 = (target.get_fp() ** 2 - 1) ** (1 / 2)
        altitudeBurst = collins_airburst_altitude(
            impactor, target, alpha2, lDisper, altitudeBU
        )

    if energy_seafloor is None:
        energy_seafloor = collins_cal_energy_at_seafloor(impactor, target)

    if altitudeBurst > 0:
        logging.warning("Altitude of burst is greater than 0")
        return None

    magnitude = 0.67 * ((log(energy_seafloor)) / (log(10))) - 5.87
    return magnitude


def collins_cal_magnitude2(
    impactor: Impactor,
    target: Target,
    energy_seafloor: float = None,
    altitudeBurst: float = None,
    delta: float = None,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if altitudeBurst is None:
        i_factor, _av, _rStrength = collins_cal_iFactor(impactor, target)
        altitudeBU = collins_altitude_of_breakup(
            impactor, target, i_factor, _rStrength
        )
        lDisper = collins_dispersion_length_scale(
            impactor, target, altitudeBU
        )

        alpha2 = (target.get_fp() ** 2 - 1) ** (1 / 2)
        altitudeBurst = collins_airburst_altitude(
            impactor, target, alpha2, lDisper, altitudeBU
        )

    if energy_seafloor is None:
        energy_seafloor = collins_cal_energy_at_seafloor(impactor, target)

    if delta is None:
        delta = collins_cal_ePIcentral_angle(target=target)

    if altitudeBurst > 0:
        logging.warning("Altitude of burst is greater than 0")
        return None, None

    Ax = 0  # factor for determining "effective magnitude" at given distance
    magnitude = collins_cal_magnitude(
        impactor,
        target,
        altitudeBurst=altitudeBurst,
        energy_seafloor=energy_seafloor,
    )
    distance = target.distance
    surface_wave_v = target.surface_wave_v

    if distance >= 700:
        Ax = 20 * 10 ** (magnitude - 1.66 * (log(delta) / log(10)) - 3.3)
        Ax /= 1000
    elif distance >= 60:
        Ax = 10 ** (magnitude - (0.0048 * distance + 2.5644))

    else:
        Ax = 10 ** (magnitude - (0.00238 * distance + 1.3342))

    eff_mag = (log(Ax) / log(10)) + 1.4
    seismic_arrival = distance / surface_wave_v

    return eff_mag, seismic_arrival


def collins_cal_shock_arrival(
    impactor: Impactor, target: Target, altitudeBurst: float = None
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if altitudeBurst is None:
        i_factor, _av, _rStrength = collins_cal_iFactor(impactor, target)
        altitudeBU = collins_altitude_of_breakup(
            impactor, target, i_factor, _rStrength
        )
        lDisper = collins_dispersion_length_scale(
            impactor, target, altitudeBU
        )

        alpha2 = (target.get_fp() ** 2 - 1) ** (1 / 2)
        altitudeBurst = collins_airburst_altitude(
            impactor, target, alpha2, lDisper, altitudeBU
        )

    vsound = 330  # speed of sound in m/s
    slantRange = 0  # in km

    # Arrival time is straight line distance divided by sound speed
    # for air burst, distance is slant range from explosion
    slantRange = (
        target.get_distance() ** 2 + (altitudeBurst / 1000) ** 2
    ) ** (1 / 2)
    # distance in meters divided by velocity of sound in m/s
    shock_arrival = (slantRange * 1000) / vsound

    return shock_arrival


def collins_cal_vmax(
    impactor: Impactor,
    target: Target,
    energy_blast: float = None,
    altitudeBurst: float = None,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if altitudeBurst is None:
        i_factor, _av, _rStrength = collins_cal_iFactor(impactor, target)
        altitudeBU = collins_altitude_of_breakup(
            impactor, target, i_factor, _rStrength
        )
        lDisper = collins_dispersion_length_scale(
            impactor, target, altitudeBU
        )

        alpha2 = (target.get_fp() ** 2 - 1) ** (1 / 2)
        altitudeBurst = collins_airburst_altitude(
            impactor, target, alpha2, lDisper, altitudeBU
        )

    if energy_blast is None:
        energy_blast, _ = collins_cal_energy_blast_surface(
            impactor, target, altitudeBurst=altitudeBurst
        )

    Po = target.get_Po()
    vsound = 330  # speed of sound in m/s
    r_cross = 0
    # radius at which relationship between overpressure and distance changes
    # radius at which relationship between
    # overpressure and distance changes (for surface burst)
    r_cross0 = 290
    op_cross = 75000  # overpressure at crossover
    energy_ktons = 0  # energy in kilotons
    d_scale = 0  # distance scaled for 1 kTon blast
    d_smooth = 0
    p_machT = 0
    p_regT = 0

    # energy_ktons = 1000 * energy_megatons
    energy_ktons = energy_blast

    # Scale distance to equivalent for a kiloton explosion
    sf = (energy_ktons) ** (1 / 3)
    d_scale = (target.get_distance() * 1000) / sf

    # Scale burst altitude to equivalent for a kiloton explosion
    z_scale = altitudeBurst / sf
    r_cross = r_cross0 + 0.65 * z_scale
    r_mach = 550 * z_scale / (1.2 * (550 - z_scale))
    if z_scale >= 550:
        r_mach = 1e30

    if altitudeBurst > 0:
        d_smooth = z_scale ** 2 * 0.00328
        p_machT = (
            ((r_cross * op_cross) / 4)
            * (1 / (r_mach + d_smooth))
            * (1 + 3 * (r_cross / (r_mach + d_smooth)) ** (1.3))
        )
        p_regT = 3.14e11 * ((r_mach - d_smooth) ** 2 + z_scale ** 2) ** (
            -1.3
        ) + 1.8e7 * ((r_mach - d_smooth) ** 2 + z_scale ** 2) ** (-0.565)
    else:
        d_smooth = 0
        p_machT = 0

    if d_scale >= (r_mach + d_smooth):
        opressure = (
            ((r_cross * op_cross) / 4)
            * (1 / d_scale)
            * (1 + 3 * (r_cross / d_scale) ** (1.3))
        )
    elif d_scale <= (r_mach - d_smooth):
        opressure = 3.14e11 * (d_scale ** 2 + z_scale ** 2) ** (
            -1.3
        ) + 1.8e7 * (d_scale ** 2 + z_scale ** 2) ** (-0.565)
    else:
        opressure = (
            p_regT
            - (d_scale - r_mach + d_smooth)
            * 0.5
            * (p_regT - p_machT)
            / d_smooth
        )

    # Wind velocity
    vmax = ((5 * opressure) / (7 * Po)) * (
        vsound / (1 + (6 * opressure) / (7 * Po)) ** (1 / 2)
    )

    return vmax, opressure


def collins_cal_shock_damage(impactor: Impactor, target: Target, opressure: float = None, vmax: float = None) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """

    if opressure == None or vmax == None:
        vmax, opressure = collins_cal_vmax(impactor=impactor, target=target)

    # damage descriptions:  structures
    shock_damage = ""
    if opressure >= 42600:
        shock_damage += "Multistory wall-bearing buildings will collapse.\n"
    elif opressure >= 38500:
        shock_damage += " Multistory wall-bearing buildings will experience severe cracking and interior partitions will be blown down\n"

    if opressure >= 26800:
        shock_damage += " Wood frame buildings will almost completely collapse.\n"
    elif opressure >= 22900:
        shock_damage += " Interior partitions of wood frame buildings will be blown down.  Roof will be severely damaged.\n"

    if opressure >= 273000:
        shock_damage += " Multistory steel-framed office-type buildings will suffer extreme frame distortion, incipient collapse.\n"

    if opressure >= 121000:
        shock_damage += " Highway truss bridges will collapse.\n"
    elif opressure >= 100000:
        shock_damage += " Highway truss bridges will suffer substantial distortion of bracing.\n"

    if opressure >= 379000:
        shock_damage += " Highway girder bridges will collapse.\n"

    # damage descriptions:  glass, transportation, forrests
    if opressure >= 6900:
        shock_damage += " Glass windows will shatter.\n"
    elif opressure >= 690:
        shock_damage += " Glass windows may shatter.\n"

    if opressure >= 426000:
        shock_damage += " Cars and trucks will be largely displaced and grossly distorted and will require rebuilding before use.\n"
    elif opressure >= 297000:
        shock_damage += " Cars and trucks will be overturned and displaced, requiring major repairs.\n"

    if vmax >= 62:
        shock_damage += " Up to 90 percent of trees blown down remainder stripped of branches and leaves.\n"
    elif vmax >= 40:
        shock_damage += " About 30 percent of trees blown down remainder have some branches and leaves blown off.\n"

    return shock_damage


def collins_cal_dec_level(
    impactor: Impactor,
    target: Target,
    energy_blast: float = None,
    altitudeBurst: float = None,
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if altitudeBurst is None:
        i_factor, _av, _rStrength = collins_cal_iFactor(impactor, target)
        altitudeBU = collins_altitude_of_breakup(
            impactor, target, i_factor, _rStrength
        )
        lDisper = collins_dispersion_length_scale(
            impactor, target, altitudeBU
        )

        alpha2 = (target.get_fp() ** 2 - 1) ** (1 / 2)
        altitudeBurst = collins_airburst_altitude(
            impactor, target, alpha2, lDisper, altitudeBU
        )

    if energy_blast is None:
        energy_blast, _ = collins_cal_energy_blast_surface(
            impactor, target, altitudeBurst=altitudeBurst
        )

    r_cross = 0
    # radius at which relationship between overpressure and distance changes
    # radius at which relationship between
    # overpressure and distance changes (for surface burst)
    r_cross0 = 290
    op_cross = 75000  # overpressure at crossover
    energy_ktons = 0  # energy in kilotons
    d_scale = 0  # distance scaled for 1 kTon blast
    d_smooth = 0
    p_machT = 0
    p_regT = 0

    # energy_ktons = 1000 * energy_megatons
    energy_ktons = energy_blast

    # Scale distance to equivalent for a kiloton explosion
    sf = (energy_ktons) ** (1 / 3)
    d_scale = (target.get_distance() * 1000) / sf

    # Scale burst altitude to equivalent for a kiloton explosion
    z_scale = altitudeBurst / sf
    r_cross = r_cross0 + 0.65 * z_scale
    r_mach = 550 * z_scale / (1.2 * (550 - z_scale))
    if z_scale >= 550:
        r_mach = 1e30

    if altitudeBurst > 0:
        d_smooth = z_scale ** 2 * 0.00328
        p_machT = (
            ((r_cross * op_cross) / 4)
            * (1 / (r_mach + d_smooth))
            * (1 + 3 * (r_cross / (r_mach + d_smooth)) ** (1.3))
        )
        p_regT = 3.14e11 * ((r_mach - d_smooth) ** 2 + z_scale ** 2) ** (
            -1.3
        ) + 1.8e7 * ((r_mach - d_smooth) ** 2 + z_scale ** 2) ** (-0.565)
    else:
        d_smooth = 0
        p_machT = 0

    if d_scale >= (r_mach + d_smooth):
        opressure = (
            ((r_cross * op_cross) / 4)
            * (1 / d_scale)
            * (1 + 3 * (r_cross / d_scale) ** (1.3))
        )
    elif d_scale <= (r_mach - d_smooth):
        opressure = 3.14e11 * (d_scale ** 2 + z_scale ** 2) ** (
            -1.3
        ) + 1.8e7 * (d_scale ** 2 + z_scale ** 2) ** (-0.565)
    else:
        opressure = (
            p_regT
            - (d_scale - r_mach + d_smooth)
            * 0.5
            * (p_regT - p_machT)
            / d_smooth
        )

    # sound intensity
    if opressure > 0:
        dec_level = 20 * (log(opressure) / log(10))
    else:
        dec_level = 0

    return dec_level


def collins_cal_TsunamiArrivalTime(
    impactor: Impactor, target: Target, wdiameter: float = None
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if wdiameter is None:
        wdiameter = collins_cal_wdiameter(impactor, target)

    TsunamiSpeed = 0  # Tsunami speed in m/s
    TsunamiWavelength = 0  # Tsunami wavelength in m

    # Tsunami arrival time assumes linear wave theory
    TsunamiWavelength = 2.0 * wdiameter
    # print("TsunamiWavelength: ", TsunamiWavelength)
    TsunamiSpeed = sqrt(
        0.5
        * target.get_g()
        * TsunamiWavelength
        / PI
        * tanh(2.0 * PI * target.get_depth() / TsunamiWavelength)
    )
    # print("TsunamiSpeed: ", TsunamiSpeed)
    TsunamiArrivalTime = target.get_distance() * 1000 / TsunamiSpeed

    return TsunamiArrivalTime


def collins_cal_WaveAmplitudeUpperLimit(
    impactor: Impactor, target: Target, wdiameter: float = None
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if wdiameter is None:
        wdiameter = collins_cal_wdiameter(impactor, target)

    MaxWaveAmplitude = 0  # Maximum rim wave amplitude
    MaxWaveRadius = (
        0  # Radius where max rim wave is formed (upper estimate)
    )
    RimWaveExponent = 0  # Attenuation factor for rim wave

    # Define parameters
    RimWaveExponent = 1.0
    MaxWaveRadius = 0.001 * wdiameter

    MaxWaveAmplitude = min(0.07 * wdiameter, target.get_depth())
    WaveAmplitudeUpperLimit = (
        MaxWaveAmplitude
        * (MaxWaveRadius / target.get_distance()) ** RimWaveExponent
    )

    return WaveAmplitudeUpperLimit


def collins_cal_WaveAmplitudeLowerLimit(
    impactor: Impactor, target: Target, wdiameter: float = None
) -> float:
    """

    Arguments
    ---------


    Returns
    -------

    """
    if wdiameter is None:
        wdiameter = collins_cal_wdiameter(impactor, target)

    shallowness = 0  # Ratio of Impactor diameter to water depth
    MaxWaveAmplitude = 0  # Maximum rim wave amplitude
    MinWaveRadius = (
        0  # Radius where max rim wave is formed (lower estimate)
    )
    CollapseWaveRadius = 0  # Radius where collapse wave is formed
    RimWaveExponent = 0  # Attenuation factor for rim wave
    CollapseWaveExponent = 0  # Attenuation factor for collapse wave
    MaxCollapseWaveAmplitude = 0  # Maximum collapse wave amplitude
    CollapseWaveAmplitude = (
        0  # Amplitude of collapse wave at specified distance
    )

    # Define parameters
    shallowness = impactor.get_pdiameter() / target.get_depth()
    RimWaveExponent = 1.0
    MinWaveRadius = 0.0005 * wdiameter

    MaxWaveAmplitude = min(0.07 * wdiameter, target.get_depth())
    WaveAmplitudeLowerLimit = (
        MaxWaveAmplitude
        * (MinWaveRadius / target.get_distance()) ** RimWaveExponent
    )

    # Collapse wave correction to lower limit for deep-water impacts
    if shallowness < 0.5:
        CollapseWaveExponent = 3.0 * exp(-0.8 * shallowness)
        CollapseWaveRadius = 0.0025 * wdiameter
        MaxCollapseWaveAmplitude = 0.06 * min(
            wdiameter / 2.828, target.get_depth()
        )
        CollapseWaveAmplitude = (
            MaxCollapseWaveAmplitude
            * (CollapseWaveRadius / target.get_distance())
            ** CollapseWaveExponent
        )
        WaveAmplitudeLowerLimit = min(
            CollapseWaveAmplitude, WaveAmplitudeLowerLimit
        )

    return WaveAmplitudeLowerLimit
