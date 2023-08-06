#! /usr/bin/perl -w

use strict;

use lib "/var/www/html/ImpactEarth/cgi-bin";
use CGI qw(:standard);
use List::Util qw[min max];
use Scalar::Util qw(looks_like_number);
use Math::Trig;
use Math::SigFigs;

# copyright 2010, Gareth Collins, H.J. Melosh, and Robert Marcus. 

#my $output;

# Flags for whether the hazard is present (0 not present; 1 present)
my $qCrater   = 0;
my $qAirblast = 0;
my $qThermal  = 0;
my $qSeismic  = 0;
my $qEjecta   = 0;
my $qTsunami  = 0;

my $sigfigs = 3;			# number of sig figs to print
my $pdiameter;                          # Impactor diameter (m)
my $pdensity;                           # Impactor density (kg/m^3)
my $vInput;				# input velocity (km/s) before entry
my $velocity;				# velocity at target surface km/s
my $theta;
my $tdensity;
my $ttype;
my $latitude;                           # Latitude in degrees (decimal notation)
my $longitude;                          # Latitude in degrees (decimal notation)
my $ViewAltitude;
#my $effect;
my $CraterRadiusFinal;
my $CraterRadiusTransient;
my $RadiusFireball;
my $RadiusVisibleFireball;
my $RadiusClothingIgnition;
my $Radius100mEjecta = 0;
my $Radius10mEjecta  = 0;
my $Radius1mEjecta   = 0;
my $Radius10cmEjecta = 0;
my $Radius1cmEjecta  = 0;
my $RadiusMercalliIII = 0;
my $RadiusMercalliV   = 0;
my $RadiusMercalliVII = 0;
my $RadiusMercalliIX  = 0;
my $RadiusMercalliXII = 0;
my $RadiusAirblast126 = 0;
my $RadiusAirblast155 = 0;
my $RadiusAirblast500 = 0;
my $RadiusAirblast1160 = 0;
my $RadiusAirblast3300 = 0;
my $Radius1mTsunami   = 0;
my $Radius10mTsunami  = 0;
my $Radius100mTsunami = 0;
my $Radius1kmTsunami  = 0;
my $distance;				# distance in km
my $depth;				# water depth in meters
my $mwater;				# mass of water
my $vseafloor;				# velocity of projectile at seafloor
my $energy0;				# input energy before atmospheric entry
my $energy_power;
my $energy0_megatons;
my $megaton_power;
my $energy_atmosphere;                  # energy deposited in atmosphere
my $energy_surface;			# energy at surface (bottom of atmosphere)
my $energy_blast;			# energy used in airblast calc. (ktons)
my $energy_megatons;			# energy at suface in MT
my $energy_seafloor;			# energy at seafloor (bottom of water layer)
my $rec_time;                           # Reccurence interval (years)
my $iFactor;				# intact factor >= 1, projectile lands intact
my $altitudeBU;				# altitude of projectile breakup in meters
my $altitudeBurst;			# altitude at which projectile bursts in meters
my $dispersion;				# dispersion of pancake upon impact, 2 * semimajor axis of pancaked impactor
my $mass;               		# mass of projectile
my $magnitude;          		# richter scale magnitude
my $seismic_arrival;			# time of arrival for seismic effects
my $eff_mag;            		# effective magnitude
my @input; 				# stores input from mercalli.txt
my $des;				# description of intensity
my $wdiameter;				# diameter of crater in water
my $WaveAmplitudeUpperLimit;            # Amplitude of tsunami wave at specified distance (upper estimate; m)
my $WaveAmplitudeLowerLimit;            # Amplitude of tsunami wave at specified distance (lower estimate; m)
my $TsunamiArrivalTime;                 # Arrival time of tsunami wave at specified distance (s)
my $cdiameter;          		# final crater diameter
my $Dtr;                		# transient crater diameter in m at the original ground surface
my $depthtr;				# depth of transient crater in m (below the original ground surface)
my $brecciaThickness;			# in m
my $depthfr;				# final crater depth in m (from rim to floor)
my $vCrater;				# volume of crater in km^3
my $vMelt;				# volume of melt in km^3
my $ejecta_thickness;			# thickness of ejecta
my $ejecta_arrival;			# time of arrival for ejecta
my $d_frag;				# mean ejecta fragment size
my $shock_arrival;			# arrival time for shock wave
my $sf;					# scale factor for shock wave calculations
my $opressure;				# overpressure
my $vmax;				# max velocity of shock wave
my $shock_damage = "";			# text description of shock damage
my $dec_level;				# intensity of sound in decibels
my $Rf;					# radius of fireball
my $h;					# part of the fireball below the horizon
my $no_radiation;			# set to true if the fireball is below horizon
my $thermal_exposure;			# thermal exposure in Joules/m^2
my $thermal_power;			# order of magnitude of thermal exposrure
my $max_rad_time;			# time for max thermal radiation in sec
my $irradiation_time;			# time of irradiation
my $thermal_des;			# description of thermal effects
my $Po = 10**5;				# ambient pressure in Pa
my $g = 9.8;            		# acceleration due to gravity
my $R_earth = 6370;     		# radius of the earth in km
my $surface_wave_v = 5; 		# velocity of surface wave in km/s
my $melt_coeff = 8.9 * 10**-21;		# coefficient for melt volume calc
my $vEarth = 1.1 * 10**12;		# volume of earth in km^3
my $vratio;				# ratio of volume of crater to volume of earth
my $mratio;				# ratio of melt to volume of earth
my $mcratio;				# ratio of melt to volume of crater
my $lEarth = 5.86 * 10**33;		# angular momen. of earth in (kg m^3)/sec
my $lratio;				# ratio of proj ang. momen, to $lEarth
my $mEarth = 5.97 * 10**24;             # Mass of Earth in kg
my $pEarth = 1.794 * 10**32;		# lin. momen of earth in (kg * m) / sec
my $pratio;				# ratio of proj lin. momen to $pEarth
my $trot_change;                        # Change in Earth's rotation period (secs)
my $pi = 3.14159;
my $rhoSurface = 1;			# suface density of atmosphere kg/m^3
my $scaleHeight = 8000;			# scale height of atmosphere in m
my $dragC = 2;				# drag coefficient
my $fp = 7;				# pancake factor
my $valid_data = 1;
my @valid = qw(1 1 1 1 1 1 1 1 1 1);

&get_data();
&check_data();
if($valid_data == 0){
  &reprint_form();
}else{
  &impact();
}


sub get_data
  {
    my $location  = 0;
    my $latlon    = 1;                  # Boolean: have lat and long been specified? (default: yes)
      
    ### Get the location of the impact
    $latitude = param("latitude");
    $longitude = param("longitude");
    if ($latitude eq '' or $longitude eq ''){
      $latlon = 0;
    }
    if ($latlon == 0) {
      $location = param("LocationSelect");
      
      if ($location == 1) {
	$latitude = 51.5;         ### London
	$longitude = -0.125;
      }	elsif ($location == 2) {
	$latitude = 34.052;       ### LA
	$longitude = -118.244;
      }	elsif ($location == 3) {
	$latitude = 40.767;       ### New York
	$longitude = -73.975;
      }	elsif ($location == 4) {
	$latitude = 52.525;       ### Berlin
	$longitude = 13.4114;
      }	elsif ($location == 5) {
	$latitude = 48.86;        ### Paris
	$longitude = 2.35;
      }	elsif ($location == 6) {
	$latitude = -26.201;      ### Johannesburg
	$longitude = 28.045;
      }	elsif ($location == 7) {
	$latitude = -33.864;      ### Sydney
	$longitude = 151.193;
      }	elsif ($location == 8) {
	$latitude = 51.4782;      ### Cardiff
	$longitude = -3.1826;
      }	elsif ($location == 9) {
	$latitude = 55.9486;      ### Edinburgh
	$longitude = -3.1998;
      }	
    }
    if ($location == 0 and $latlon == 0) {
      my $EarthCrater = param("CraterSelect");
      if ($EarthCrater == 1) {
	$latitude = -32.0173;     ### Aracman
	$longitude = 135.45;
      }	elsif ($EarthCrater == 2) {
	$latitude = -16.783;      ### Araguainha
	$longitude = -52.983;
      }	elsif ($EarthCrater == 3) {
	$latitude = 35.0272;      ### Barringer
	$longitude = -111.0228;
      }	elsif ($EarthCrater == 4) {
	$latitude = 21.3;         ### Chicxulub
	$longitude = -89.5;
      }	elsif ($EarthCrater == 5) {
	$latitude = 37.283;       ### Chesapeake Bay
	$longitude = -76.017;
      }	elsif ($EarthCrater == 6) {
	$latitude = -57.787;      ### Eltanin
	$longitude = -90.793;
      }	elsif ($EarthCrater == 7) {
	$latitude = 71.65;        ### Popigai
	$longitude = 111.1833;
      }	elsif ($EarthCrater == 8) {
	$latitude = 48.883;       ### Ries
	$longitude = 10.617;
      }	elsif ($EarthCrater == 9) {
	$latitude = 61.0333;      ### Siljan
	$longitude = 14.87;
      }	elsif ($EarthCrater == 10) {
	$latitude = 46.6;         ### Sudbury
	$longitude = -81.18;
      }	elsif ($EarthCrater == 11) {
	$latitude = -27.;         ### Vredefort
	$longitude = 27.5;
      }	elsif ($EarthCrater == 12) {
	$latitude = 54.233;         ### Silverpit
	$longitude = 1.85;
      }	
    }
      


    # Impactor diameter
    my $punits;	
    $pdiameter = param("diam");
    $punits = param('diameterUnits');
    if ($pdiameter eq '') {
      $pdiameter = param('pdiameter_select');
      $punits = 1  
    }
    if ($punits == 2) {
      $pdiameter *= 1000;
    } elsif ($punits == 3) {
      $pdiameter *= 0.3048;
    } elsif ($punits == 4) {
      $pdiameter *= 1609.34;
    }

    # Impactor density
    $pdensity = param('pdens');
    if ($pdensity eq '') {
      $pdensity = param('pdens_select');  
    }

    # Distance from impact (not relevant for this version)
    #$distance = param('dist');
    #my $dunits;
    #$dunits = param('distanceUnits');
    #if ($dunits == 2) {
    #  $distance *= 1.61;
    #}

    # Velocity
    my $vUnits;
    $vInput = param('vel');  	
    $vUnits = param('velocityUnits');
    if ($vInput eq '') {
      $vInput = param('velocity_select');
      $vUnits = 1
    }
    if ($vUnits == 2) {
      $vInput *= 1.61;
    }

    # Angle
    $theta = param('theta');
    if ($theta eq '') {
      $theta = param('angle_select');
    }

    # Target density and water depth
    $tdensity = param('tdens');
    if ($tdensity == 1000) {
      $depth = param('wdepth');
    } else {
      $depth = 0;
    }
    	
    my $depthUnits;
    $depthUnits = param('wdepthUnits');
    if ($depthUnits == 2) {
      $depth *= 0.3048;
    }
  
    $ttype = 3;
	    	
    $distance = param('dist');

    my $dunits;
    $dunits = param('distanceUnits');
    if ($dunits == 2) {
      $distance *= 1.61;
    }

    #my $punits;	
    #$punits = param('diameterUnits');
    #if ($punits == 2) {
    #  $pdiameter *= 1000;
    #} elsif ($punits == 3) {
    #  $pdiameter *= 0.3048;
    #} elsif ($punits == 4) {
    #  $pdiameter *= 1609.34;
    #}

    my $vunits;
    $vunits = param('velocityUnits');
    if ($vunits == 2) {
      $velocity *= 1.61;
    }
    
    #$effect = param("effect");

  }


sub check_data
{
	
	if(!($energy0 =~ /^[0-9]+\.?[0-9]*e?[0-9]*$/)){
		$valid[7] = 0;
	}
	if($pdiameter == 0.0 or !($pdiameter =~ /^[0-9]*\.?[0-9]*$/)){
		$valid_data = 0;
		$valid[0] = 0;
	}
	if($pdensity == 0 or !($pdensity =~ /^[0-9]?\.?[0-9]*$/)){
		$valid_data = 0;
		$valid[1] = 0;
	}
	if($vInput == 0 or $vInput >= 3 * 10**5 or !($vInput =~ /^[0-9]*\.?[0-9]*$/)){
		$valid_data = 0;
		$valid[2] = 0;
	}
	if($theta > 90 or $theta == 0 or !($theta =~ /^[0-9]+\.?[0-9]*$/)){
		$valid_data = 0;
		$valid[3] = 0;
	} 
	if($tdensity == 0 or !($tdensity =~ /^[0-9]?\.?[0-9]*$/)){
		$valid_data = 0;
		$valid[4] = 0;
	}
	if($ttype == ''){
		$valid_data = 0;
		$valid[5] = 0;
	}
	if(!($depth =~ /^[0-9]?\.?[0-9]*$/)){
		$valid_data = 0;
		$valid[9] = 0;
	}
	if($latitude > 90 or $latitude < -90 or !($latitude =~ /^[+-]?[0-9]+\.?[0-9]*$/)) {
		$valid_data = 0;
		$valid[6] = 0;
	}
	if($longitude > 180 or $longitude < -180 or !($longitude =~ /^[+-]?[0-9]+\.?[0-9]*$/)) {
		$valid_data = 0;
		$valid[8] = 0;
	}
	


}


### The main sub program
### pre:  All necessary parameters are valid, results calculated
sub impact
  {

    ### Print the title and header; echo the user's inputs
    print header();

    print_begin();

    ### Compute impact energy and atmospheric entry
    calc_energy();

    ### Calculate the crater dimensions
    find_crater();

    ### For crater-forming impacts calculate consequences
    if ($altitudeBurst <= 0) {
      $qCrater=1;
      find_ejecta();
      find_seismic();
      find_airblast();
      ### Calculate tsunami height
      if ($depth > 0) {
	$qTsunami = 1;
	find_tsunami();
      }
    } else { 
      $qCrater=0;
      find_airblast(); 
    }

    ### Calculate the thermal radiation damage
    if ($velocity >= 15) {
      $qThermal = 1;
      find_thermal();
    }

    ### If the impactor does not airburst, compute:
    ### Ejecta, thermal radiation, earthquake
#    if ($altitudeBurst <= 0) {
      #&find_crater();

      ### Calculate the ejecta thickness, particle size and arrival time
#      &find_ejecta();

      ### For high-velocity impacts, calculate the fireball size, thermal radiation
#      if ($velocity >= 15) {
#	&find_thermal();
#      }

      ### Calculate the earthquake magnitude and damage
#      &find_magnitude();
#      &find_intensity();

      ### Print results (only print ejecta if inside the crater)
#      print_crater();
#      if ($distance * 1000 <= $Dtr/2) {
#	print_ejecta();
#	return;
#      }		
#      print_thermal();
#      print_seismic();
#      print_ejecta();
#    }	

    print_title();
    print <<EOF;
    <div id="cesiumContainer" class="halfSize">
    <div id="toolbar"></div>
    </div>
EOF

    #<div id="loadingOverlay"><h1>Loading...</h1></div>

    print_CesiumWidget();

    echo_inputs();

    ### Print the impact energy, recurrence interval and global effects
    print_energy();
    print_recurrencetime();
    print_change();
    if ($mass <= 1.5707963E12) { print_atmospheric_entry(); }

    if ($qCrater == 1) { print_crater(); }

    ### Include a link to the documentation
    print_pdf();

  }  ### End of main program impact_effects

### Subroutine for computing impact energy (before and after atmospheric entry, and after ocean traverse).
### Atmospheric entry calculation is called from in here
### Also compute reccurence time interval (years)
sub calc_energy {

    ### mass = density * volume, volume calculated assuming the projectile to be approximately spherical
    ### V = 4/3pi(r^3) = 1/6pi(d^3)
    $mass = (($pi * ($pdiameter)**3.)/6.)*$pdensity;
    $energy0 = 0.5 * $mass * ($vInput * 1000)**2;
    $energy0_megatons = $energy0 / (4.186 * 10**15); ### joules to megatons conversion

    ### Compute the recurrence interval for this energy impact
    ### Old model
    #$rec_time = 110 * ($energy0_megatons)**0.77;
    ### New model (after Bland and Artemieva (2006) MAPS 41 (607-621).
    if ($mass < 3.) {
      $rec_time = 10**(-4.568)*$mass**0.480;
    } elsif ($mass < 1.7E10 ) {
      $rec_time = 10**(-4.739)*$mass**0.926;
    } elsif ($mass < 3.3E12 ) {
      $rec_time = 10**(0.922)*$mass**0.373;
    } elsif ($mass < 8.4E14 ) {
      $rec_time = 10**(-0.086)*$mass**0.454;
    } else {
      $rec_time = 10**(-3.352)*$mass**0.672;
    }

    ### Use our previous estimate at large sizes.
    $rec_time = max($rec_time,110*($energy0_megatons)**0.77);

    
    ### If the impactor is less than a kilogram, the impactor burns up in the atmosphere
    if ($mass < 1.) {
      print_noimpact();
    }
	
    ### Calculate the effects of atmospheric entry
    atmospheric_entry();

    ### Compute linear and angular momentum as a fraction of Earth's
    my $linmom;
    my $angmom;
    $linmom = $mass * ($velocity * 1000);
    $angmom = $mass * ($velocity * 1000) * cos($theta * $pi / 180) * $R_earth;

    if ($vInput > (0.25 * 3 * 10**5)) {	# relativistic effects, multiply energy by 1/sqrt(1 - v^2/c^2)
      my $beta = 1/ (1 - $vInput**2 / 9 * 10**10)**0.5;
      $energy0 *= $beta;	
      $linmom *= $beta;
      $angmom *= $beta;
    }

    $lratio = $angmom / $lEarth;
    $pratio = $linmom / $pEarth;

    $trot_change = (1.25/$pi)*($mass/$mEarth)*cos($theta * $pi / 180) / $R_earth * $velocity * (24.*60.*60.)**2;
	
    ### Compute energy of airburst, or energy after deceleration by atmosphere
    $energy_atmosphere = 0.5 * $mass * (($vInput * 1000)**2 - ($velocity * 1000)**2);
    if ($altitudeBurst > 0) {
      # Blast energy is airburst energy (kTons)
      $energy_blast = $energy_atmosphere / (4.186 * 10**12);
      $energy_surface = $energy_atmosphere;
    } else {
      $altitudeBurst = 0;
      $energy_surface = 0.5 * $mass * ($velocity * 1000)**2;
      # Blast energy is larger of airburt and impact energy (kTons)
      if ($energy_atmosphere > $energy_surface) {
        $energy_blast = $energy_atmosphere / (4.186 * 10**12);
      } else {
        $energy_blast = $energy_surface / (4.186 * 10**12);
      }
    }
    $energy_megatons = $energy_surface / (4.186 * 10**15); ### joules to megatons conversion

    ### Account for the decelerating effect of the water layer
    $mwater = ($pi * $pdiameter**2 / 4) * ($depth / sin($theta * $pi / 180)) * 1000;	
    $vseafloor = $velocity * exp(-(3 * 1000 * 0.877 * $depth) / (2 * $pdensity * $pdiameter * sin($theta * $pi / 180)));
    $energy_seafloor = 0.5 * $mass * ($vseafloor * 1000)**2;
	
}				### End of sub calc_energy

### Subroutine for computing effects of atmospheric entry:
### -- Break-up altitude (if break-up occurs)
### -- Burst altitude (if airbust)
### -- impactor velocity at break-up and airburst/impact
### -- dispersion of fragments if break-up occurs
sub atmospheric_entry
  {

    my $yield;			# yield strength of projectile in Pa 
    my $av;			# velocity decrement factor
    my $rStrength;		# strength ratio
    my $vTerminal;		# m/s
    my $vSurface;		# velocity of the impactor at surface in m/s if greater than terminal velocity
    my $altitude1;
    my $omega;
    my $vBU;

    ## Approximate the strength of the impactor using the density function in
    ## Eq. 9 of Collins et al. (2005)
    $yield = 10**(2.107 + 0.0624 * $pdensity**(1/2));

    ## Define a relative strength of the impactor compared to the
    ## maximum possible stagnation pressure on entry
    $rStrength = $yield / ($rhoSurface * ($vInput * 1000) **2);

    ## Define the exponent of Eq. 8 for the case of impact at the surface
    $av = 3 * $rhoSurface * $dragC * $scaleHeight / (4 * $pdensity * $pdiameter * sin($theta * $pi / 180)); # Assuming drag coefficient of 2

    ## Define the factor (Eq. 12), used in the break-up altitude calculation (Eq. 11)
    $iFactor = 2.7185 * $av * $rStrength; # Assuming drag coefficient of 2

    if ($iFactor >= 1) {	# projectile lands intact

      ## Burst altitude is zero
      $altitudeBurst = 0;

      ## Define the terminal velocity
      $vTerminal = min($vInput,(4 * $pdensity * $pdiameter * $g / (3 * $rhoSurface * $dragC) )**(1/2)); # Assuming drag coefficient of 2

      ## Define the surface velocity assuming continual spreading using Eq. 8
      $vSurface = $vInput * 1000 * exp(-$av);
		
      ## Take the maximum of the extrapolated surface velocity and the terminal velocity
      if ($vTerminal > $vSurface) {
	$velocity = $vTerminal;
      } else {
	$velocity = $vSurface;
      }

    } else {			# projectile does not land intact

      ## Compute the first term in Eq. 11
      $altitude1 = - $scaleHeight * log($rStrength);

      ## Define the second, third and fourth terms (inside the brackets) in Eq. 11
      $omega = 1.308 - 0.314 * $iFactor - 1.303 * (1 - $iFactor)**(1/2);

      ## Compute the breakup altitude by combining above parameters to evaluate Eq. 11
      $altitudeBU = $altitude1 - $omega * $scaleHeight;

      ## Define velocity at breakup altitude using Eq. 8 (and Eq. 5)
      $vBU = $vInput * 1000 * exp(- $av * exp(- $altitudeBU/$scaleHeight)); # m/s

      ## Define factor for evaluating Eq. 17
      my $vFac = 0.75 * ($dragC * $rhoSurface / $pdensity )**(1/2) * exp(- $altitudeBU / (2 * $scaleHeight)); # Assuming drag coefficient of 2

      ## Define dispersion length-scale (Eq. 16)
      my $lDisper = $pdiameter * sin($theta * $pi / 180) * ($pdensity / ($dragC * $rhoSurface) )**(1/2) * exp($altitudeBU / (2 * $scaleHeight)); # Assuming drag coefficient of 2

      ## Define the alpha parameters used to evaluate Eq. 18 and Eq. 19
      my $alpha2 = ($fp**2 - 1)**(1/2);

      ## Define the burst altitude using Eq. 18
      my $altitudePen = 2 * $scaleHeight * log(1 + $alpha2 * $lDisper /(2 * $scaleHeight));
      $altitudeBurst = $altitudeBU - $altitudePen;

      if ($altitudeBurst > 0) {	# impactor bursts in atmosphere

	## Evaluate Eq. 19 (without factor lL_0^2; $lDisper * $pdiameter**2)
	my $expfac = 1/24 * $alpha2 *(24 + 8 * $alpha2**2 + 6 * $alpha2 * $lDisper / $scaleHeight + 3 * $alpha2**3 * $lDisper / $scaleHeight);

	## Evaluate velocity at burst using Eq. 17 
	## (note that factor $lDisper * $pdiameter**2 in $expfac cancels with same factor in $vFac)
	$velocity = $vBU * exp(- $expfac * $vFac);

      } else {

	## Define (l/H) for use in Eq. 20
	my $altitudeScale = $scaleHeight / $lDisper;

	## Evaluate Eq. 20 (without factor lL_0^2; $lDisper * $pdiameter**2)
	## (note that this Eq. is not correct in the paper)
	my $integral = $altitudeScale**3 / 3 * (3 * (4 + 1/$altitudeScale**2) * exp($altitudeBU / $scaleHeight) + 6 * exp(2 * $altitudeBU / $scaleHeight) - 16 * exp(1.5 * $altitudeBU / $scaleHeight ) - 3 / $altitudeScale**2 - 2);

	## Evaluate velocity at the surface using Eq. 17
	$velocity = $vBU * exp(- $vFac * $integral);

	## Evaluate dispersion of impactor at impact using Eq. 15
	$dispersion = $pdiameter * (1 + 4 * $altitudeScale**2 * (exp($altitudeBU / (2 * $scaleHeight)) - 1)**2)**(1/2);

      }

    }

    ## Define velocity in km/s for output
    $velocity /= 1000;

  }

sub find_crater()
  {
    
    my $Cd;       # pi scaling diameter constant
    my $beta;     # pi scaling diameter constant
    
    my $anglefac = (sin ($theta * $pi / 180))**(1/3);
    if($ttype == 1){
      $Cd = 1.88;
      $beta = 0.22;
    }elsif($ttype == 2){
      $Cd = 1.54;
      $beta = 0.165;
    }else{
      $Cd = 1.6;
      $beta = 0.22;
    }
    
    if($depth != 0){		# calculate crater in water using Cd = 1.88 and beta = 0.22
      
      $wdiameter = 1.88 * (($mass / $tdensity)**(1/3)) * ( (1.61*$g*$pdiameter)/($velocity*1000)**2)**(- 0.22);
      $wdiameter *= $anglefac;
      
      $tdensity = 2700;	# change target density for seafloor crater calculation
    }
    
    # vseafloor == surface velocity if there is no water
    $Dtr = $Cd * (($mass / $tdensity)**(1/3)) * ( (1.61*$g*$pdiameter)/($vseafloor*1000)**2)**(- $beta);
    $Dtr *= $anglefac;
    
    if($dispersion >= $Dtr){		# if crater field is formed, compute crater dimensions assuming 
      $Dtr /= 2;			# impact of largest fragment (with diameter = 1/2 initial diameter)
    }
    
    $depthtr = $Dtr / 2.828;
    
    if($Dtr*1.25 >= 3200){                  # complex crater will be formed, use equation from McKinnon and Schenk (1985)
      $cdiameter = (1.17 * $Dtr**1.13) / (3200**0.13);
      $depthfr = 37 * $cdiameter**0.301;
    }else{                                  # simple crater will be formed
      
      #Diameter of final crater in m
      $cdiameter = 1.25 * $Dtr;
      
      #Breccia lens volume in m^3
      my $vbreccia = 0.032 * $cdiameter**3;		# in m^3
      
      #Rim height of final crater in m
      my $rimHeightf = 0.07 * $Dtr**4 / $cdiameter**3;
      
      #Thickness of breccia lens in m
      $brecciaThickness = 2.8 * $vbreccia * (($depthtr + $rimHeightf) / ($depthtr * $cdiameter**2));
      
      #Final crater depth (in m) = transient crater depth + final rim height - breccia thickness
      $depthfr = $depthtr + $rimHeightf - $brecciaThickness;
      
    }
    
    $vCrater = ($pi / 24) * ($Dtr/1000)**3;
    $vratio = $vCrater / $vEarth;
    
    if($velocity >= 12){
      $vMelt = $melt_coeff * ($energy_seafloor) * sin($theta * $pi / 180);		# energy_seafloor = energy_surface if there is no water layer
      if($vMelt > $vEarth){
	$vMelt = $vEarth;
      }
      $mratio = $vMelt / $vEarth;
      $mcratio = $vMelt / $vCrater;
    }

    $CraterRadiusFinal = 0.5E-3*$cdiameter/$R_earth;
    $CraterRadiusTransient = 0.5E-3*$Dtr/$R_earth;
    
  }  ### End of sub find_crater

### Subroutine to compute radii of ejecta thicknesses
sub find_ejecta
  {
    ejecta_radius(100, $Radius100mEjecta);
    ejecta_radius(10,  $Radius10mEjecta);
    ejecta_radius(1,   $Radius1mEjecta);
    ejecta_radius(0.1, $Radius10cmEjecta);
    ejecta_radius(0.01,$Radius1cmEjecta);
  }

### subroutine to return ejecta radius
sub ejecta_radius
  {
    my $third = 1./3.;
    my $EjectaThickness = $_[0];
    $_[1] = 1.E-3*($Dtr**4/(112*$EjectaThickness))**$third/$R_earth;
    if ($_[1] > $CraterRadiusTransient) {
      $qEjecta = 1;
    } else {
      $_[1] = 0.;
    }
    if ($_[1] > 0.5*$pi) {$_[1] = $CraterRadiusFinal};
  }

### Subroutine to compute radii of seismic shaking intensity
sub find_seismic
  {
    $magnitude = 0.67 * ((log ($energy_seafloor))/(log 10)) - 5.87;
    if ($magnitude >= 3) { seismic_radius($magnitude,3,$RadiusMercalliIII); $qSeismic = 1; }
    if ($magnitude >= 4) { seismic_radius($magnitude,4,$RadiusMercalliV); }
    if ($magnitude >= 6) { seismic_radius($magnitude,6,$RadiusMercalliVII); }
    if ($magnitude >= 7) { seismic_radius($magnitude,7,$RadiusMercalliIX); }
    if ($magnitude >= 9) { seismic_radius($magnitude,9,$RadiusMercalliXII); }
  }

### subroutine to return seismic radius
sub seismic_radius
  {
    my $mag     = $_[0];
    my $mag_eff = $_[1];
    my $radius1 = 42*($mag-$mag_eff)/$R_earth;
    my $radius2 = 208*($mag-$mag_eff-1.1644)/$R_earth;
    my $radius3 = 10**(($mag-6.399-$mag_eff)/1.66);
    $_[2] = max($radius1,$radius2,$radius3);
    if ($_[2] > 0.5*$pi) {$_[2] = $CraterRadiusFinal};
  }

sub find_airblast
  {
    ### Convert energy into kilotons for yield scaling
    my $energy_ktons = $energy_blast; #1000 * $energy_megatons;

    ### If this is a surface burst, the blast radii can be scaled by the yield
    if ($qCrater == 1) {
      airblast_radius_crater($energy_ktons,0.126,$RadiusAirblast126); # cars overturned (426 kPa)
      airblast_radius_crater($energy_ktons,0.155,$RadiusAirblast155); # steel buildings collapse (273 kPa)
      airblast_radius_crater($energy_ktons,0.660,$RadiusAirblast500); # wood building collapse (20 kPa)
      airblast_radius_crater($energy_ktons,1.651,$RadiusAirblast1160); # window shatter (5 kPa)
    } else {
      airblast_radius_crater($energy_ktons,0.660,$RadiusAirblast500); # wood building collapse (20 kPa)
      airblast_radius_crater($energy_ktons,1.651,$RadiusAirblast1160); # window shatter (5 kPa)
      airblast_radius_crater($energy_ktons,4.100,$RadiusAirblast3300); # window damage (1 kPa) 
    }
  }

### subroutine to return airblast radius
sub airblast_radius_crater
  {
    my $Ekt = $_[0];   # energy in kT
    my $rkt = $_[1];   # damage radius in 1kT expl.
    my $hkt = $altitudeBurst/($Ekt)**(1./3.);  # scaled burst altitude (m)
    $_[2] = $rkt*($Ekt)**(1./3.)/$R_earth; # radius of given damage effect
    # Consider if impact forms a crater or not; do not report blast zone if inside crater
    if ($qCrater == 1) {
      if ($_[2] < $CraterRadiusFinal ) {
	$_[2] = 0;
      } else {
	$qAirblast = 1;
	if ($_[2] > 0.5*$pi) { $_[2] = $CraterRadiusFinal; }
      }
    } else {
      # If scaled burst altitude is less blast effect radius compute based on slant range
      if ($hkt < $rkt*1000.) {
	$qAirblast = 1;
	$_[2] = ($rkt**2-($hkt/1000.)**2)**0.5*($Ekt)**(1./3.)/$R_earth;
      } else {
	$_[2] = 0;
      }
    }
  }


### Subroutine to compute tsunami wave amplitude and arrival time
sub find_tsunami
  {
    my $shallowness;                  # Ratio of Impactor diameter to water depth
    my $MaxWaveAmplitude;             # Maximum rim wave amplitude
    my $MaxWaveRadius;                # Radius where max rim wave is formed (upper estimate)
    my $MinWaveRadius;                # Radius where max rim wave is formed (lower estimate)
    my $CollapseWaveRadius;           # Radius where collapse wave is formed
    my $RimWaveExponent;              # Attenuation factor for rim wave
    my $CollapseWaveExponent;         # Attenuation factor for collapse wave
    my $MaxCollapseWaveAmplitude;     # Maximum collapse wave amplitude
    my $CollapseWaveAmplitude;        # Amplitude of collapse wave at specified distance

    ### Define parameters
    $shallowness = $pdiameter/$depth;
    $RimWaveExponent = 1.;
    $MaxWaveRadius = 0.001*$wdiameter;
    $MinWaveRadius = 0.0005*$wdiameter;

    ### Rim wave upper and lower limit estimates
    $MaxWaveAmplitude  = min(0.07*$wdiameter,$depth);
    if ($MaxWaveAmplitude > 1)    { tsunami_radius($MaxWaveRadius,$MaxWaveAmplitude,$RimWaveExponent,1,$Radius1mTsunami);     }
    if ($MaxWaveAmplitude > 10)   { tsunami_radius($MaxWaveRadius,$MaxWaveAmplitude,$RimWaveExponent,10,$Radius10mTsunami);   }
    if ($MaxWaveAmplitude > 100)  { tsunami_radius($MaxWaveRadius,$MaxWaveAmplitude,$RimWaveExponent,100,$Radius100mTsunami); }
    if ($MaxWaveAmplitude > 1000) { tsunami_radius($MaxWaveRadius,$MaxWaveAmplitude,$RimWaveExponent,1000,$Radius1kmTsunami); }

    ### Collapse wave correction to lower limit for deep-water impacts
#    if ($shallowness < 0.5) {
#      $CollapseWaveExponent = 3.*exp(-0.8*$shallowness);
#      $CollapseWaveRadius = 0.0025*$wdiameter;
#      $MaxCollapseWaveAmplitude = 0.06*min($wdiameter/2.828,$depth);
#      $CollapseWaveAmplitude = $MaxCollapseWaveAmplitude*($CollapseWaveRadius/$distance)**$CollapseWaveExponent;
#      $WaveAmplitudeLowerLimit = min($CollapseWaveAmplitude,$WaveAmplitudeLowerLimit);
#    }

  }

### subroutine to return seismic radius
sub tsunami_radius
  {
    my $Rmax = $_[0]/$R_earth;
    my $Amax = $_[1];
    my $Rexp = $_[2];
    my $A    = $_[3];
    $_[4] = $Rmax*($Amax/$A)**$Rexp;
    if ($_[4] > 0.5*$pi) {$_[4] = $CraterRadiusFinal};
  }

sub find_thermal
  {

    my $r_guess;
    my $eta = 3 * 10**-3;	                ## factor for scaling thermal energy
    my $T_star = 3000;		                ## temperature of fireball
    $Rf = 2* 10**-6* ($energy_surface)**(1/3);  ## Rf is in km
    my $sigma = 5.67 * 10**-8;	                ## Stephan-Boltzmann constant
    my $ignite_clothing = ($energy_megatons)**(1/6)*1.E6;
    my $delta;				# epicentral angle

    ### Radius of fireball as a fraction of Earth radius
    $RadiusFireball = $Rf/$R_earth;

    ### Radius of fireball visibility as a fraction of Earth radius
    $RadiusVisibleFireball = acos(1-$RadiusFireball);

    ### Radius at which clothing ignites
    my $r_upr = $RadiusVisibleFireball*$R_earth;
    my $r_low = $RadiusFireball*$R_earth;
    my $error = $ignite_clothing;
    my $count = 0;
    while (abs($error) > 1.E-3*$ignite_clothing and $count < 10) {
      $count += 1;
      $r_guess = 0.5*($r_low+$r_upr);
      $delta = $r_guess/$R_earth;
      $h = (1 - cos($delta))* $R_earth; ## h is in km, $R_earth is in km	
      my $del = acos($h / $Rf);
      my $f = (2/$pi)*($del - ($h/$Rf)*sin($del));
      $thermal_exposure = $f*($eta * $energy_surface)/(2 * $pi * ($r_guess * 1000)**2);
      $error = $thermal_exposure-$ignite_clothing;
      if ($error < 0.) {
	$r_upr = $r_guess;
      } else {
	$r_low = $r_guess;
      }
    }
    $RadiusClothingIgnition = $r_guess/$R_earth;
  }

### ---------------- ###
### HTML GUFF BEGINS ###
### ---------------- ###

sub print_begin
  {
    print <<EOF;
  <html>
  <head>
  <title>Earth Impact Effects Program</title>
  <script src="../../Build/Cesium/Cesium.js"></script>
  <script type="text/javascript" src="../../Apps/Sandcastle/Sandcastle-header.js"></script>
  <script type="text/javascript" src="../../ThirdParty/requirejs-2.1.20/require.js"></script>
  <script type="text/javascript">
  require.config({
      baseUrl : '../../Source',
      waitSeconds : 60
  });
</script>
</head>
EOF
  }

sub print_CesiumWidget
  {
    print <<EOF;
      <script>
      /* ----------------- */
      /* JAVASCRIPT BEGINS */
      /* ----------------- */
      function startup(Cesium) {
      'use strict';
      //Sandcastle_Begin
      Cesium.BingMapsApi.defaultKey = "AnYxEI_HDpXg2IRwTgoBs-8KllN86SawHfeEPheFEINFHngKO4B2mGa61yHxVtVM" 
      var viewer = new Cesium.Viewer('cesiumContainer', { infoBox : false });
      var entities = viewer.entities;
      //Create Entity "folders" to allow us to turn on/off entities as a group.
      var Airblast = entities.add(new Cesium.Entity());
      var Ejecta   = entities.add(new Cesium.Entity());
      var Crater   = entities.add(new Cesium.Entity());
      var SeismicS = entities.add(new Cesium.Entity());
      var Fireball = entities.add(new Cesium.Entity());
      var Tsunami  = entities.add(new Cesium.Entity());
      var allents = [Crater,Ejecta,Airblast,SeismicS,Fireball,Tsunami];
      var ii;
EOF
    print "      var centerLng = $latitude; var centerLat = $longitude;\n";

    ### If a crater is formed, add the option to plot crater
    if ($qCrater == 1) {
      print "       var radii_C = [$CraterRadiusFinal*1.274E7*0.5,$CraterRadiusTransient*1.274E7*0.5]\n";
      print "       var label_C = ['Final Crater','Transient Crater']\n";
      print "       var iC\n";
      #print "       radii_C.reverse()\n";
      #print "       label_C.reverse()\n";
      print <<EOF;
        for (iC=2-1;iC>=0;--iC){
            entities.add({
                parent : Crater,
                position : Cesium.Cartesian3.fromDegrees(centerLat,centerLng, 0),
                ellipse : { // Crater
                    semiMinorAxis: radii_C[iC],
                    semiMajorAxis: radii_C[iC],
                    material : Cesium.Color.WHITE.withAlpha(0.5),
                    height : 0,
                    outline : true,
                    outlineColor : Cesium.Color.BLACK,
                }
            });
            entities.add({
                parent : Crater,
                position : Cesium.Cartesian3.fromDegrees(centerLat, centerLng, 0),
                label : {
                    text : label_C[iC],
                    eyeOffset : new Cesium.Cartesian2(0,radii_C[iC],0),
                    horizontalOrigin : Cesium.HorizontalOrigin.CENTER,
                    verticalOrigin : Cesium.VerticalOrigin.BOTTOM,
                    //scaleByDistance : new Cesium.NearFarScalar(0.0, 1.0, 6370000, 0.0)
                    //font : '20px sans-serif',
                    //showBackground : true,
		    font : '12px Helvetica',
                    fillColor : Cesium.Color.WHITE,
                    outlineColor : Cesium.Color.BLACK,
                    outlineWidth : 2,
                    style : Cesium.LabelStyle.FILL_AND_OUTLINE,
		    scaleByDistance : new Cesium.NearFarScalar(1.5e2, 2.0, 1.5e7, 0.5)
                }
           });
        }
        Sandcastle.addToolbarButton('Crater',function(){
                for (ii=0;ii<6;ii++){
                   if (allents[ii].show){
                       allents[ii].show = !allents[ii].show;
                   }
                }
                if (!Crater.show){
                    viewer.camera.flyTo({
                        destination : Cesium.Cartesian3.fromDegrees(centerLat, centerLng, Math.max.apply(null,radii_C)*6),
                        orientation : {
                            heading : Cesium.Math.toRadians(0.0),
                            pitch : Cesium.Math.toRadians(-90.0),
                            roll : 0.0,
                            }
                    });
                    }
                Crater.show = !Crater.show;
        });
EOF

    }

    ### If Air blast occurs, add the option to plot air blast contours
    if ($qAirblast == 1) {
      print "      var radii_A = [$RadiusAirblast3300*1.274E7*0.5,$RadiusAirblast1160*1.274E7*0.5,$RadiusAirblast500*1.274E7*0.5,$RadiusAirblast155*1.274E7*0.5,$RadiusAirblast126*1.274E7*0.5];\n";
      print <<EOF;
        var label_A = ["Glass window damage (1 kPa)","Glass windows shatter (5 kPa)","Wood-frame buildings collapse (20 kPa)","Steel-framed buildings collapse","Vehicles overturned and distorted"];
        var iA;
        for (iA=5-1;iA>=0;--iA){
            entities.add({
                parent : Airblast,
                position : Cesium.Cartesian3.fromDegrees(centerLat,centerLng, 0),
                ellipse : { // Airblast
                    semiMinorAxis: radii_A[iA],
                    semiMajorAxis: radii_A[iA],
                    material : Cesium.Color.BLUE.withAlpha(0.25),
                    height : 0,
                    outline : true,
                }
            });
            if ((radii_A[iA])>0.0){
                 entities.add({
                     parent : Airblast,
                     position : Cesium.Cartesian3.fromDegrees(centerLat, centerLng, 0),
                     label : {
                         text : label_A[iA],
                         //font : '20px sans-serif',
                         //showBackground : true,
                         horizontalOrigin : Cesium.HorizontalOrigin.CENTER,
                         verticalOrigin : Cesium.HorizontalOrigin.BOTTOM,
                         eyeOffset : new Cesium.Cartesian2(0,radii_A[iA],0),
                         //scaleByDistance : new Cesium.NearFarScalar(0.0, 1.5, 6370000*3.5, 0.0),
		         font : '12px Helvetica',
                         fillColor : Cesium.Color.WHITE,
                         outlineColor : Cesium.Color.BLACK,
                         outlineWidth : 2,
                         style : Cesium.LabelStyle.FILL_AND_OUTLINE,
		         scaleByDistance : new Cesium.NearFarScalar(1.5e2, 2.0, 1.5e7, 0.5)
                     }
                });
           }
        }
        Sandcastle.addToolbarButton('Airblast',function(){
                for (ii=0;ii<6;ii++){
                   if (allents[ii].show){
                       allents[ii].show = !allents[ii].show;
                   }
                }
                if (!Airblast.show){
                    viewer.camera.flyTo({
                        destination : Cesium.Cartesian3.fromDegrees(centerLat, centerLng, Math.max.apply(null,radii_A)*6),
                        orientation : {
                            heading : Cesium.Math.toRadians(0.0),
                            pitch : Cesium.Math.toRadians(-90.0),
                            roll : 0.0,
                            }
                    });
                    }
                Airblast.show = !Airblast.show;
        });
EOF

    }

    ### If an impact plume is formed, add the option to plot the thermal radiation contours
    if ($qThermal == 1) {
      print "       var radii_F = [$RadiusVisibleFireball*1.274E7*0.5,$RadiusClothingIgnition*1.274E7*0.5,$RadiusFireball*1.274E7*0.5];\n";
      print <<EOF;
        var label_F = ["Fireball Visible","Clothing Ignites","Fireball"];
        var iF;
        for (iF=3-1;iF>=0;--iF){
            entities.add({
                parent : Fireball,
                position : Cesium.Cartesian3.fromDegrees(centerLat,centerLng, 0),
                ellipse : { // Airblast
                    semiMinorAxis: radii_F[iF],
                    semiMajorAxis: radii_F[iF],
                    material : Cesium.Color.CRIMSON.withAlpha(0.25),
                    height : 0,
                    outline : true,
                }
            });
            if ((radii_F[iF])>0.0){
                 entities.add({
                     parent : Fireball,
                     position : Cesium.Cartesian3.fromDegrees(centerLat, centerLng, 0),
                     label : {
                         text : label_F[iF],
                         //font : '20px sans-serif',
                         //showBackground : true,
                         horizontalOrigin : Cesium.HorizontalOrigin.CENTER,
                         verticalOrigin : Cesium.HorizontalOrigin.BOTTOM,
                         eyeOffset : new Cesium.Cartesian2(0,radii_F[iF],0),
                         //scaleByDistance : new Cesium.NearFarScalar(0.0, 3.0, 6370000*1.5, 0.0),
		         font : '12px Helvetica',
                         fillColor : Cesium.Color.WHITE,
                         outlineColor : Cesium.Color.BLACK,
                         outlineWidth : 2,
                         style : Cesium.LabelStyle.FILL_AND_OUTLINE,
		         scaleByDistance : new Cesium.NearFarScalar(1.5e2, 2.0, 1.5e7, 0.5)
                     }
                });
           }
        }
        Sandcastle.addToolbarButton('Fireball',function(){
                for (ii=0;ii<6;ii++){
                   if (allents[ii].show){
                       allents[ii].show = !allents[ii].show;
                   }
                }
                if (!Fireball.show){
                    viewer.camera.flyTo({
                        destination : Cesium.Cartesian3.fromDegrees(centerLat, centerLng, Math.max.apply(null,radii_F)*6),
                        orientation : {
                            heading : Cesium.Math.toRadians(0.0),
                            pitch : Cesium.Math.toRadians(-90.0),
                            roll : 0.0
                            }
                    });
                    }
                Fireball.show = !Fireball.show;
        });
EOF
    }

    ### If ejecta deposit is at least 1-cm thick, add option to plot ejecta thickness
    if ($qEjecta == 1) {
      print "       var radii_E = [$Radius1cmEjecta*1.274E7*0.5,$Radius10cmEjecta*1.274E7*0.5,$Radius1mEjecta*1.274E7*0.5,$Radius10mEjecta*1.274E7*0.5,$Radius100mEjecta*1.274E7*0.5];\n";
      print <<EOF;
        var label_E = ["Ejecta thickness > 1 cm","Ejecta thickness > 10 cm","Ejecta thickness > 1 m","Ejecta thickness > 10 m","Ejecta thickness > 100 m"];
        var iE;
        for (iE=5-1;iE>=0;--iE){
            entities.add({
                parent : Ejecta,
                position : Cesium.Cartesian3.fromDegrees(centerLat,centerLng, 0),
                ellipse : { // Ejecta
                    semiMinorAxis: radii_E[iE],
                    semiMajorAxis: radii_E[iE],
                    material : Cesium.Color.SKYBLUE.withAlpha(0.2),
                    height : 0,
                    outline : true,
                }
            });
            if ((radii_E[iE])>0.0){
                entities.add({
                    parent : Ejecta,
                    position : Cesium.Cartesian3.fromDegrees(centerLat, centerLng, 0),
                    label : {
                        text : label_E[iE],
                        //font : '20px sans-serif',
                        //showBackground : true,
                        horizontalOrigin : Cesium.HorizontalOrigin.CENTER,
                        verticalOrigin : Cesium.HorizontalOrigin.BOTTOM,
                        eyeOffset : new Cesium.Cartesian2(0,radii_E[iE],0),
                        //scaleByDistance : new Cesium.NearFarScalar(0.0, 1.0, 6370000, 0.0)
		        font : '12px Helvetica',
                        fillColor : Cesium.Color.WHITE,
                        outlineColor : Cesium.Color.BLACK,
                        outlineWidth : 2,
                        style : Cesium.LabelStyle.FILL_AND_OUTLINE,
		        scaleByDistance : new Cesium.NearFarScalar(1.5e2, 2.0, 1.5e7, 0.5)
                    }
                });
           }
        }
        entities.add({
            parent : Ejecta,
            position : Cesium.Cartesian3.fromDegrees(centerLat,centerLng, 0),
            ellipse : { // Crater
                semiMinorAxis: radii_C[0],
                semiMajorAxis: radii_C[0],
                material : Cesium.Color.WHITE.withAlpha(0.2),
                height : 0,
                outline : true,
            }
        });
        entities.add({
            parent : Ejecta,
            position : Cesium.Cartesian3.fromDegrees(centerLat, centerLng, 0),
            label : {
                text : 'Crater',
                //font : '20px sans-serif',
                //showBackground : true,
                horizontalOrigin : Cesium.HorizontalOrigin.CENTER,
                verticalOrigin : Cesium.HorizontalOrigin.BOTTOM,
                eyeOffset : new Cesium.Cartesian2(0,-radii_C[0],0),
                //scaleByDistance : new Cesium.NearFarScalar(0.0, 1.0, 6370000, 0.0)
		font : '12px Helvetica',
                fillColor : Cesium.Color.WHITE,
                outlineColor : Cesium.Color.BLACK,
                outlineWidth : 2,
                style : Cesium.LabelStyle.FILL_AND_OUTLINE,
		scaleByDistance : new Cesium.NearFarScalar(1.5e2, 2.0, 1.5e7, 0.5)
            }
        });
        Sandcastle.addToolbarButton('Ejecta',function(){
                for (ii=0;ii<6;ii++){
                   if (allents[ii].show){
                       allents[ii].show = !allents[ii].show;
                   }
                }
                if (!Ejecta.show){
                    viewer.camera.flyTo({
                        destination : Cesium.Cartesian3.fromDegrees(centerLat, centerLng, Math.max.apply(null,radii_E)*6),
                        orientation : {
                            heading : Cesium.Math.toRadians(0.0),
                            pitch : Cesium.Math.toRadians(-90.0),
                            roll : 0.0
                            }
                    });
                    }
                Ejecta.show = !Ejecta.show;
        });
EOF
  }
    ### If at least Mercalli intensity III is reached, add the option to plot seismic shaking intensity
    if ($qSeismic == 1) {
      print "      var radii_S = [$RadiusMercalliIII*1.274E7*0.5,$RadiusMercalliV*1.274E7*0.5,$RadiusMercalliVII*1.274E7*0.5,$RadiusMercalliIX*1.274E7*0.5,$RadiusMercalliXII*1.274E7*0.5];\n";
      print <<EOF
        var label_S = ["Mercalli Intensity III; Vibration like passing of light trucks.","Mercalli Intensity V; Small unstable objects displaced.","Mercalli Intensity VII; Difficult to stand; landslides; damage to buildings.","Mercalli Intensity IX","Mercalli Intensity XII"];
        var iS;
        for (iS=5-1;iS>=0;--iS){
            entities.add({
                parent : SeismicS,
                position : Cesium.Cartesian3.fromDegrees(centerLat,centerLng, 0),
                ellipse : { // Seismic Shaking
                    semiMinorAxis: radii_S[iS],
                    semiMajorAxis: radii_S[iS],
                    material : Cesium.Color.GREEN.withAlpha(0.33),
                    height : 0,
                    outline : true,
                }
            });
            if ((radii_S[iS])>0.0){
              entities.add({
                  parent : SeismicS,
                  position : Cesium.Cartesian3.fromDegrees(centerLat, centerLng, 0),
                  label : {
                      text : label_S[iS],
                      //font : '20px sans-serif',
                      //showBackground : true,
                      horizontalOrigin : Cesium.HorizontalOrigin.CENTER,
                      verticalOrigin : Cesium.HorizontalOrigin.BOTTOM,
                      eyeOffset : new Cesium.Cartesian2(0,radii_S[iS],0),
                      //scaleByDistance : new Cesium.NearFarScalar(0.0, 2.0, 6370000*3.0, 0.0)
	              font : '12px Helvetica',
                      fillColor : Cesium.Color.WHITE,
                      outlineColor : Cesium.Color.BLACK,
                      outlineWidth : 2,
                      style : Cesium.LabelStyle.FILL_AND_OUTLINE,
	              scaleByDistance : new Cesium.NearFarScalar(1.5e2, 2.0, 1.5e7, 0.5)
                  }
              });
            }
        }
        Sandcastle.addToolbarButton('Seismic Shaking',function(){
                for (ii=0;ii<6;ii++){
                   if (allents[ii].show){
                       allents[ii].show = !allents[ii].show;
                   }
                }
                if (!SeismicS.show){
                    viewer.camera.flyTo({
                        destination : Cesium.Cartesian3.fromDegrees(centerLat, centerLng, Math.max.apply(null,radii_S)*6),
                        orientation : {
                            heading : Cesium.Math.toRadians(0.0),
                            pitch : Cesium.Math.toRadians(-90.0),
                            roll : 0.0
                            }
                    });
                    }
                SeismicS.show = !SeismicS.show;
        });
EOF
    }

    ### If tsunami height is at least 1 m, add the option to plot tsunami wave height
    if ($qTsunami == 1) {
      print "       var radii_T = [$Radius1mTsunami*1.274E7*0.5,$Radius10mTsunami*1.274E7*0.5,$Radius100mTsunami*1.274E7*0.5,$Radius1kmTsunami*1.274E7*0.5];\n";
      print <<EOF
        var label_T = ["Tsunami wave height > 1 m", "Tsunami wave height > 10 m","Tsunami wave height > 100 m","Tsunami wave height > 1 km"];
        var iT;
        for (iT=0;iT<5;iT++){
            entities.add({
                parent : Tsunami,
                position : Cesium.Cartesian3.fromDegrees(centerLat,centerLng, 0),
                ellipse : { // Tsunami
                    semiMinorAxis: radii_T[iT],
                    semiMajorAxis: radii_T[iT],
                    material : Cesium.Color.CYAN.withAlpha(0.25),
                    height : 0,
                    outline : true,
                }
            });
            if ((radii_T[iT])>0.0){
              entities.add({
                  parent : Tsunami,
                  position : Cesium.Cartesian3.fromDegrees(centerLat, centerLng, 0),
                  label : {
                      text : label_T[iT],
                      font : '20px sans-serif',
                      showBackground : true,
                      horizontalOrigin : Cesium.HorizontalOrigin.CENTER,
                      verticalOrigin : Cesium.HorizontalOrigin.BOTTOM,
                      eyeOffset : new Cesium.Cartesian2(0,radii_T[iT],0),
                      scaleByDistance : new Cesium.NearFarScalar(0.0, 2.0, 6370000*4.0, 0.0)
                  }
              });
            }
        }
        Sandcastle.addToolbarButton('Tsunami',function(){
                for (ii=0;ii<6;ii++){
                   if (allents[ii].show){
                       allents[ii].show = !allents[ii].show;
                   }
                }
                if (!Tsunami.show){
                    viewer.camera.flyTo({
                        destination : Cesium.Cartesian3.fromDegrees(centerLat, centerLng, Math.max.apply(null,radii_T)*6),
                        orientation : {
                            heading : Cesium.Math.toRadians(0.0),
                            pitch : Cesium.Math.toRadians(-90.0),
                            roll : 0.0
                            }
                    });
                    }
                Tsunami.show = !Tsunami.show;
        });
EOF
    }

    ### Print the remainder of the script
    print <<EOF;
        for (ii=0;ii<6;ii++){
           if (allents[ii].show){
               allents[ii].show = !allents[ii].show;
           }
        }
        viewer.camera.flyTo({
            destination : Cesium.Cartesian3.fromDegrees(centerLat, centerLng, 10000.0),
            orientation : {
                heading : Cesium.Math.toRadians(0.0),
                pitch : Cesium.Math.toRadians(-90.0),
                roll : 0.0,
                }
        });

        var pinBuilder = new Cesium.PinBuilder();
        var impactPin = viewer.entities.add({
            name : 'Impact',
            position : Cesium.Cartesian3.fromDegrees(centerLat, centerLng),
            billboard : {
                image : pinBuilder.fromText('!', Cesium.Color.BLACK, 48).toDataURL(),
                verticalOrigin : Cesium.VerticalOrigin.BOTTOM,
            }
        });
	}
          
        if (typeof Cesium !== "undefined") {
            startup(Cesium);
        } else if (typeof require === "function") {
            require(["Cesium"], startup);
        }
        /* --------------- */
        /* JAVASCRIPT ENDS */
        /* --------------- */
	</script>
EOF

  }

#<script src="../saved_files/saved_resource" type="text/javascript"></script>
### Subroutine to format time into appropriate units and significant figures
sub FormatTime
  {
    ### Default time unit is seconds
    $_[1] = FormatSigFigs($_[0],$sigfigs);
    $_[2] = "seconds";

    ### Convert to minutes or hours as required
    if ($_[0] > 3600) {
      $_[1] = FormatSigFigs($_[0]/3600.,$sigfigs);
      $_[2] = "hours";
    } elsif ($_[0] > 60.) {
      $_[1] = FormatSigFigs($_[0]/60.,$sigfigs);
      $_[2] = "minutes";
    } elsif ($_[0] < 1.) {
      $_[1] = FormatSigFigs($_[0]*1000.,$sigfigs);
      $_[2] = "milliseconds";
    }
  }

### Subroutine to format distance into appropriate units and significant figures
sub FormatDistance
  {
    ### Default SI distance unit is m
    $_[1] = FormatSigFigs($_[0],$sigfigs);
    $_[2] = "meters";

    ### Alternative distance unit is feet
    $_[3] = FormatSigFigs($_[0]*3.28,$sigfigs); #meters to feet
    $_[4] = "feet";

    ### Convert to cm, microns or km
    if ($_[0] < 0.001) {
      $_[1] = FormatSigFigs($_[0]*1000000,$sigfigs);
      $_[2] = "microns";
      $_[3] = FormatSigFigs($_[0]*39400,$sigfigs); #meters to thousandths of an inch
      $_[4] = "thousandths of an inch";
    } elsif ($_[0] < 0.01) {
      $_[1] = FormatSigFigs($_[0]*1000,$sigfigs);
      $_[2] = "mm";
      $_[3] = FormatSigFigs($_[0]*394,$sigfigs); #meters to thousandths of an inch
      $_[4] = "tenths of an inch";
    } elsif ($_[0] < 1) {
      $_[1] = FormatSigFigs($_[0]*100,$sigfigs);
      $_[2] = "cm";
      $_[3] = FormatSigFigs($_[0]*39.37,$sigfigs); #meters to inches
      $_[4] = "inches";
    } elsif ($_[0] > 1000) {
      $_[1] = FormatSigFigs($_[0]*0.001,$sigfigs);
      $_[2] = "km";
      $_[3] = FormatSigFigs($_[0]*0.000621,$sigfigs); #meters to miles
      $_[4] = "miles";
    }
  }

sub echo_inputs
  {
    ### input echo
    my $FormattedDistanceMet;
    my $MetUnit;
    my $FormattedDistanceImp;
    my $ImpUnit;

    print "<dl>\n<dt>\n<h2>Your Inputs:</h2>\n";
    FormatDistance($pdiameter,$FormattedDistanceMet,$MetUnit,$FormattedDistanceImp,$ImpUnit);
    printf("<dd>Projectile diameter:  <b>%.2f %s ( = %.2f %s )</b> \n", $FormattedDistanceMet, $MetUnit, $FormattedDistanceImp, $ImpUnit);
    print "<dd>Projectile Density:  <b>$pdensity kg/m<sup>3</sup></b>\n";
    FormatDistance($vInput*1000,$FormattedDistanceMet,$MetUnit,$FormattedDistanceImp,$ImpUnit);
    printf("<dd>Impact Velocity:  <b>%.2f %s per second ( = %.2f %s per second ) </b> \n", $FormattedDistanceMet, $MetUnit, $FormattedDistanceImp, $ImpUnit);
    if($vInput >= 72){
      print "<b><i>(Your chosen velocity is higher than the maximum for an object orbiting the sun)</i></b>";
    }
    print "<dd>Impact Angle:  <b>$theta degrees</b>\n";
    print "<dd>Target Density:  <b>$tdensity kg/m<sup>3</sup></b>\n";
    if($depth != 0){
      FormatDistance($depth,$FormattedDistanceMet,$MetUnit,$FormattedDistanceImp,$ImpUnit);
      printf("<dd>Target Type:  Liquid water of depth <b>%.1f %s ( = %.1f %s )</b>, over crystalline rock. \n", $FormattedDistanceMet, $MetUnit, $FormattedDistanceImp, $ImpUnit);
    }elsif($tdensity == 1000){
      print "<dd>Target Type:  Ice\n";
    }elsif($tdensity == 2500){
      print "<dd>Target Type: Sedimentary Rock\n";
    }else{
      print "<dd>Target Type:  Crystalline Rock\n";
    }
    print"</dl>\n";
    
  } ### end of echo_inputs



sub print_title
  {

    print <<EOF;
 <!body style="font-family:calibri" text="#FFFFFF" bgcolor="#000000" link="#FFFFFF" vlink="#FFFFFF" alink="#FF0000">
 <link rel="stylesheet" href="../ImpactEarth.css">
 <body>


<table COLS=2 WIDTH=100%>
<tr>
<td><img class="banner_image" SRC="../imperial.png" BORDER=5></td>
<td><img class="banner_image" align=right SRC="../purduemark.png" BORDER=5></td>
</tr>
</table>
<h1 align=center><a href="../index.html">Impact Effects</a></h1>
<h3 align=center><a href="http://www.imperial.ac.uk/people/g.collins">Gareth Collins</a>, <a href="http://www.cfa.harvard.edu/~rmarcus/index.html">Robert Marcus</a>, and <a href="http://www.eaps.purdue.edu/people/faculty-pages/melosh.html">H. Jay Melosh</a></h3>

<p>Please note:  the results below are estimates based on current (limited) understanding of the impact process and come with large uncertainties;  they should be used with caution, particularly in the case of peculiar input parameters.  All values are given to three significant figures but this does not reflect the precision of the estimate.  For more information about the uncertainty associated with our calculations and a full discussion of this program, please refer to this <a href="../ImpactEffects/effects.pdf">article</a></p><h3 align=center style="color:#fA6140;">Click each effect button (e.g. "Crater") to see the extent of each impact effect!</h2>
EOF


    #print"<div id=\"map3d\" style=\"height: 520px; width: 780px;\"></div>\n"

  }

sub reprint_form
  {

    print header();

    print <<EOF;
<!DOCTYPE html>
<html>
<head>
<title>Earth Impact Effects Program</title>
<link rel="stylesheet" href="../ImpactEarth.css">
</head>
 <body>
 <!body style="font-family:calibri" text="#FFFFFF" bgcolor="#000000" link="#FFFFFF" vlink="#FFFFFF" alink="#FF0000">

<table COLS=2 WIDTH=100%>
<tr>
<td><img class="banner_image" SRC="../imperial.png" BORDER=5></td>
<td><img class="banner_image" align=right SRC="../purduemark.png" BORDER=5></td>
</tr>
</table>
<h1 align=center>Impact Effects</h1>
<h2 align=center>Damage Map Version</h2>
<h3 align=center><a href="http://www.imperial.ac.uk/people/g.collins">Gareth Collins</a>, <a href="http://www.cfa.harvard.edu/~rmarcus/index.html">Robert Marcus</a>, and <a href="http://www.eaps.purdue.edu/people/faculty-pages/melosh.html">H. Jay Melosh</a></h3>

<p>Welcome to the Earth Impact Effects Program: an easy-to-use, interactive web site for estimating the regional environmental consequences of an impact on Earth.  This program will estimate the ejecta distribution, ground shaking, atmospheric blast wave, and thermal effects of an impact as well as the size of the crater produced. </p>

<p>Please enter a location on Earth to impact, then enter values in the boxes below to describe your impact of choice. Select the impact effect you are interested in and rhen click "Display Impact Effects" to see the damage zone!</p>
EOF

    print "<font color=ff3d3d><dl><dt>Please re-enter the following items:";

    if ($valid[6] == 0) {
      print "<dd>Latitude";
      print "<dd>Note:  Latitude must be between 0 (equator) and 90 degrees (pole); use negative values for Southern latitudes.";
    }

    if ($valid[8] == 0) {
      print "<dd>Longitude";
      print "<dd>Note:  Longitude must be between 0 and 180 degrees; use positive values for eastern longitudes and negative values for western longitudes.";
    }

    if ($valid[0] == 0) {
      print "<dd>Projectile Diameter";
    }
	
    if ($valid[1] == 0) {
      print "<dd>Projectile Density";
    }
	
    if ($valid[2] == 0) {
      print "<dd>Impact Velocity";
      if ($velocity >= 3 * 10**5) {
	print "<dd>Note:  The velocity must be less than the velocity of light (3 x 10<sup>5</sup>km/s)."; 
      }
    }
	
    if ($valid[3] == 0) {
      print "<dd>Impact Angle";
    }
	
    if ($valid[4] == 0) {
      print "<dd>Target Type";
    }
    if ($valid[9] == 0) {
      print "<dd> Water Depth: invalid characters detected, only the numerals 0-9 are accepted.";
    }
	

    print "</font></dl>";
	
    print <<EOF;
		<form action ="../cgi-bin/impact.cgi">
	
		<h2 align=left>Location of Impact</h2>
EOF


    if ($valid[6] == 1) {	
      print "<input type=\"text\" name=\"latitude\" id=\"latinput\" onchange=\"changeNOTlatlon()\" value=$latitude> and";
    } else {
      print"<input type=\"text\" name=\"latitude\" id=\"latinput\" onchange=\"changeNOTlatlon()\"> and";
    }

    if ($valid[8] == 1) {	
      print "<input type=\"text\" name=\"longitude\" id=\"loninput\" onchange=\"changeNOTlatlon()\" value=$longitude> or";
    } else {
      print"<input type=\"text\" name=\"longitude\" id=\"loninput\" onchange=\"changeNOTlatlon()\"> or";
    }

    print <<EOF;
	<select name="LocationSelect" id="locselec" onchange="changeNOTloc()">
	  <option value="0">Select a City
	  <option value="1">London
	  <option value="2">Los Angeles
	  <option value="3">New York
	  <option value="4">Berlin
	  <option value="5">Paris
	  <option value="6">Johannesburg
	  <option value="7">Sydney
	  <option value="8">Cardiff
	  <option value="9">Edinburgh
	</select> or 
	<select name="CraterSelect" id="crtselec" onchange="changeNOTcrt()">
	  <option value="0">Select a crater
	  <option value="1">Acraman (Australia)
	  <option value="2">Araguainha (Brazil)
	  <option value="3">Barringer (USA)
	  <option value="4">Chicxulub (Mexico)
	  <option value="5">Chesapeake Bay (USA)
	  <option value="6">Eltanin (Bellingshausen Sea)
	  <option value="7">Popiagai (Russia)
	  <option value="8">Ries (Germany)
	  <option value="9">Siljan (Sweden)
	  <option value="10">Sudbury (Canada)
	  <option value="11">Vredefort (South Africa)
	  <option value="12">Silverpit (North Sea)
	</select>
      </blockquote>
      <script>
      function changeNOTlatlon(){
          var loc = document.getElementById("locselec");
          var crt = document.getElementById("crtselec");
          loc.value = 0;
          crt.value = 0;
      }
      function changeNOTloc(){
          var crt = document.getElementById("crtselec");
          var lat = document.getElementById("latinput");
          var lon = document.getElementById("loninput");
          crt.value =  0;
	  lat.value = '';
          lon.value = '';
      }
      function changeNOTcrt(){
          var loc = document.getElementById("locselec");
          var lat = document.getElementById("latinput");
          var lon = document.getElementById("loninput");
          loc.value =  0;
	  lat.value = '';
          lon.value = '';
      }
      </script> 
EOF

    print <<EOF;
		<h2 align=center>Enter Impact Parameters</h2>
		<h3 align=left>Projectile Parameters</h3>
		<blockquote>
		Projectile Diameter (in meters)
EOF


    if ($valid[0] == 1) {
      print "<input type=\"text\" name=\"diam\" id=\"pdinput\" onchange=\"NOTpdinp()\" value=$pdiameter>";
    } else {
      print "<input type=\"text\" name=\"diam\" id=\"pdinput\" onchange=\"NOTpdinp()\">";
    }
    print <<EOF;
	or 
	<select name="pdiameter_select" id="pdselec" onchange="NOTpdsel()">
	  <option value="0">Select from a list
	  <option value="0.25">Football (25 cm)
	  <option value="5">Double-decker bus (5 m)
	  <option value="20">Cricket wicket (20 m)
	  <option value="52.">Nelson's column (52 m)
	  <option value="87.">Queen's Tower (87 m)
	  <option value="320.">Wembley Stadium (320 m)
	  <option value="1340.">Ben Nevis (1.3 km)
	  <option value="10000.">Jersey (10 km)
	  <option value="20000.">Isle of Wight (20 km)
	  <option value="0">-- Asteroids --
	  <!!--option value="952000."Ceres (952 km)>
	  <!!--option value="529000."Vesta (529 km)>
	  <!!--option value="100000."Lutitia (100 km)>
	  <!!--option value="53000."Mathilde (53 km)>
	  <!!--option value="33000."Ida (33 km)>
	  <option value="500.">Itokawa (500 m)
	  <option value="325.">Apophis (325 m)
	  <option value="250.">Bennu (250 m)
	  <option value="0">-- Comets --
	  <option value="6300.">Tempel 1 (6.3 km)
	  <option value="4200.">67P/Churyumov–Gerasimenko (4.2 km)
	  <option value="4200.">Wild 2 (4.2 km)
	  <option value="1500.">Hartley 2 (1.5 km)
	  <option value="0">-- Past events --
	  <option value="20">Chelyabinsk (20 m)
	  <option value="50">Tunguska (50 m; stone)
	  <option value="50">Barringer (50 m; iron)
	  <option value="1500">Ries (1.5 km)
	  <option value="14000">Chicxulub (14 km)
	</select>
EOF

    print "<p>Projectile Density (in kg/m<sup>3</sup>) ";

    if ($valid[1] == 1) {
      print "<input type=\"text\" name=\"pdens\" id=\"pDNinput\" onchange=\"NOTpDNinp()\" value=$pdensity> or"; 
    } else {
      print "<input type=\"text\" name=\"pdens\" id=\"pDNinput\" onchange=\"NOTpDNinp()\" > or";
    }
    print <<EOF;
	  <select name="pdens_select" id="pDNselec" onchange="NOTpDNsel()">
	    <option value="0">Select from a list
	    <option value="1000">1000 kg/m^3 for ice
	    <option value="1500">1500 kg/m^3 for porous rock
	    <option value="3000">3000 kg/m^3 for dense rock
	    <option value="8000">8000 kg/m^3 for iron
	  </select>
      <script>
      function NOTpdinp(){
          var pdslc = document.getElementById("pdselec");
          pdslc.value = 0;
      }
      function NOTpdsel(){
          var pdinp = document.getElementById("pdinput");
          pdinp.value = '';
      }
      function NOTpDNinp(){
          var pDNslc = document.getElementById("pDNselec");
          pDNslc.value = 0;
      }
      function NOTpDNsel(){
          var pDNinp = document.getElementById("pDNinput");
          pDNinp.value = '';
      }
      </script> 
      </blockquote>
EOF

print <<EOF;
	<h3 align=left>Impact Parameters</h3>
	<blockquote>
	Impact Velocity (in km/s)
EOF

    if ($valid[2] == 1) {
      print "<input type=\"text\" name=\"vel\" id=\"velinp\" onchange=\"NOTvelinp()\" value=$vInput>";
    } else {
      print "<input type=\"text\" name=\"vel\" id=\"velinp\" onchange=\"NOTvelinp()\">";
    }
    print <<EOF;
                <select name="velocity_select" id="velsel" onchange="NOTvelsel()">
                  <option value="0">Select from a list
                  <option value="11.2">11.2 km/s (escape velocity)
                  <option value="17">17 km/s (typical asteroid)
                  <option value="51">51 km/s (typical comet)
                  <option value="72">72 km/s (max. speed bound to Sun)
                </select>

		<p>This is the velocity of the projectile before it enters the atmosphere.  The minimum impact velocity on Earth is 11 km/s.  Typical
		impact velocities are 17 km/s for asteroids and 51 km/s for comets.  The maximum Earth impact velocity for objects orbiting the sun is
		72 km/s.
	
EOF
	




    print "<p>Impact Angle (in degrees) ";

    if ($valid[3] == 1) {
      print "<input type=\"text\" name=\"theta\" id=\"thtinp\" onchange=\"NOTthtinp()\" value=$theta>";
    } else {
      print "<input type=\"text\" name=\"theta\" id=\"thtinp\" onchange=\"NOTthtinp()\">";
    }

      print <<EOF;	
        <select name="angle_select" id="thtsel" onchange="NOTthtsel()">
          <option value="0">Select from a list
          <option value="90">90 degrees (vertical)
          <option value="45">45 degrees (most frequent)
          <option value="15">15 degrees (shallowest to form circular crater) 
        </select>
      <script>
      function NOTvelinp(){
          var entry = document.getElementById("velsel");
          entry.value = 0;
      }
      function NOTvelsel(){
          var entry = document.getElementById("velinp");
          entry.value = '';
      }
      function NOTthtinp(){
          var entry = document.getElementById("thtsel");
          entry.value = 0;
      }
      function NOTthtsel(){
          var entry = document.getElementById("thtinp");
          entry.value = '';
      }
      </script> 
	  
EOF

    print <<EOF;
	
		<p>The impact angle is measured from a plane tangent to the impact surface.  This angle is 90 degrees for a vertical impact.  The most
		probable angle of impact is 45 degrees.
		</blockquote>
		<h3 align=left>Target Parameters</h3>
		<blockquote>
		Target Type
EOF


    if ($valid[4] == 1) {
#      print "<input type=\"text\" name=\"tdens\" value=$tdensity size=10> or";
    } else {
###      print "<input type=\"text\" name=\"tdens\" size=10> or ";
    } 

    print <<EOF;
	<br>
	<blockquote>
	  <input type="radio" name="tdens" value ="1000">Water
	  of depth:  <input type="text" name="wdepth" size=10>
	  <select name="wdepthUnits">
	    <option value="1">meters
	    <option value="2">feet
	  </select>
	  <br>
	  <input type="radio" name="tdens" value ="2500">Sedimentary Rock
	  <br>
	  <input type="radio" name="tdens" value ="2750">Crystalline Rock
	  <br>
	</blockquote>
      </blockquote>	

EOF
    print <<EOF;
		<br>
		<center>
		<input type="submit" value="Display Impact Effects">
		<input type="reset" value="Reset Form">
		</center>
		
		</form>
		<p>
		<br>
EOF
		
	print_pdf();
	print "<hr>\n<br>\n</body>\n</html>\n";



}                 ###  End of sub reprint_form


sub print_crater
  {
    my $DistMet;
    my $UnitMet;
    my $DistImp;
    my $UnitImp;
    my $melt_thickness;	# thickness of melt in km
    $melt_thickness = $vMelt / ($pi * ($Dtr/2000)**2);

    ### crater results
    print "<dl>\n<dt>\n<h2>Crater Dimensions:</h2>\n";
	
    print <<EOF;
	<dd><a target="blank" href="../ImpactEffects/craterexp.html#crater">What does this mean?</a><br><br><br>
EOF

    ### Print details of crater in water layer
    if($depth != 0){
      FormatDistance($wdiameter,$DistMet,$UnitMet,$DistImp,$UnitImp);
      printf("<dd>The crater opened in the water has a diameter of <b>%g %s ( = %g %s )</b>.", $DistMet, $UnitMet, $DistImp, $UnitImp);
      if($Dtr > 0){
	print "<dd><br>";
	print "<dd>For the crater formed in the seafloor:";
      }
    }
	
    ### Report consequences of atmospheric disruption
    if($pdiameter < 1000){

      if($dispersion >= $Dtr){
	print "<dd>The result of the impact is a crater field, not a single crater.  The following dimensions are for the crater produced by the largest fragment.";
	print "<dd><br>";
      }elsif($iFactor < 1){
	print "<dd>Crater shape is normal in spite of atmospheric crushing; fragments are not significantly dispersed.";
	print "<dd><br>";
      }
    }

    ### Report transient crater dimensions
    print <<EOF;
	<dd><a target="blank" href="../ImpactEffects/craterglos.html#transient">Transient Crater</a> Diameter:
EOF
    FormatDistance($Dtr,$DistMet,$UnitMet,$DistImp,$UnitImp);
    printf("<b>%g %s ( = %g %s )</b>",$DistMet,$UnitMet,$DistImp,$UnitImp);
    FormatDistance($depthtr,$DistMet,$UnitMet,$DistImp,$UnitImp);
    printf("<dd>Transient Crater Depth:  <b>%g %s ( = %g %s )</b>", $DistMet,$UnitMet,$DistImp,$UnitImp);
    print "<dd><br>";
      
    ### If melt volume is equivalent to the volume of the Earth finish
    if($mratio == 1){
      print "</dl>";
      return;
    }
    
    ### Report final crater dimensions
    print <<EOF;
	<dd><a target="blank" href="../ImpactEffects/craterglos.html#final">Final Crater</a> Diameter:
EOF
      
    FormatDistance($cdiameter,$DistMet,$UnitMet,$DistImp,$UnitImp);
    printf("<b>%g %s ( = %g %s )</b>",$DistMet,$UnitMet,$DistImp,$UnitImp);
    FormatDistance($depthfr,$DistMet,$UnitMet,$DistImp,$UnitImp);
    printf("<dd>Final Crater Depth:  <b>%g %s ( = %g %s )</b>", $DistMet,$UnitMet,$DistImp,$UnitImp);

    ### Report the type of crater formed
    if($mcratio >= 1){
      print "<dd>The final crater is replaced by a large, circular melt province.";
    }elsif($cdiameter >= 3200){
      print <<EOF;
	<dd>The crater formed is a <a target="blank" href="../ImpactEffects/craterglos.html#complex">complex crater</a>.
EOF
    }else{
      print <<EOF;
	<dd>The crater formed is a <a target="blank" href="../ImpactEffects/craterglos.html#simple">simple crater</a>
EOF
      print "<dd><br>";
      FormatDistance($brecciaThickness,$DistMet,$UnitMet,$DistImp,$UnitImp);
      printf("<dd>The floor of the crater is underlain by a lens of broken rock debris (breccia) with a maximum thickness of <b>%g %s ( = %g %s )</b>.", $DistMet,$UnitMet,$DistImp,$UnitImp);
    }

    ### Report the melt volume and thickness
    if($velocity >= 12 and $mratio < 0.1){

      ### Melt volume
      if($vMelt < 0.001){
	printf("<dd>The volume of the target melted or vaporized is %g m<sup>3</sup> = %g feet<sup>3</sup>\n", FormatSigFigs($vMelt * 10**9, $sigfigs), FormatSigFigs($vMelt * 10**9 * 3.28**3, $sigfigs));
      }else{
	printf("<dd>The volume of the target melted or vaporized is %g km<sup>3</sup> = %g miles<sup>3</sup>\n", FormatSigFigs($vMelt, $sigfigs), FormatSigFigs($vMelt * 0.2399, $sigfigs));
      }

      ### Melt thickness for complex crater (not melt pool)
      if($mcratio < 1){
	print "<dd>Roughly half the melt remains in the crater";
	if($Dtr >= 3200){
	  FormatDistance($melt_thickness*1000,$DistMet,$UnitMet,$DistImp,$UnitImp);
	  printf(", where its average thickness is <b>%g %s ( = %g %s )</b>. \n", $DistMet,$UnitMet,$DistImp,$UnitImp);
	}
      }
    }else{
      print "<dd>At this impact velocity ( < 12 km/s), little shock melting of the target occurs.";
    }

    ### Melt pool
    if($mcratio >= 1){
      printf("<dd>Melt volume = %g times the crater volume\n", FormatSigFigs($mcratio, $sigfigs));
      print "<dd>At this size, the crater forms in its own melt pool.";
    }
    
    
    print "</dl>";
    
    
  }  ### end of print_crater


### Subroutine to output the results of the energy calculation
sub print_energy
  {

    ### Format energy in scientific notation and in different units
    $energy_power = log($energy0)/log(10);
    $energy_power = int($energy_power);
    $energy0 /= 10**$energy_power;
	
    $megaton_power = log($energy0_megatons)/log(10);
    $megaton_power = int($megaton_power);
    $energy0_megatons /= 10**$megaton_power;

    ### Print the energy
    print "<dl>\n<dt>\n<h2>Energy:</h2>\n";
    if ($energy_power == 0) {
      printf ("<dd>Energy before atmospheric entry: <b>%.2f Joules</b> ", $energy0);
    } else {
      printf ("<dd>Energy before atmospheric entry: <b>%.2f x 10<sup>%.0f</sup> Joules</b> ", $energy0, $energy_power);
    }
    if ($megaton_power == 0) {
      if ($energy0_megatons < 1) {
	printf(" = <b>%.2f KiloTons TNT</b>", $energy0_megatons* 1000);
      } else {
	printf(" = <b>%.2f MegaTons TNT</b>", $energy0_megatons);
      }
    } else {
      printf (" = <b>%.2f x 10<sup>%.0f</sup> MegaTons TNT</b>", $energy0_megatons, $megaton_power);
    }

  }

### Subroutine to output the results of the energy calculation
sub print_recurrencetime
  {
    my $rec_time_p;

      ### Use scientific notation for recurrence times longer than 1000 years
      if ($rec_time > 1000) {
	$rec_time_p = log($rec_time)/log(10);
	$rec_time_p = int($rec_time_p);
	$rec_time /= 10**$rec_time_p;
	
	if ($rec_time * 10**$rec_time_p < 4.5e9) {
	  printf("<dd>The average interval between impacts of this size somewhere on Earth during the last 4 billion years is <b>%.1f x 10<sup>%.0f</sup>years</b>", $rec_time, $rec_time_p);
	} else {
	  print "<dd>The average interval between impacts of this size is longer than the Earth's age.";
	  print "<dd>Such impacts could only occur during the accumulation of the Earth, between 4.5 and 4 billion years ago.";
	}
	printf("</dl>\n");
	return;
      }
    
    ### Use normal notation for intervals less than 1000 years
    if ($rec_time * 12 < 1) {
      print"<dd>The average interval between impacts of this size somewhere on Earth is less than 1 month.";
    } else {
      printf("<dd>The average interval between impacts of this size somewhere on Earth is <b>%.1f years</b>", $rec_time);
    }
    printf("</dl>\n");
    
  }				### end of print_energy

sub print_change
  {

    print "<dl>\n<dt>\n<h2>Major Global Changes:</h2>\n";


    if ($vratio >= 0.1) {
      if ($vratio >= 0.5) {
	print "<dd>The Earth is completely disrupted by the impact and its debris forms a new asteroid belt orbiting the sun between Venus and Mars.</dl>";
	print_pdf();
	print footer();
      } else {
	print "<dd>The Earth is strongly disturbed by the impact, but loses little mass.";
      }
    } else {
      print "<dd>The Earth is not strongly disturbed by the impact and loses negligible mass.";
    }
	
    if ($mratio >= 0.01) {
      printf("<dd><b>%.2f</b> percent of the Earth is melted\n", $mratio * 100);
    }

    if ($lratio >= 0.001) {
      print "<dd>Depending on the direction and location the collision, ";
      if ($lratio < 0.01) {
	print "the impact may make a very small change in the tilt of Earth's axis (< half a degree).";
      } elsif ($lratio < 0.1) {
	print "the impact may make a noticeable change in the tilt of Earth's axis (< 5 degrees).";
      } elsif ($lratio < 1.0) {
	print "the impact may make a significant change in the tilt of Earth's axis.";
      } else {
	print "the impact may totally change the Earth's rotation period and the tilt of its axis.";
      }
    } else {
      print "<dd>The impact does not make a noticeable change in the tilt of Earth's axis (< 5 hundreths of a degree).";
    }

    ### Print the change in length of the day if more than one second
    if ($trot_change > 1.E-3) {

      my $Time;
      my $TimeUnit;

      FormatTime($trot_change,$Time,$TimeUnit);
      printf("<dd>Depending on the direction and location of impact, the collision may cause a change in the length of the day of up to <b>%g %s</b>.",$Time,$TimeUnit);

    }
	
    if ($pratio >= 0.001) {
      if ($pratio < .01) {
	print "<dd>The impact shifts the Earth's orbit noticeably.";
      } elsif ($pratio < 0.1) {
	print "<dd>The imapct shifts the Earth's orbit substantially.";
      } else {
	print "<dd>The impact shifts the Earth's orbit totally.";
      }
    } else {
      print "<dd>The impact does not shift the Earth's orbit noticeably.";
    }
	
	
    print "</dl>\n";
  }

sub print_atmospheric_entry
  {

    print "<dl>\n<dt>\n<h2>Atmospheric Entry:</h2>\n";

    my $en = 0.5 * $mass * (($vInput * 1000)**2 - ($velocity * 1000)**2);
    my $en_power;
    my $ens_power;
    my $en_mton;
    my $enmton_power;

    $en_mton = $en / (4.186 * 10**15); ### joules to megatons conversion

    $en_power = log($en)/log(10);
    $en_power = int($en_power);
    $en /= 10**$en_power;

    $ens_power = log($energy_surface)/log(10);
    $ens_power = int($ens_power);
    $energy_surface /= 10**$ens_power;

    $enmton_power = log($en_mton)/log(10);
    $enmton_power = int($enmton_power);
    $en_mton /= 10**$enmton_power;

    $megaton_power = log($energy_megatons)/log(10);
    $megaton_power = int($megaton_power);
    $energy_megatons /= 10**$megaton_power;
	

    if ($iFactor >= 1) {
      printf("<dd>The projectile lands intact, with a velocity <b>%g km/s = %g miles/s</b>.", FormatSigFigs($velocity, $sigfigs), FormatSigFigs($velocity * 0.621, $sigfigs));
      printf("<dd>The energy lost in the atmosphere is <b>%.2f x 10<sup>%.0f</sup> Joules = %.2f x 10<sup>%.0f</sup> MegaTons</b>.", $en, $en_power, $en_mton, $enmton_power);
    } else {
      printf("<dd>The projectile begins to breakup at an altitude of <b>%g meters = %g ft</b>", FormatSigFigs($altitudeBU, 3), FormatSigFigs($altitudeBU * 3.28,3));
      if ($altitudeBurst > 0) {
	printf("<dd>The projectile bursts into a cloud of fragments at an altitude of <b>%g meters = %g ft</b>", FormatSigFigs($altitudeBurst, $sigfigs), FormatSigFigs($altitudeBurst * 3.28, $sigfigs));
	printf("<dd>The residual velocity of the projectile fragments after the burst is <b>%g km/s = %g miles/s</b>", FormatSigFigs($velocity, $sigfigs), FormatSigFigs($velocity * 0.621, $sigfigs));
	printf("<dd>The energy of the airburst is <b>%.2f x 10<sup>%.0f</sup> Joules = %.2f x 10<sup>%.0f</sup> MegaTons</b>.", $en, $en_power, $en_mton, $enmton_power);
	if ($pdensity < 5000) {
	  print "<dd>No crater is formed, although large fragments may strike the surface.";
	} else {  
	  print "<dd>Large fragments strike the surface and may create a crater strewn field.  A more careful treatment of atmospheric entry is required to accurately estimate the size-frequency distribution of meteoroid fragments and predict the number and size of craters formed.";
	}

      } else {
	printf("<dd>The projectile reaches the ground in a broken condition.  The mass of projectile strikes the surface at velocity <b>%g km/s = %g miles/s</b>", FormatSigFigs($velocity, $sigfigs), FormatSigFigs($velocity * 0.621, $sigfigs));
        printf("<dd>The energy lost in the atmosphere is <b>%.2f x 10<sup>%.0f</sup> Joules = %.2f x 10<sup>%.0f</sup> MegaTons</b>.", $en, $en_power, $en_mton, $enmton_power);
	if ($megaton_power != 0) {
	  printf("<dd>The impact energy is <b>%.2f x 10<sup>%.0f</sup> Joules = %.2f x 10<sup>%.0f</sup>MegaTons</b>.", $energy_surface, $ens_power, $energy_megatons, $megaton_power);
	} else {
	  printf("<dd>The impact energy is <b>%.2f x 10<sup>%.0f</sup> Joules = %.2f MegaTons</b>.", $energy_surface, $ens_power, $energy_megatons);
	}
        print "<dd>The larger of these two energies is used to calculate the airblast damage.";
	printf("<dd>The broken projectile fragments strike the ground in an ellipse of dimension <b>%g km by %g km</b>", FormatSigFigs($dispersion/(1000 * sin($theta * $pi /180)), $sigfigs), FormatSigFigs($dispersion / 1000, $sigfigs));
      }
    }

    $energy_surface *= 10**$ens_power;
    $energy_megatons *= 10**$megaton_power;
    print "</dl>";
  }

sub print_pdf
{


print <<EOF;
	<br>
	<br>
	
	<a target="_blank" href="../ImpactEffects/effects.pdf">Tell me more...</a>
	<p>Click here for a pdf document that details the observations, assumptions, and equations upon which this program is based.  It
	describes our approach to quantifying the important impact processes that might affect the people, buildings, and landscape in the
	vicinity of an impact event and discusses the uncertainty in our predictions.  The processes included are:  atmospheric entry, impact
	crater formation, fireball expansion and thermal radiation, ejecta deposition, seismic shaking, and the propagation of the atmospheric
	blast wave.</p>

        <p>Recent improvements in the airblast calculation are described <a target="_blank" href="http://dx.doi.org/10.1111/maps.12873">here</a>.</p>

	<br>

EOF

    ### Disclaimer and footer
    print "<br><br><hr><br>";
    print "<font size=1>";
    print "Earth Impact Effects Program Copyright 2004, Robert Marcus, H.J. Melosh, and G.S. Collins<br>";
    print "These results come with ABSOLUTELY NO WARRANTY";
    print "</font>";
    print "</body>\n</html>\n";
    #print_footer();

}

