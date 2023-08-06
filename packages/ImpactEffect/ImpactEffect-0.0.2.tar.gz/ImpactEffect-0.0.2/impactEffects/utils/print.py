from impactEffects.core.config import *


def print_energy(energy0, energy0_megatons):
    # Format energy in scientific notation and in different units
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

    print("")


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


if __name__ == "__main__":
    print_energy(4.8967338468637005e+17, 116.9788305509723)
