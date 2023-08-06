import numpy as np
from sympy import re
import impactEffects.instances.ImpactorClass
from impactEffects.functions import *
from impactEffects.functions.function import *
from impactEffects.instances import ImpactorClass, TargetClass
from ans_config import *

# TODO： add the test for more cases


def test_Kinetic_energy():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=0, distance=75, density=2500)

    res = kinetic_energy(impactor)
    print(res, energy0)
    assert np.allclose(res, energy0)


def test_kinetic_energy_megatons():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=0, distance=75, density=2500)

    res = kinetic_energy_megatons(impactor)
    print(res, energy0_megatons)
    assert np.allclose(res, energy0_megatons)


def test_rec_time():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=0, distance=75, density=2500)

    res = rec_time(impactor)
    print(res, rec_time_)
    assert np.allclose(res, rec_time_)


def test_iFactor():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=0, distance=75, density=2500)

    collins_iFactor, _av, _rStrength = iFactor(impactor, targets)
    print(collins_iFactor, i_Factor)
    assert np.allclose(collins_iFactor, i_Factor)


def test_altitude_of_breakup():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=0, distance=75, density=2500)

    res = altitude_of_breakup(impactor, targets)

    print(res, altitudeBurst)
    assert np.allclose(res, altitudeBU)


def test_velocity_at_breakup():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=0, distance=75, density=2500)

    res = velocity_at_breakup(impactor, targets)

    print(res, vBU)
    assert np.allclose(res, vBU)


def test_dispersion_length_scale():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=0, distance=75, density=2500)

    res = dispersion_length_scale(impactor, targets)

    print(res, lDisper)
    assert np.allclose(res, lDisper)


def test_airburst_altitude():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=0, distance=75, density=2500)

    res = airburst_altitude(impactor, targets)

    print(res, altitudeBurst)
    assert np.allclose(res, altitudeBurst)


def test_brust_velocity():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=0, distance=75, density=2500)

    res = brust_velocity(impactor, targets)
    print(res, velocity)

    assert np.allclose(res, velocity)


def test_dispersion_of_impactor():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=0, distance=75, density=2500)

    res = dispersion_of_impactor(impactor, targets)


def test_fraction_of_momentum():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=0, distance=75, density=2500)

    res = fraction_of_momentum(impactor, targets)

    print(res, lratio, pratio)
    assert np.allclose(res[0], lratio)
    assert np.allclose(res[1], pratio)


def test_cal_trot_change():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=0, distance=75, density=2500)

    res = cal_trot_change(impactor, targets)

    assert np.allclose(res, trot_change)


def test_cal_energy_atmosphere():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=0, distance=75, density=2500)

    res = cal_energy_atmosphere(impactor, targets)

    assert np.allclose(res, energy_atmosphere)


def test_cal_energy_blast_surface():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=0, distance=75, density=2500)

    res = cal_energy_blast_surface(impactor, targets)

    assert np.allclose(res[0], energy_blast)
    assert np.allclose(res[1], energy_surface)


def test_cal_mass_of_water():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=0, distance=75, density=2500)

    res = cal_mass_of_water(impactor, targets)

    assert np.allclose(res, mwater)


def test_cal_velocity_projectile():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=0, distance=75, density=2500)

    res = cal_velocity_projectile(impactor, targets)
    print(res, vseafloor)

    assert np.allclose(res, vseafloor)


def test_cal_energy_at_seafloor():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=0, distance=75, density=2500)

    res = cal_energy_at_seafloor(impactor, targets)
    print(res, energy_seafloor)

    assert np.allclose(res, energy_seafloor)


def test_cal_ePIcentral_angle():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=0, distance=75, density=2500)

    res = cal_ePIcentral_angle(targets)
    print(res, delta)

    assert np.allclose(res, delta)


def test_cal_scaling_diameter_constant():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=0, distance=75, density=2500)

    res = cal_scaling_diameter_constant(targets)
    print(res, Cd, beta)

    assert np.allclose(res[0], Cd)
    assert np.allclose(res[1], beta)


def test_cal_anglefac():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=0, distance=75, density=2500)

    res = cal_anglefac(impactor)
    print(res, anglefac)

    assert np.allclose(res, anglefac)


def test_cal_wdiameter():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=1111, distance=75, density=1000)

    res = cal_wdiameter(impactor, targets)
    wdiameter = 873.96211031212
    print(res, wdiameter)

    assert np.allclose(res, wdiameter)


def test_cal_transient_crater_diameter():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=0, distance=75, density=2500)

    res = cal_transient_crater_diameter(impactor, targets)
    print(res, Dtr)

    assert np.allclose(res, Dtr)


def test_cal_depthr():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=0, distance=75, density=2500)

    res = cal_depthr(impactor, targets)
    print(res, depthtr)

    assert np.allclose(res, depthtr)


def test_cal_cdiamater():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=0, distance=75, density=2500)

    res = cal_cdiamater(impactor, targets)
    print(res, cdiameter)

    assert np.allclose(res, cdiameter)


def test_cal_depthfr():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=0, distance=75, density=2500)

    res = cal_depthfr(impactor, targets)
    print(res, depthfr)

    assert np.allclose(res, depthfr)


def test_cal_vCrater_vRation():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=0, distance=75, density=2500)

    res = cal_vCrater_vRation(impactor, targets)
    print(res, vCrater, vratio)

    assert np.allclose(res[0], vCrater)
    assert np.allclose(res[1], vratio)


def test_cal_vMelt():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=0, distance=75, density=2500)

    res = cal_vMelt(impactor, targets)
    print(res, vMelt)

    assert np.allclose(res, vMelt)


def test_cal_mratio_and_mcratio():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=0, distance=75, density=2500)

    res = cal_mratio_and_mcratio(impactor, targets)
    print(res, mratio, mcratio)

    assert np.allclose(res[0], mratio)
    assert np.allclose(res[1], mcratio)


def test_cal_eject_arrival():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111000, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=1111, distance=75, density=1000)

    res = cal_eject_arrival(impactor, targets)
    ejecta_arrival = 124.569530217127
    print(res, ejecta_arrival)

    assert np.allclose(res, ejecta_arrival)


def test_cal_ejecta_thickness():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111000, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=1111, distance=75, density=1000)

    res = cal_ejecta_thickness(impactor, targets)
    ejecta_thickness = 143311.274150426

    print(res, ejecta_thickness)
    assert np.allclose(res, ejecta_thickness)


def test_cal_themal():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111000, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=1111, distance=75, density=1000)

    (
        h,
        Rf,
        thermal_exposure_,
        no_radiation_,
        max_rad_time_,
        irradiation_time_,
        megaton_factor_,
        thermal_power_,
    ) = cal_themal(impactor, targets)
    (
        thermal_exposure,
        no_radiation,
        max_rad_time,
        irradiation_time,
        megaton_factor,
        thermal_power,
    ) = (
        4.14356223682368,
        0,
        14.208291667122,
        20466.8083549098,
        69.9012618159051,
        13,
    )

    assert np.allclose(thermal_exposure, thermal_exposure_)
    assert np.allclose(no_radiation, no_radiation_)
    assert np.allclose(max_rad_time, max_rad_time_)
    assert np.allclose(irradiation_time, irradiation_time_)
    assert np.allclose(megaton_factor, megaton_factor_)
    assert np.allclose(thermal_power, thermal_power_)


def test_cal_magnitude():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111000, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=1111, distance=75, density=1000)

    res = cal_magnitude(impactor, targets)
    magnitude = 11.9138097245741

    assert np.allclose(res, magnitude)


def test_cal_magnitude2():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111000, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=1111, distance=75, density=1000)

    eff_mag = 10.3894097245741
    seismic_arrival = 15
    res = cal_magnitude2(impactor, targets)

    print(res)

    assert np.allclose(res[0], eff_mag)
    assert np.allclose(res[1], seismic_arrival)


def test_cal_shock_arrival():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=0, distance=75, density=2500)

    res = cal_shock_arrival(impactor, targets)
    print(res, shock_arrival)

    assert np.allclose(res, shock_arrival)


def test_cal_vmax():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=0, distance=75, density=2500)

    res = cal_vmax(impactor, targets)
    assert np.allclose(res[0], vmax)


def test_cal_dec_level():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=0, distance=75, density=2500)

    res = cal_dec_level(impactor, targets)

    assert np.allclose(res, dec_level)


def test_cal_TsunamiArrivalTime():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=1111, distance=75, density=1000)

    res = cal_TsunamiArrivalTime(impactor, targets)
    TsunamiArrivalTime = 1436.89232538551

    print(res, TsunamiArrivalTime)
    assert np.allclose(res, TsunamiArrivalTime)


def test_cal_WaveAmplitudeUpperLimit():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=1111, distance=75, density=1000)

    res = cal_WaveAmplitudeUpperLimit(impactor, targets)
    WaveAmplitudeUpperLimit = 0.712889118910467

    print(res, WaveAmplitudeUpperLimit)
    assert np.allclose(res, WaveAmplitudeUpperLimit)


def test_cal_WaveAmplitudeLowerLimit():
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=1111, distance=75, density=1000)

    res = cal_WaveAmplitudeLowerLimit(impactor, targets)
    WaveAmplitudeLowerLimit = 0.00103553906729725

    print(res, WaveAmplitudeLowerLimit)
    assert np.allclose(res, WaveAmplitudeLowerLimit)
