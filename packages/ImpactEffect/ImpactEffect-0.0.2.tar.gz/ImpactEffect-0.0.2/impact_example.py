from tkinter.tix import InputOnly
import numpy as np
from sqlalchemy import false
from sympy import re
import impactEffects.instances.ImpactorClass
from impactEffects.functions import *
from impactEffects.functions.function import *
from impactEffects.instances import ImpactorClass, TargetClass
from impactEffects.utils.print import print_energy, print_recurrencetime


def get_input():
    input_fail = True 
    while True:
        pdiameter = float(input("please input diameter of impactor: "))
        pdensity = float(input("please input density of impactor: "))
        v_input = float(input("please input the velocity of impactor: "))
        theta = float(input("please input the theta of impactor: "))
        tdensity = float(input("please input the density of target: "))
        depth = float(input("please input the depth(meters): "))
        distance = float(input("please input the distance: "))
        
        try:
            impactor = impactEffects.instances.ImpactorClass.Impactor(
                diameter=pdiameter, density=pdensity, velocity= v_input, theta=theta
            )
            targets = TargetClass.Target(depth=depth, distance=distance, density=tdensity)
            break
        except:
            print("Input error, please retry or exit.")
            retry = input("Do you want to retry?(0:false, 1:true)")
            if retry == "0":
                exit(0)
            elif retry == "1":
                continue
            else:
                print("error: input is not 0/1 .")
                exit(1)

    return impactor, targets

def simulateImpactor(impartor: Impactor, targets: Target):
    
    _kinetic_energy = kinetic_energy(impactor)
    _kinetic_energy_megatons = kinetic_energy_megatons(impactor)
    print_energy(_kinetic_energy, _kinetic_energy_megatons)

    _rec_time = rec_time(impactor)
    print_recurrencetime(_rec_time)

    collins_iFactor, _av, _rStrength = iFactor(impactor, targets)
    print(collins_iFactor)
    
    if collins_iFactor >= 1:
        velocity_at_surface = burst_velocity_at_zero(impactor, targets)

    altitudeBU = altitude_of_breakup(impactor, targets)
    print(altitudeBU)

    res = velocity_at_breakup(impactor, targets)
    print(res)

    res = dispersion_length_scale(impactor, targets)
    print(res)

    res = airburst_altitude(impactor, targets)
    print(res)

    res = brust_velocity(impactor, targets)
    print(res)

    res = dispersion_of_impactor(impactor, targets)

    res = fraction_of_momentum(impactor, targets)
    print(res)

    res = cal_trot_change(impactor, targets)
    res = cal_energy_atmosphere(impactor, targets)
    res = cal_energy_blast_surface(impactor, targets)
    res = cal_mass_of_water(impactor, targets)

    res = cal_velocity_projectile(impactor, targets)
    print(res)

    res = cal_energy_at_seafloor(impactor, targets)
    print(res)

    res = cal_ePIcentral_angle(targets)
    print(res)

    res = cal_scaling_diameter_constant(target=targets)
    print(res)

    res = cal_anglefac(impactor)
    print(res)

    
    res = cal_wdiameter(impactor, targets)
    wdiameter = 873.96211031212
    print(res, wdiameter)

    res = cal_transient_crater_diameter(impactor, targets)
    print(res)

    res = cal_depthr(impactor, targets)
    print(res)

    res = cal_cdiamater(impactor, targets)
    print(res)

    res = cal_depthfr(impactor, targets)
    print(res)

    res = cal_vCrater_vRation(impactor, targets)
    print(res)

    res = cal_vMelt(impactor, targets)
    print(res)

    res = cal_mratio_and_mcratio(impactor, targets)
    print(res)

    res = cal_eject_arrival(impactor, targets)
    ejecta_arrival = 124.569530217127
    print(res, ejecta_arrival)

    res = cal_ejecta_thickness(impactor, targets)
    ejecta_thickness = 143311.274150426

    print(res, ejecta_thickness)

    (
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

    res = cal_magnitude(impactor, targets)
    magnitude = 11.9138097245741

    eff_mag = 10.3894097245741
    seismic_arrival = 15
    res = cal_magnitude2(impactor, targets)

    print(res)

    res = cal_shock_arrival(impactor, targets)
    print(res)

    res = cal_vmax(impactor, targets)
    res = cal_dec_level(impactor, targets)

    
    res = cal_TsunamiArrivalTime(impactor, targets)
    TsunamiArrivalTime = 1436.89232538551
    print(res, TsunamiArrivalTime)

    
    res = cal_WaveAmplitudeUpperLimit(impactor, targets)
    WaveAmplitudeUpperLimit = 0.712889118910467
    print(res, WaveAmplitudeUpperLimit)
    
    res = cal_WaveAmplitudeLowerLimit(impactor, targets)
    WaveAmplitudeLowerLimit = 0.00103553906729725

    print(res, WaveAmplitudeLowerLimit)


if __name__ == "__main__":
    # impactor, target = get_input()
    # print(impactor.get_density())
    impactor = impactEffects.instances.ImpactorClass.Impactor(
        diameter=111, density=111, velocity=111, theta=45
    )
    targets = TargetClass.Target(depth=0, distance=75, density=2500)
    simulateImpactor(impactor, targets)
    