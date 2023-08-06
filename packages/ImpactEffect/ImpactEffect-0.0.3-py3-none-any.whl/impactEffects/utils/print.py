from impactEffects.core.config import *


def print_energy(energy0, energy0_megatons):
    energy_power = log(energy0)/log(10)
    energy_power = int(energy_power)
    energy0 /= 10**energy_power

    megaton_power = log(energy0_megatons)/log(10)
    megaton_power = int(megaton_power)
    energy0_megatons /= 10**megaton_power

    # Print the energy
    if energy_power == 0:
        print("Energy before atmospheric entry: %.2f Joules " %
              (energy0),  end='')
    else:
        print("Energy before atmospheric entry: %.2f x 10^%.0f Joules " %
              (energy0, energy_power),  end='')

    if megaton_power == 0:
        if energy0_megatons < 1:
            print(" = %.2f KiloTons TNT" % (energy0_megatons * 1000),  end='')
        else:
            print(" = %.2f MegaTons TNT" % (energy0_megatons),  end='')
    else:
        print(" = %.2f x 10^%.0f MegaTons TNT" %
              (energy0_megatons, megaton_power),  end='')

    print("\n")


def print_recurrencetime(rec_time):
    # Use scientific notation for recurrence times longer than 1000 years
    if rec_time > 1000:
        rec_time_p = log(rec_time)/log(10)
        rec_time_p = int(rec_time_p)
        rec_time /= 10**rec_time_p

        if rec_time * 10**rec_time_p < 4.5e9:
            print("The average interval between impacts of this size somewhere on Earth during the last 4 billion years is %.1f x 10^%.0fyears." % (
                rec_time, rec_time_p))
        else:
            print(
                "The average interval between impacts of this size is longer than the Earth's age.")
            print("Such impacts could only occur during the accumulation of the Earth, between 4.5 and 4 billion years ago.")

        return

    # Use normal notation for intervals less than 1000 years
    if rec_time * 12 < 1:
        print("The average interval between impacts of this size somewhere on Earth is less than 1 month.")
    else:
        print("The average interval between impacts of this size somewhere on Earth is %.1f years." % (rec_time))
    print("")


def print_change(vratio, mratio, lratio, trot_change, pratio):
    print("Major Global Changes:")

    if vratio >= 0.1:
        if vratio >= 0.5:
            print("The Earth is completely disrupted by the impact and its debris forms a new asteroid belt orbiting the sun between Venus and Mars.")
        else:
            print("The Earth is strongly disturbed by the impact, but loses little mass.")
    else:
        print(
            "The Earth is not strongly disturbed by the impact and loses negligible mass.")

    if mratio >= 0.01:
        print("%.2f percent of the Earth is melted" % (mratio * 100))

    if lratio >= 0.001:
        print("Depending on the direction and location the collision, ")
        if lratio < 0.01:
            print(
                "the impact may make a very small change in the tilt of Earth's axis (< half a degree).")
        elif lratio < 0.1:
            print(
                "the impact may make a noticeable change in the tilt of Earth's axis (< 5 degrees).")
        elif lratio < 1.0:
            print("the impact may make a significant change in the tilt of Earth's axis.")
        else:
            print(
                "the impact may totally change the Earth's rotation period and the tilt of its axis.")
    else:
        print("The impact does not make a noticeable change in the tilt of Earth's axis (< 5 hundreths of a degree).")

    # Print the change in length of the day if more than one second
    if trot_change > 1e-3:
        print("Depending on the direction and location of impact, the collision may cause a change in the length of the day of up to %f unit." % (trot_change))

    if pratio >= 0.001:
        if pratio < .01:
            print("The impact shifts the Earth's orbit noticeably.")
        elif pratio < 0.1:
            print("The imapct shifts the Earth's orbit substantially.")
        else:
            print("The impact shifts the Earth's orbit totally.")

    else:
        print("The impact does not shift the Earth's orbit noticeably.")

    print("")


def print_atmospheric_entry(mass, vInput, velocity, iFactor, altitudeBU, altitudeBurst, pdensity, dispersion, theta, energy_surface, energy_megatons):
    print("Atmospheric Entry:")

    en = 0.5 * mass * ((vInput * 1000)**2 - (velocity * 1000)**2)

    en_mton = en / (4.186 * 10**15)  # joules to megatons conversion

    en_power = log(en)/log(10)
    en_power = int(en_power)
    en /= 10**en_power

    ens_power = log(energy_surface)/log(10)
    ens_power = int(ens_power)
    energy_surface /= 10**ens_power

    enmton_power = log(en_mton)/log(10)
    enmton_power = int(enmton_power)
    en_mton /= 10**enmton_power

    megaton_power = log(energy_megatons)/log(10)
    megaton_power = int(megaton_power)
    energy_megatons /= 10**megaton_power

    if iFactor >= 1:
        print("The projectile lands intact, with a velocity %f km/s = %f miles/s." %
              (velocity, velocity * 0.621))
        print("The energy lost in the atmosphere is %.2f x 10^%.0f Joules = %.2f x 10^%.0f MegaTons." % (
            en, en_power, en_mton, enmton_power))
    else:
        print("The projectile begins to breakup at an altitude of %f meters = %f ft" %
              (altitudeBU, altitudeBU * 3.28))
        if altitudeBurst > 0:
            print("The projectile bursts into a cloud of fragments at an altitude of %f meters = %f ft" %
                  (altitudeBurst, altitudeBurst * 3.28))
            print("The residual velocity of the projectile fragments after the burst is %f km/s = %f miles/s" %
                  (velocity, velocity * 0.621))
            print("The energy of the airburst is %.2f x 10^%.0f Joules = %.2f x 10^%.0f MegaTons." %
                  (en, en_power, en_mton, enmton_power))
            if pdensity < 5000:
                print(
                    "No crater is formed, although large fragments may strike the surface.")
            else:
                print("Large fragments strike the surface and may create a crater strewn field.  A more careful treatment of atmospheric entry is required to accurately estimate the size-frequency distribution of meteoroid fragments and predict the number and size of craters formed.")

        else:
            print("The projectile reaches the ground in a broken condition.  The mass of projectile strikes the surface at velocity %f km/s = %f miles/s" %
                  (velocity, velocity * 0.621))
            print("The energy lost in the atmosphere is %.2f x 10^%.0f Joules = %.2f x 10^%.0f MegaTons." %
                  (en, en_power, en_mton, enmton_power))
            if megaton_power != 0:
                print("The impact energy is %.2f x 10^%.0f Joules = %.2f x 10^%.0fMegaTons." %
                      (energy_surface, ens_power, energy_megatons, megaton_power))
            else:
                print("The impact energy is %.2f x 10^%.0f Joules = %.2f MegaTons." %
                      (energy_surface, ens_power, energy_megatons))

            print(
                "The larger of these two energies is used to estimate the airblast damage.")
            print("The broken projectile fragments strike the ground in an ellipse of dimension %f km by %f km" %
                  (dispersion/(1000 * sin(theta * PI / 180)), dispersion / 1000))

    print("")


def print_ejecta(energy_megatons, megaton_power, distance, Rf, Dtr, cdiameter, ejecta_arrival, ejecta_thickness, d_frag):
    # ejecta results
    print("Ejecta:")

    # Ejecta from small impacts is blocked by the atmosphere
    if (energy_megatons * 10**megaton_power) < 200 and (distance > Rf):
        print("Most ejecta is blocked by Earth's atmosphere")
        return

    # Ejecta comes from transient crater
    if distance * 1000 <= Dtr/2:
        print("Your position was inside the transient crater and ejected upon impact")
        return

    # Inside final crater
    if distance * 1000 > Dtr/2 and distance * 1000 < cdiameter/2:
        print("Your position is in the region which collapses into the final crater.")
        return

    # Arrival time greater than 1 hour or almost no ejecta
    if ejecta_arrival >= 3600:
        print("Little rocky ejecta reaches this site fallout is dominated by condensed vapor from the projectile.")
        return
    elif ejecta_thickness * 10**6 < 1:
        print("Almost no solid ejecta reaches this site.")
        return

    # Type of ejecta deposit
    if distance * 1000 <= 3 * cdiameter/2:
        print("Your position is beneath the continuous ejecta deposit.")
    else:
        print("At your position there is a fine dusting of ejecta with occasional larger fragments")

    # Ejecta thickness
    print("Average Ejecta Thickness:  %f %s ( = %f %s ) \n" % (
          ejecta_thickness, "meters", ejecta_thickness * 3.28, "feet"))

    # Fragment size
    print("Mean Fragment Diameter:  %f %s ( = %f %s ) \n" % (
          d_frag, "meters", d_frag * 3.28, "feet"))
    print("")


def print_thermal(velocity, no_radiation, max_rad_time, distance, Rf, h, thermal_power, thermal_exposure, irradiation_time):
    print("Thermal Radiation:")

    print("What does this mean?")

    # No fireball at low velocity
    if velocity < 15:
        print("At this impact velocity ( < 15 km/s), little vaporization occurs no fireball is created, therefore, there is no thermal radiation damage.")
        return

    # Is fireball above the horizon?
    if no_radiation == 1:
        print(
            "The fireball is below the horizon. There is no direct thermal radiation.\n</dl>\n")
        return

    # Time of maximum radiation
    print("Time for maximum radiation:  %f %s  after impact" %
          (max_rad_time, "seconds"))

    # Size of the fireball
    if distance < Rf:
        print("Your position is inside the fireball.")
    else:
        print("Visible fireball radius:  %f %s ( = %f %s ) " %
              ((Rf-h)*1000, "meters", (Rf-h)*1000*3.28, "feet"))

    # Brightness of the fireball relative to the sun
    B = (Rf - h)/(4.4 * 10**-3 * distance)
    if B >= 0.1:
        print("The fireball appears %f times larger than the sun" % (B))

    # Thermal exposure
    if thermal_power == 0:
        print("Thermal Exposure:  %.2f Joules/m<sup2</sup>" % (
              thermal_exposure))
    else:
        print("Thermal Exposure:  %.2f x 10<sup>%.0f</sup> Joules/m<sup>2</sup>" %
              (thermal_exposure, thermal_power))

    # Duration of irradiation
    print("Duration of Irradiation:  %f %s" % (
          irradiation_time, "seconds"))

    # Radiant flux relative to solar flux
    flux = (thermal_exposure * 10**thermal_power) / (irradiation_time * 1000)
    print("Radiant flux (relative to the sun):  %f", flux)
    if flux >= 15 and flux <= 25:
        print(" (Flux from a burner on full at a distance of 10 cm)")
    print("")


def print_seismic(magnitude, seismic_arrival):
    # seismic results
    print("<dl>\n<dt>\n<h2>Seismic Effects:</h2>\n")
    print("What does this mean?")

    # Don' print results if magnitude very small
    if magnitude < 0:
        print("The Richter Scale Magnitude for this impact is less than zero no seismic shaking will be felt.")
        return

    # Arrival time
    if seismic_arrival < 0.1:
        print("The major seismic shaking will arrive almost instantly.")
    else:
        print("The major seismic shaking will arrive approximately %f %s after impact." %
              (seismic_arrival, "seconds"))

    # Richter Scale Magnitude
    print("Richter Scale Magnitude:  %.1f" % (magnitude))
    if magnitude >= 9.5:
        print(" (This is greater than any earthquake in recorded history)")

    # Earthquake damage
    # print("Mercalli Scale Intensity at a distance of distance km: \n<br>\n"
    # print des
    print("")


def print_airblast(opressure, vmax, shock_arrival, distance, altitudeBurst, dec_level, shock_damage):
    bars = opressure / 10**5
    mph = vmax * 2.23694

    print("Air Blast:")

    print("What does this mean?")

    # Exit if airblast has no effect
    if opressure < 1:
        print("The air blast at this location would not be noticed. (The overpressure is less than 1 Pa)")
        return

    # Blast wave arrival time
    print("The air blast will arrive approximately %f %s after impact." %
          (shock_arrival, "seconds"))

    # Overpressure
    if distance*1000. < 3*altitudeBurst:
        print("Peak Overpressure:  %f - %f Pa = %f - %f bars = %f - %f psi" %
              (opressure, 2*opressure, bars, 2*bars, bars * 14.2, 2*bars * 14.2))
    else:
        print("Peak Overpressure:  %f Pa = %f bars = %f psi" %
              (opressure, bars, bars * 14.2))

    # Wind velocity
    print("Max wind velocity:  %f m/s = %f mph" % (vmax, mph))

    # Sound intensity
    if dec_level > 0:
        print("Sound Intensity:  %.0f dB" % (dec_level), end="")
        if dec_level <= 20:
            print(" (Barely Audible)")
        elif dec_level <= 50:
            print(" (Easily Heard)")
        elif dec_level <= 90:
            print(" (Loud as heavy traffic)")
        elif dec_level <= 120:
            print(" (May cause ear pain)")
        else:
            print(" (Dangerously Loud)")

    else:
        print("The blast wave will not be heard.")

    # Airblast damage
    if shock_damage != "":
        print("Damage Description: ", end="")

    print(shock_damage)
    print("")


def print_tsunami(distance, wdiameter, TsunamiArrivalTime, WaveAmplitudeLowerLimit, WaveAmplitudeUpperLimit):
    FormattedTime = 0.
    TimeUnit = "non"

    # Print the tsunami results
    print("Tsunami Wave:")

    print("What does this mean?")

    # If inside the water crater say this and finish.
    if distance*1000 < wdiameter:
        print("Your location is within the crater formed in the water layer. This is where the impact tsunami wave is generated. \n")
        return

    # Report the approximate arrival time of the tsunami
    print("The impact-generated tsunami wave arrives approximately %.1f %s after impact. " % (
          TsunamiArrivalTime, "seconds"))

    # Report the two wave amplitude limits if more than 10 cm
    if WaveAmplitudeLowerLimit > 0.1:
        print("Tsunami wave amplitude is between:  %.1f %s ( = %.1f %s) and %.1f %s ( = %.1f %s). " % (
              WaveAmplitudeLowerLimit, "meters", WaveAmplitudeLowerLimit*3.28, "feets", WaveAmplitudeUpperLimit, "meters", WaveAmplitudeUpperLimit*3.28, "feets"))
    elif WaveAmplitudeUpperLimit < 0.1:
        print(
            "Tsunami wave amplitude is less than 10 cm at your location. ")
    else:
        print("Tsunami wave amplitude is less than %.1f %s ( = %.1f %s). " % (
              WaveAmplitudeUpperLimit, "meters",  WaveAmplitudeUpperLimit*3.28, "feets"))

    print("")


if __name__ == "__main__":
    print_energy(4.8967338468637005e+17, 116.9788305509723)
