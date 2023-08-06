# -*- encoding: utf-8 -*-
"""
Filename         :impact.py
Description      :
Time             :2022/07/10 10:39:57
Author           :daniel
Version          :1.0
"""
from impactEffects.functions.function import *


def atmospheric_entry(impactor: Impactor, target: Target):
    """

    Arguments
    ---------


    Returns
    -------

    """

    i_factor, _av, _rStrength = iFactor(impactor, target)

    if i_factor >= 1:
        velocity_at_surface = burst_velocity_at_zero(impactor, target)
    else:
        # Compute the breakup altitude by
        # combining above parameters to evaluate Eq. 11
        altitudeBU = altitude_of_breakup(
            target.scaleHeight, _rStrength, i_factor
        )

        # Define velocity at breakup
        # altitude using Eq. 8 (and Eq. 5)
        vBU = velocity_at_breakup(
            impactor.get_velocity(),
            _av,
            altitudeBU,
            target.get_schaleHeight(),
        )

        # Define dispersion length-scale (Eq. 16)
        lDisper = dispersion_length_scale(
            impactor.get_pdiameter(),
            impactor.get_theta(),
            impactor.get_density(),
            target.get_dragC(),
            target.get_rhoSurface(),
            altitudeBU,
            target.get_schaleHeight(),
        )

        # Define the alpha parameters
        # used to evaluate Eq. 18 and Eq. 19
        alpha2 = (target.get_fp() ** 2 - 1) ** (1 / 2)

        # Define the burst altitude using Eq. 18
        altitudeBurst = airburst_altitude(
            impactor, target, alpha2, lDisper, altitudeBU
        )

        velocity_at_surface = brust_velocity(
            impactor, target, altitudeBurst, altitudeBU, vBU, lDisper
        )
        dispersion = dispersion_of_impactor(
            impactor, target, lDisper, altitudeBU, altitudeBurst
        )

    return (
        velocity_at_surface,
        i_factor,
        altitudeBU,
        altitudeBurst,
        dispersion,
    )


def calc_energy(impactor: Impactor, target: Target):
    """
    Implement equation (1)
    """
    mass, energy0, energy0_megatons, theta, R_earth = (
        impactor.get_mass(),
        impactor.get_energy0(),
        impactor.get_energy0_megatons(),
    )

    # If the impactor is less than a kilogram,
    # the impactor burns up in the atmosphere
    if mass < 1:
        logging.warning(
            "Impactor is less than a kilogram. \
                Impactor will burn up in the atmosphere."
        )

    # Calculate the effects of atmospheric entry
    (
        velocity,
        iFactor,
        altitudeBU,
        altitudeBurst,
        dispersion,
    ) = atmospheric_entry(impactor, target)

    # Compute linear and angular momentum as a fraction of Earth's
    linmom, angmom, energy0 = fraction_of_momentum(
        impactor, target, velocity
    )

    trot_change = cal_trot_change(impactor, target, velocity)

    # Compute energy of airburst, or energy after deceleration by atmosphere
    energy_atmosphere = cal_energy_atmosphere(impactor, target, velocity)
    energy_blast, energy_surface = cal_energy_blast_surface(
        impactor, target, velocity, altitudeBurst, energy_atmosphere
    )
    energy_megatons = energy_surface / (
        4.186 * 10 ** 15
    )  # joules to megatons conversion

    # Account for the decelerating effect of the water layer
    mwater = cal_mass_of_water(impactor, target, velocity)
    vseafloor = cal_velocity_projectile(impactor, target, velocity)
    energy_seafloor = cal_energy_at_seafloor(impactor, target, vseafloor)

    # Compute the epicentral angle for
    # use in several subsequent calculations.
    delta = cal_energy_at_seafloor(target)

    return (
        velocity,
        altitudeBU,
        altitudeBurst,
        dispersion,
        linmom,
        angmom,
        energy0,
        trot_change,
        energy_atmosphere,
        energy_blast,
        energy_surface,
        energy_megatons,
        mwater,
        vseafloor,
        energy_seafloor,
        delta,
    )


def air_blast(
    impactor: Impactor,
    target: Target,
    energy_blast: float = None,
    altitudeBurst: float = None,
):
    Po = target.get_Po()
    vsound = 330  # speed of sound in m/s
    # radius at which relationship
    # between overpressure and distance changes
    r_cross = 0
    # radius at which relationship between
    # overpressure and distance changes (for surface burst)
    r_cross0 = 290
    op_cross = 75000  # overpressure at crossover
    energy_ktons = 0  # energy in kilotons
    d_scale = 0  # distance scaled for 1 kTon blast
    slantRange = 0  # in km
    d_smooth = 0
    p_machT = 0
    p_regT = 0

    # energy_ktons = 1000 * energy_megatons
    energy_ktons = energy_blast

    # Arrival time is straight line distance divided by sound speed
    # for air burst, distance is slant range from explosion
    slantRange = (
        target.get_distance() ** 2 + (altitudeBurst / 1000) ** 2
    ) ** (1 / 2)
    # distance in meters divided by velocity of sound in m/s
    shock_arrival = (slantRange * 1000) / vsound

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

    # sound intensity
    if opressure > 0:
        dec_level = 20 * (log(opressure) / log(10))
    else:
        dec_level = 0

    return shock_arrival, vmax, dec_level


def tsunami(
    impactor: Impactor, target: Target, wdiameter: float = None
) -> float:
    shallowness = 0  # Ratio of Impactor diameter to water depth
    MaxWaveAmplitude = 0  # Maximum rim wave amplitude
    MaxWaveRadius = (
        0  # Radius where max rim wave is formed (upper estimate)
    )
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
    TsunamiSpeed = 0  # Tsunami speed in m/s
    TsunamiWavelength = 0  # Tsunami wavelength in m

    # Define parameters
    shallowness = impactor.get_pdiameter() / target.get_depth()
    RimWaveExponent = 1.0
    MaxWaveRadius = 0.001 * wdiameter
    MinWaveRadius = 0.0005 * wdiameter

    # Tsunami arrival time assumes linear wave theory
    TsunamiWavelength = 2.0 * wdiameter
    TsunamiSpeed = sqrt(
        0.5
        * target.get_g()
        * TsunamiWavelength
        / PI
        * tanh(2.0 * PI * target.get_depth() / TsunamiWavelength)
    )
    TsunamiArrivalTime = target.get_distance() * 1000 / TsunamiSpeed

    # Rim wave upper and lower limit estimates
    MaxWaveAmplitude = min(0.07 * wdiameter, target.get_depth())
    WaveAmplitudeUpperLimit = (
        MaxWaveAmplitude
        * (MaxWaveRadius / target.get_distance()) ** RimWaveExponent
    )
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

    return (
        TsunamiArrivalTime,
        WaveAmplitudeUpperLimit,
        WaveAmplitudeLowerLimit,
    )
