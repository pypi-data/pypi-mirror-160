#!/usr/bin/perl -w

use strict;

use lib "../cgi-bin";

use CGI qw(:standard);
use List::Util qw[min max];
use Math::Trig;
use Math::SigFigs;

# copyright 2004, Robert Marcus, H.J. Melosh, and Gareth Collins

#my $output;

my $sigfigs = 3;			# number of sig figs to print
my $pdiameter;                          # Impactor diameter (m)
my $pdensity;                           # Impactor density (kg/m^3)
my $vInput;				# input velocity (km/s) before entry
my $velocity;				# velocity at target surface km/s
my $theta;
my $tdensity;
my $ttype;
my $distance;				# distance in km
my $depth;				# water depth in meters

my $mwater;				# mass of water
my $vseafloor;				# velocity of projectile at seafloor
my $energy0;				# input energy before atmospheric entry
my $energy_power;
my $energy0_megatons;
my $megaton_power;
my $energy_atmosphere;                  # energy deposited in the atmosphere
my $energy_blast;                       # energy used for airblast calculation (ktons)
my $energy_surface;			# energy at surface
my $energy_megatons;			# energy at suface in MT
my $energy_seafloor;			# energy at seafloor (bottom of water layer)
my $rec_time;                           # Reccurence interval (years)
my $iFactor;				# intact factor >= 1, projectile lands intact
my $altitudeBU;				# altitude of projectile breakup in meters
my $altitudeBurst;			# altitude at which projectile bursts in meters
my $dispersion;				# dispersion of pancake upon impact, 2 * semimajor axis of pancaked impactor
my $delta;				# angle of the distance entered, measured from center of the earth
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
my $lratio;			        # ratio of proj ang. momen, to $lEarth	
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
my @valid = qw(1 1 1 1 1 1 1 1);

&get_data();
&check_data();
if($valid_data == 0){
	&reprint_form();
}else{
	&impact_effects();
}

# dist=75
# diam=111
# pdens=111
# pdens_select=0
# vel=111
# theta=45
# tdens=2750
# tdens_select=0

# dist=75 distanceUnits=1 
# diam=111 diameterUnits=1 
# pdens=111 pdens_select=3000 
# vel=111 velocityUnits=1 theta=111
# wdepth= wdepthUnits=1 tdens=2750

sub get_data
{

	$pdiameter = param("diam");
	$pdensity = param('pdens');

  if($pdensity eq ''){
      $pdensity = param('pdens_select');  
  }

  $vInput = param('vel');
  
  my $vUnits;
  $vUnits = param('velocityUnits');
  if($vUnits == 2){
    $vInput *= 1.61;
  }

  $theta = param('theta');
  $tdensity = param('tdens');
  if($tdensity == 1000){
    $depth = param('wdepth');
	}else{
		$depth = 0;
	}
    	
  my $depthUnits;
  $depthUnits = param('wdepthUnits');
  if($depthUnits == 2){
    $depth *= 0.3048;
  }
  
	$ttype = 3;
	    	
  $distance = param('dist');

	my $dunits;
	$dunits = param('distanceUnits');
	if($dunits == 2){
		$distance *= 1.61;
	}

	my $punits;	
	$punits = param('diameterUnits');
	if($punits == 2){
		$pdiameter *= 1000;
	}elsif($punits == 3){
		$pdiameter *= 0.3048;
	}elsif($punits == 4){
		$pdiameter *= 1609.34;
	}

	my $vunits;
	$vunits = param('velocityUnits');
	if($vunits == 2){
		$velocity *= 1.61;
	}
}


sub check_data
{
	
	if(!($energy0 =~ /^[0-9]+\.?[0-9]*e?[0-9]*$/)){
		$valid[7] = 0;
	}
	if($pdiameter == 0 or !($pdiameter =~ /^[0-9]*\.?[0-9]*$/)){
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
	if($distance == 0 or !($distance =~ /^[0-9]*\.?[0-9]*$/) or $distance > (3.14159 * $R_earth)){
		$valid_data = 0;
		$valid[6] = 0;
	}
	


}


sub impact_effects
  ### The main sub program
  ### pre:  All necessary parameters are valid, results calculated
  ### post: Displays the results to the user
  {

    ### Print the title and header; echo the users inputs
    print header();
    print_title();
    echo_inputs();

    ### Check that the impact energy is sensible, compute
    ### the global effects, recurrence interval and atmospheric entry
    if ($valid[7] == 0) {
      &calc_energy();
    }

    ### Print the impact energy, recurrence interval
    print_energy();
    print_recurrencetime();

    ### Compute the crater size
    &find_crater();

    ### Print global effects
    print_change();

    ### Print the effects of atmospheric entry for impactors
    ### less than approx. 1-km diameter (for projectile density of 3000 kg/m3)
    ### Actually use mass threshold to allow for density effect.
    #if ($pdiameter <= 1000) {
    if ($mass <= 1.5707963E12) {
      print_atmospheric_entry();
    }

    ### If the impactor does not airburst, compute:
    ### Ejecta, thermal radiation, earthquake
    if ($altitudeBurst <= 0) {
      #&find_crater();

      ### Calculate the ejecta thickness, particle size and arrival time
      &find_ejecta();

      ### For high-velocity impacts, calculate the fireball size, thermal radiation
      if ($velocity >= 15) {
	      &find_thermal();
      }

      ### Calculate the earthquake magnitude and damage
      &find_magnitude();
      &find_intensity();

      ### Print results (only print ejecta if inside the crater)
      print_crater();
      if ($distance * 1000 <= $Dtr/2) {
        print_ejecta();
        return;
      }		
      print_thermal();
      print_seismic();
      print_ejecta();
    }	

    ### Compute the effects of the airblast and print
    &air_blast();	
    print_airblast();

    ### Compute the tsunami amplitude if water layer present
    if ($depth > 0.) {
      &tsunami();
      print_tsunami();
    }

    ### Include a link to the documentation
    print_pdf();

  }  ### End of main program impact_effects

### Subroutine for computing impact energy (before and after atmospheric entry, and after ocean traverse).
### Atmospheric entry calculation is called from in here
### Also compute reccurence time interval (years)
sub calc_energy {

    ### mass = density * volume, volume calculated assuming the projectile to be approximately spherical
    ### V = 4/3pi(r^3) = 1/6pi(d^3)
    $mass = (($pi * $pdiameter**3)/6)*$pdensity;
    $energy0 = 0.5 * $mass * ($vInput * 1000)**2;
    $energy0_megatons = $energy0 / (4.186 * 10**15); ### joules to megatons conversion

    ### Compute the recurrence interval for this energy impact
    ### Old model
    #$rec_time = 110 * ($energy0_megatons)**0.77;
    ### New model (after Bland and Artemieva (2006) MAPS 41 (607-621).
    if ($mass < 3) {
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
    if ($mass < 1) {
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
	
    ### Compute the epicentral angle for use in several subsequent calculations.
    $delta = (180 / $pi) * ($distance/$R_earth);

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

sub find_magnitude
### post:  returns the richter magnitude of the seismic disturbance caused by impact
{
  my $Ax;         # factor for determining "effective magnitude" at given distance
	
  $magnitude = 0.67 * ((log ($energy_seafloor))/(log 10)) - 5.87;
  
  if($distance >= 700){
    
    $Ax = 20 * 10**($magnitude - 1.66 * (log ($delta) / log (10)) - 3.3);
    $Ax /= 1000;
    
  }elsif($distance >= 60){
    
    $Ax = 10**($magnitude - (0.0048*$distance + 2.5644));
    
  }else{
    
    $Ax = 10**($magnitude - (0.00238*$distance + 1.3342));
    
  }
  
  $eff_mag = (log ($Ax) / log (10)) + 1.4;
  $seismic_arrival = $distance / $surface_wave_v;
  
}  ### End of sub find_magnitude


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
      
      $tdensity = 2700;	# change target density for seafloor crater calculation // TODO:注意变换
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
    
  }  ### End of sub find_crater


sub find_intensity
{

  open (FILE, "./mercalli.txt");        
  @input = <FILE>;
  
  if($eff_mag >= 9){ 
    $des = "<br><ul>";
    $des .= $input[9] . "<br><br>";
    $des .= $input[10] . "<br><br>";
    $des .= $input[11];
  }elsif($eff_mag >= 8){
    $des = "<br><ul>" . $input[9] . "<br><br>" . $input[10]; 
  }elsif($eff_mag >= 7){
    $des = "<br><ul>" . $input[8];
    $des .= "<br><br>";
    $des .= $input[9];
  }elsif($eff_mag >= 6){
    $des = "<br><ul>" . $input[6];
    $des .= "<br><br>";
    $des .= $input[7];
  }elsif($eff_mag >= 5){
    $des = "<br><ul>" . $input[5];
    $des .= "<br><br>";
    $des .= $input[6];
  }elsif($eff_mag >= 4){
    $des = "<br><ul>" . $input[3];
    $des .= "<br><br>";
    $des .= $input[4]; 
  }elsif($eff_mag >= 3){
    $des = "<br><ul>" . $input[2];
    $des .= "<br><br>";
    $des .= $input[3]; 
  }elsif($eff_mag >= 2){
    $des = "<br><ul>" . $input[0];
    $des .= "<br><br>";
    $des .= $input[1];
  }else{
    $des = "<br><ul>Nothing would be felt.  However, seismic equipment may still detect the shaking.";
  }
  
  
  
  close FILE;
}                ### end of sub find intensity


sub find_ejecta
  {
    
    my $phi = ($distance) / (2 * $R_earth);
    my $X = (2 * tan($phi)) / (1 + tan($phi));
    my $e = -(0.5 * ($X - 1)**2 + 0.5)**0.5; # eccentricity of eliptical path of the ejecta
    my $a = ($X * $R_earth * 1000) / (2 * (1 - $e**2));	# semi major axis of elliptical path
    
    my $part1 = $a**1.5 / ($g * ($R_earth * 1000)**2)**0.5;
    my $term1 = 2* atan(((1 - $e)/(1 + $e))**0.5 * tan ($phi / 2));
    my $term2 = $e * (1 - $e**2)**0.5 * sin ($phi)/ (1 + $e * cos($phi));
    $ejecta_arrival = 2 * $part1 * ($term1 - $term2);
    
    $ejecta_thickness = $Dtr**4/(112 * ($distance * 1000)**3);
    
    ### compute mean fragment size
    my $a2 = 2.65;
    my $half_diameter = ($cdiameter/1000)/2;  # half of final crater diameter in km
    my $dc = 2400* $half_diameter**-1.62;
    
    $d_frag = $dc*($half_diameter/$distance)**$a2;
    
  }  ### end of sub find_ejecta


sub air_blast
  {

    my $vsound = 330;		# speed of sound in m/s
    my $r_cross;		# radius at which relationship between overpressure and distance changes
    my $r_cross0 = 290;		# radius at which relationship between overpressure and distance changes (for surface burst)
    my $op_cross = 75000;	# overpressure at crossover
    my $energy_ktons;		# energy in kilotons
    my $d_scale;		# distance scaled for 1 kTon blast
    my $slantRange;		# in km
    my $d_smooth;
    my $p_machT;
    my $p_0;
    my $expFactor;
    my $p_regT;
  
    #$energy_ktons = 1000 * $energy_megatons;
    $energy_ktons = $energy_blast;

    ### Arrival time is straight line distance divided by sound speed
    $slantRange = ($distance**2 + ($altitudeBurst/1000)**2)**(1/2); # for air burst, distance is slant range from explosion
    $shock_arrival = ($slantRange * 1000)/$vsound; # distance in meters divided by velocity of sound in m/s
  
    ### Scale distance to equivalent for a kiloton explosion
    $sf = ($energy_ktons)**(1/3);
    $d_scale = ($distance * 1000) / $sf;
  
    ### Scale burst altitude to equivalent for a kiloton explosion
    my $z_scale = $altitudeBurst / $sf;
    $r_cross = $r_cross0 + 0.65 * $z_scale;
    my $r_mach = 550 * $z_scale /(1.2 * (550 - $z_scale));
    if ($z_scale >= 550) {
      $r_mach = 1e30;
    }
  
    if ($altitudeBurst > 0) {
      $d_smooth = $z_scale**2 * 0.00328;
      $p_machT = (($r_cross * $op_cross) / 4) * (1 / ($r_mach + $d_smooth)) * (1 + 3*($r_cross / ($r_mach + $d_smooth))**(1.3));
      #$p_0 = 3.1423e11 / $z_scale**2.6;
      #$expFactor = - 34.87 / $z_scale**1.73;
      #$p_regT = $p_0 * exp($expFactor * ($r_mach - $d_smooth));
      $p_regT = 3.14e11 * ( ($r_mach - $d_smooth )**2 + $z_scale **2) **(-1.3) + 1.8e7 * ( ($r_mach - $d_smooth )**2 + $z_scale **2) **(-0.565)
    } else {
      $d_smooth = 0;
      $p_machT = 0;
    }
  
    if ($d_scale >= ($r_mach + $d_smooth)) {
      $opressure = (($r_cross * $op_cross) / 4) * (1 / $d_scale) * (1 + 3*($r_cross / $d_scale)**(1.3));
    } elsif ($d_scale <= ($r_mach - $d_smooth)) {
      #$opressure = $p_0 * exp($expFactor * $d_scale);
      $opressure = 3.14e11 * ($d_scale **2 + $z_scale **2) **(-1.3) + 1.8e7 * ($d_scale **2 + $z_scale **2) **(-0.565)
    } else {
      $opressure = $p_regT - ($d_scale - $r_mach + $d_smooth) * 0.5 * ($p_regT - $p_machT)/$d_smooth;
    }
  
    ### Wind velocity
    $vmax = ((5 * $opressure) / (7 * $Po)) * ($vsound / (1 + (6 * $opressure) / (7 * $Po))**(1/2));
  
    ### damage descriptions:  structures
    if ($opressure >= 42600) {
      $shock_damage .= "<br>Multistory wall-bearing buildings will collapse.<br>\n";
    } elsif ($opressure >= 38500) {
      $shock_damage .= "<br> Multistory wall-bearing buildings will experience severe cracking and interior partitions will be blown down<br>\n";
    }
    if ($opressure >= 26800) {
      $shock_damage .= "<br> Wood frame buildings will almost completely collapse.<br>\n";
    } elsif ($opressure >= 22900) {
      $shock_damage .= "<br> Interior partitions of wood frame buildings will be blown down.  Roof will be severely damaged.<br>\n";
    }
    if ($opressure >= 273000) {
      $shock_damage .= "<br> Multistory steel-framed office-type buildings will suffer extreme frame distortion, incipient collapse.<br>\n";
    }
    if ($opressure >= 121000) {
      $shock_damage .= "<br> Highway truss bridges will collapse.<br>\n";
    } elsif ($opressure >= 100000) {
      $shock_damage .= "<br> Highway truss bridges will suffer substantial distortion of bracing.<br>\n";
    }
    if ($opressure >= 379000) {
      $shock_damage .= "<br> Highway girder bridges will collapse.<br>\n";
    }
  
    ### damage descriptions:  glass, transportation, forrests
    if ($opressure >= 6900) {
      $shock_damage .= "<br> Glass windows will shatter.<br>\n";
    } elsif ($opressure >= 690) {
      $shock_damage .= "<br> Glass windows may shatter.<br>\n";
    }
    if ($opressure >= 426000) {
      $shock_damage .= "<br> Cars and trucks will be largely displaced and grossly distorted and will require rebuilding before use.<br>\n";
    } elsif ($opressure >= 297000) {
      $shock_damage .= "<br> Cars and trucks will be overturned and displaced, requiring major repairs.<br>\n";
    }
    if ($vmax >= 62) {
      $shock_damage .= "<br> Up to 90 percent of trees blown down; remainder stripped of branches and leaves.<br>\n";
    } elsif ($vmax >= 40) {
      $shock_damage .= "<br> About 30 percent of trees blown down; remainder have some branches and leaves blown off.<br>\n";
    }
  
    ### sound intensity
    if ($opressure > 0) {
      $dec_level = 20 * (log ($opressure) / log (10));
    } else {
      $dec_level = 0;
    }
  
  }  ### end of sub shock_wave

sub find_thermal
  {

    my $eta = 3 * 10**-3;	                ## factor for scaling thermal energy
    my $T_star = 3000;		                ## temperature of fireball
    $Rf = 2* 10**-6* ($energy_surface)**(1/3);  ## Rf is in km
    my $sigma = 5.67 * 10**-8;	                ## Stephan-Boltzmann constant
  
    $thermal_exposure = ($eta * $energy_surface)/(2 * $pi * ($distance* 1000)**2);
  
    $h = (1 - cos($delta * $pi/180))* $R_earth; ## h is in km, $R_earth is in km	
    my $del = acos($h / $Rf);
    my $f = (2/$pi)*($del - ($h/$Rf)*sin($del));
  
    if ($h > $Rf) {
      $no_radiation = 1;
      return;
    }
  
    $no_radiation = 0;
    $thermal_exposure *= $f;
  
    $max_rad_time = $Rf / $velocity;           ## Rf in km / velocity in km/s
    $irradiation_time = ($eta * $energy_surface)/(2 * $pi * ($Rf*1000)**2 * $sigma * $T_star**4);
  
    my $megaton_factor = ($energy_megatons)**(1/6);
  
    if ($thermal_exposure > (10**6 * $megaton_factor)) {
      $thermal_des .= "<br>Clothing ignites<br>\n";
    }
    if ($thermal_exposure > (4.2 * 10**5 * $megaton_factor)) {
      $thermal_des .= "<br>Much of the body suffers third degree burns<br>\n";
    } elsif ($thermal_exposure > (2.5 * 10**5 * $megaton_factor)) {
      $thermal_des .= "<br>Much of the body suffers second degree burns<br>\n";
    } elsif ($thermal_exposure > (1.3 * 10**5 * $megaton_factor)) {
      $thermal_des .= "<br>Much of the body suffers first degree burns<br>\n";
    }
    if ($thermal_exposure > (3.3 * 10**5 * $megaton_factor)) {
      $thermal_des .= "<br>Newspaper ignites<br>\n";
    }
    if ($thermal_exposure > (6.7 * 10**5 * $megaton_factor)) {
      $thermal_des .= "<br>Plywood flames<br>\n";
    }
    if ($thermal_exposure > (2.5 * 10**5 * $megaton_factor)) {
      $thermal_des .= "<br>Deciduous trees ignite<br>\n";
    }
    if ($thermal_exposure > (3.8 * 10**5 * $megaton_factor)) {
      $thermal_des .= "<br>Grass ignites<br>\n";
    }

    $thermal_power = log($thermal_exposure)/log(10);
    $thermal_power = int($thermal_power);
    $thermal_exposure /= 10**$thermal_power;

  }

### Subroutine to compute tsunami wave amplitude and arrival time
sub tsunami
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
    my $TsunamiSpeed;                 # Tsunami speed in m/s
    my $TsunamiWavelength;            # Tsunami wavelength in m

    ### Define parameters
    $shallowness = $pdiameter/$depth;
    $RimWaveExponent = 1.;
    $MaxWaveRadius = 0.001*$wdiameter;
    $MinWaveRadius = 0.0005*$wdiameter;

    ### Tsunami arrival time assumes linear wave theory
    $TsunamiWavelength = 2.*$wdiameter;
    $TsunamiSpeed = sqrt(0.5*$g*$TsunamiWavelength/$pi*tanh(2.*$pi*$depth/$TsunamiWavelength));
    $TsunamiArrivalTime = $distance*1000/$TsunamiSpeed;

    ### Rim wave upper and lower limit estimates
    $MaxWaveAmplitude = min(0.07*$wdiameter,$depth);
    $WaveAmplitudeUpperLimit = $MaxWaveAmplitude*($MaxWaveRadius/$distance)**$RimWaveExponent;
    $WaveAmplitudeLowerLimit = $MaxWaveAmplitude*($MinWaveRadius/$distance)**$RimWaveExponent;

    ### Collapse wave correction to lower limit for deep-water impacts
    if ($shallowness < 0.5) {
      $CollapseWaveExponent = 3.*exp(-0.8*$shallowness);
      $CollapseWaveRadius = 0.0025*$wdiameter;
      $MaxCollapseWaveAmplitude = 0.06*min($wdiameter/2.828,$depth);
      $CollapseWaveAmplitude = $MaxCollapseWaveAmplitude*($CollapseWaveRadius/$distance)**$CollapseWaveExponent;
      $WaveAmplitudeLowerLimit = min($CollapseWaveAmplitude,$WaveAmplitudeLowerLimit);
    }

    ### DEBUGGING INFO:
#    print"<dl>\n<dt>\n<h2>Tsunami Debugging:</h2>\n";
#    printf("<dd>Impact shallowness (L/H): %.2f \n", $shallowness);
#    printf("<dd>Tsunami wavelength: %.2f m \n", $TsunamiWavelength);
#    printf("<dd>Tsunami speed: %.2f m/s \n", $TsunamiSpeed);
#    printf("<dd>Max amplitude: %.2f m \n", $MaxWaveAmplitude);
#    printf("<dd>Max wave radius: %.2f km \n", $MaxWaveRadius);
#    printf("<dd>Min wave radius: %.2f km \n", $MinWaveRadius);
#    print"</dl>\n<br>";

  }

sub print_tsunami
  {
    my $FormattedTime=0.;
    my $TimeUnit="non";
    my $FormattedAmplitudeMet_L;
    my $MetUnit_L;
    my $FormattedAmplitudeImp_L;
    my $ImpUnit_L;
    my $FormattedAmplitudeMet_U;
    my $MetUnit_U;
    my $FormattedAmplitudeImp_U;
    my $ImpUnit_U;

    ### Print the tsunami results
    print "<dl>\n<dt>\n<h2>Tsunami Wave:</h2>\n";

    print <<EOF;
	<dd><a target="blank" href="../ImpactEffects/craterexp.html#tsunami">What does this mean?</a><br><br>
EOF

    ### If inside the water crater say this and finish.
    if ($distance*1000 < $wdiameter) {
      printf("<dd>Your location is within the crater formed in the water layer. This is where the impact tsunami wave is generated. \n");
      print"</dl>\n<br>";
      return;
    }

    ### Report the approximate arrival time of the tsunami
    FormatTime($TsunamiArrivalTime,$FormattedTime,$TimeUnit);
    printf("<dd>The impact-generated tsunami wave arrives approximately <b>%.1f %s</b> after impact. \n", $FormattedTime, $TimeUnit);
    print"<br><br>";

    ### Report the two wave amplitude limits if more than 10 cm
    FormatDistance($WaveAmplitudeLowerLimit,$FormattedAmplitudeMet_L,$MetUnit_L,$FormattedAmplitudeImp_L,$ImpUnit_L);
    FormatDistance($WaveAmplitudeUpperLimit,$FormattedAmplitudeMet_U,$MetUnit_U,$FormattedAmplitudeImp_U,$ImpUnit_U);
    if ($WaveAmplitudeLowerLimit > 0.1) {
      printf("<dd>Tsunami wave amplitude is between:  <b>%.1f %s</b> ( = <b>%.1f %s</b>) and <b>%.1f %s</b> ( = <b>%.1f %s</b>). \n", $FormattedAmplitudeMet_L, $MetUnit_L, $FormattedAmplitudeImp_L, $ImpUnit_L, $FormattedAmplitudeMet_U, $MetUnit_U, $FormattedAmplitudeImp_U, $ImpUnit_U);
    } elsif ($WaveAmplitudeUpperLimit < 0.1) {
      printf("<dd>Tsunami wave amplitude is less than <b>10 cm</b> at your location. \n");
    } else {
      printf("<dd>Tsunami wave amplitude is less than <b>%.1f %s</b> ( = <b>%.1f %s</b>). \n", $FormattedAmplitudeMet_U, $MetUnit_U,  $FormattedAmplitudeImp_U, $ImpUnit_U);
    }

    print"</dl>\n<br>";

  }

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
    FormatDistance($distance*1000,$FormattedDistanceMet,$MetUnit,$FormattedDistanceImp,$ImpUnit);
    printf("<dd>Distance from Impact:  <b>%.2f %s ( = %.2f %s )</b> \n", $FormattedDistanceMet, $MetUnit, $FormattedDistanceImp, $ImpUnit);
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
      printf("<dd>Melt volume = <b>%g</b> times the crater volume\n", FormatSigFigs($mcratio, $sigfigs));
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


sub print_thermal
  {
    my $DistMet;
    my $UnitMet;
    my $DistImp;
    my $UnitImp;
    my $Time;
    my $TimeUnit;

    print "<dl>\n<dt>\n<h2>Thermal Radiation:</h2>\n";
  
    print <<EOF;
        <dd><a target="blank" href="../ImpactEffects/craterexp.html#thermal">What does this mean?</a><br><br><br>
EOF
  
    ### No fireball at low velocity
    if ($velocity < 15) {
      print "<dd>At this impact velocity ( < 15 km/s), little vaporization occurs; no fireball is created, therefore, there is no thermal radiation damage.";
      print "</dl>";
      return;
    }
  
    ### Is fireball above the horizon?
    if ($no_radiation == 1) {
      printf("<dd>The fireball is below the horizon.  There is no direct thermal radiation.\n</dl>\n");
      return;
    }
  
    ### Time of maximum radiation
    FormatTime($max_rad_time,$Time,$TimeUnit);
    printf("<dd>Time for maximum radiation:  <b>%g %s </b> after impact", $Time,$TimeUnit);
    printf("<dd><br>  ");
  
    ### Size of the fireball
    if ($distance < $Rf) {
      printf("<dd>Your position is inside the fireball.");
    } else {
      FormatDistance(($Rf-$h)*1000.,$DistMet,$UnitMet,$DistImp,$UnitImp);
      printf("<dd>Visible fireball radius:  <b>%g %s ( = %g %s ) </b>",$DistMet,$UnitMet,$DistImp,$UnitImp);
    }
    
    ### Brightness of the fireball relative to the sun
    my $B;
    $B = ($Rf - $h)/(4.4* 10**-3 * $distance);
    if ($B >= 0.1) {
      printf("<dd>The fireball appears <b>%g</b> times larger than the sun", FormatSigFigs($B, $sigfigs));
    }
  
    ### Thermal exposure
    if ($thermal_power == 0) {
      printf("<dd>Thermal Exposure:  <b>%.2f Joules/m<sup2</sup></b>", FormatSigFigs($thermal_exposure, $sigfigs));
    } else {
      printf("<dd>Thermal Exposure:  <b>%.2f x 10<sup>%.0f</sup> Joules/m<sup>2</sup></b>", $thermal_exposure, $thermal_power);
    }

    ### Duration of irradiation
    FormatTime($irradiation_time,$Time,$TimeUnit);
    printf("<dd>Duration of Irradiation:  <b>%g %s</b>",$Time,$TimeUnit);
    
    ### Radiant flux relative to solar flux
    my $flux;			
    $flux = ($thermal_exposure * 10**$thermal_power) / ($irradiation_time * 1000);
    printf("<dd>Radiant flux (relative to the sun):  <b>%g</b>", FormatSigFigs($flux, $sigfigs));
    if ($flux >= 15 and $flux <= 25) {
      printf(" (Flux from a burner on full at a distance of 10 cm)");
    }
  
    ### Thermal radiation damage
    printf("<dd><br>");
    if ($thermal_des ne "") {
      printf("<dd>Effects of Thermal Radiation:<br>\n");
      print "<ul> $thermal_des</ul>";
    }
    print "</dl><br>";
  
  }				### end of print_thermal


sub print_seismic
  {
    my $Time;
    my $TimeUnit;

    ### seismic results

    print "<dl>\n<dt>\n<h2>Seismic Effects:</h2>\n";
    print <<EOF;
        <dd><a target="blank" href="../ImpactEffects/craterexp.html#seismic">What does this mean?</a><br><br><br>
EOF

    ### Don' print results if magnitude very small
    if ($magnitude < 0) {
      print "<dd>The Richter Scale Magnitude for this impact is less than zero; no seismic shaking will be felt.";
      print "</dl>";
      return;
    }

    ### Arrival time
    if ($seismic_arrival < 0.1) {
      printf("The major seismic shaking will arrive almost instantly.");
    } else {
      FormatTime($seismic_arrival,$Time,$TimeUnit);
      printf ("The major seismic shaking will arrive approximately <b>%g %s</b> after impact.",$Time,$TimeUnit);
    }

    ### Richter Scale Magnitude
    printf ("<dd>Richter Scale Magnitude:  <b>%.1f</b>", $magnitude);
    if ($magnitude >= 9.5) {
      printf(" <b>(This is greater than any earthquake in recorded history)</b>");
    }

    ### Earthquake damage
    print "<dd>Mercalli Scale Intensity at a distance of $distance km: \n<br>\n";
    print $des;
    print "</dl>\n";
    print "<br>\n";


  } ### end of print seismic


sub print_ejecta
  {
    my $DistMet;
    my $UnitMet;
    my $DistImp;
    my $UnitImp;
    my $Time;
    my $TimeUnit;

    ### ejecta results
    print "<dl>\n<dt>\n<h2>Ejecta:</h2>";
    print <<EOF;
        <dd><a target="blank" href="../ImpactEffects/craterexp.html#ejecta">What does this mean?</a><br><br><br>
EOF

    ### Ejecta from small impacts is blocked by the atmosphere
    if (($energy_megatons * 10**$megaton_power) < 200 and ($distance > $Rf)) {
      print "<dd>Most ejecta is blocked by Earth's atmosphere";
      print "</dl><br>";
      return;
    }

    ### Ejecta comes from transient crater
    if ($distance * 1000 <= $Dtr/2) {
      print "<dd>Your position was inside the transient crater and ejected upon impact";
      print "</dl><br>";
      return;
    }
	
    ### Inside final crater
    if ($distance * 1000 > $Dtr/2 and $distance * 1000 < $cdiameter/2) {
      print "<dd>Your position is in the region which collapses into the final crater.";
      print "</dl><br>";
      return;
    }

    ### Arrival time greater than 1 hour or almost no ejecta
    if ($ejecta_arrival >= 3600) { 
      print "<dd>Little rocky ejecta reaches this site; fallout is dominated by condensed vapor from the projectile.";
      print "</dl><br>";
      return;
    } elsif ($ejecta_thickness * 10**6 < 1) {
      print "<dd>Almost no solid ejecta reaches this site.";
      print "</dl><br>";
      return;
    }

    ### Ejecta arrival time
    FormatTime($ejecta_arrival,$Time,$TimeUnit);
    printf ("The ejecta will arrive approximately <b>%g %s </b> after the impact.",$Time,$TimeUnit);

    ### Type of ejecta deposit
    if ($distance * 1000 <= 3 * $cdiameter/2) {
      print "<dd>Your position is beneath the continuous ejecta deposit.";
    } else {
      print "<dd>At your position there is a fine dusting of ejecta with occasional larger fragments";
    }

    ### Ejecta thickness
    FormatDistance($ejecta_thickness,$DistMet,$UnitMet,$DistImp,$UnitImp);
    printf("<dd>Average Ejecta Thickness:  <b>%g %s ( = %g %s ) </b>\n", $DistMet,$UnitMet,$DistImp,$UnitImp);

    ### Fragment size
    FormatDistance($d_frag,$DistMet,$UnitMet,$DistImp,$UnitImp);
    printf("<dd>Mean Fragment Diameter:  <b>%g %s ( = %g %s ) </b>\n",$DistMet,$UnitMet,$DistImp,$UnitImp);

    print "</dl>\n";
    print "<br>\n";
        
 
  } ### end of print_ejecta


sub print_airblast
  {
    my $Time;
    my $TimeUnit;

    ### air blast results 
    my $bars;			# overpressure in bars
    my $mph;			# max wind velocity in mph

    $bars = $opressure / 10**5;
    $mph = $vmax * 2.23694;

    print "<dl>\n<dt>\n<h2>Air Blast:</h2>";

    print <<EOF;
        <dd><a href="../ImpactEffects/craterexp.html#airblast">What does this mean?</a><br><br><br>
EOF

    ### Exit if airblast has no effect
    if ($opressure < 1) {
      print "<dd>The air blast at this location would not be noticed. (The overpressure is less than 1 Pa)";
      print "</dl>";
      return;
    }

    ### Blast wave arrival time
    FormatTime($shock_arrival,$Time,$TimeUnit);
    printf("The air blast will arrive approximately <b>%g %s</b> after impact.",$Time,$TimeUnit);

    ### Overpressure
    if ($distance*1000. < 3*$altitudeBurst) {
      printf("<dd>Peak Overpressure:  <b>%g - %g Pa = %g - %g bars = %g - %g psi</b>", FormatSigFigs($opressure, $sigfigs), FormatSigFigs(2*$opressure, $sigfigs), FormatSigFigs($bars, $sigfigs), FormatSigFigs(2*$bars, $sigfigs), FormatSigFigs($bars * 14.2, $sigfigs), FormatSigFigs(2*$bars * 14.2, $sigfigs) );
    } else {
      printf("<dd>Peak Overpressure:  <b>%g Pa = %g bars = %g psi</b>", FormatSigFigs($opressure, $sigfigs), FormatSigFigs($bars, $sigfigs), FormatSigFigs($bars * 14.2, $sigfigs));
    }

    ### Wind velocity
    printf("<dd>Max wind velocity:  <b>%g m/s = %g mph</b>", FormatSigFigs($vmax, $sigfigs), FormatSigFigs($mph, $sigfigs));

    ### Sound intensity
    if ($dec_level > 0) {
      printf("<dd>Sound Intensity:  <b>%.0f dB</b>", $dec_level);
      if ($dec_level <= 20) {
	print " <b>(Barely Audible)</b>";
      } elsif ($dec_level <= 50) {
	print " <b>(Easily Heard)</b>";
      } elsif ($dec_level <= 90) {
	print " <b>(Loud as heavy traffic)</b>";
      } elsif ($dec_level <= 120) {
	print " <b>(May cause ear pain)</b>";
      } else {
	print " <b>(Dangerously Loud)</b>";
      }
    } else {
      print "<dd>The blast wave will not be heard.";
    }

    ### Airblast damage
    if ($shock_damage ne "") {
      print "<dd>Damage Description:<br>\n";
    }
    print "<ul>$shock_damage</ul>";
    print "</dl>\n";

  } ### end of print_airblast

sub print_noimpact
  {

    print "<p>This projectile is so small that it burns up during atmospheric traverse.</p>";
    print "<p>The energy shown below is deposited in the atmosphere.";
    print_energy();
    print_recurrencetime();
    print_pdf();

  } ### end of sub print_noimpact


sub print_title
  {

    print <<EOF;

	<html>
	<head>
        <title>Calculated Results</title>
        <link rel="stylesheet" href="../ImpactEarth.css">
        </head>
 <!body style="font-family:calibri" text="#FFFFFF" bgcolor="#000000" link="#FFFFFF" vlink="#FFFFFF" alink="#FF0000">
 <body>

<table COLS=2 WIDTH=100%>
<tr>
<td><img class="banner_image" SRC="../imperial.png" BORDER=5></td>
<td><img class="banner_image" align=right SRC="../purduemark.png" BORDER=5></td>
</tr>
</table>
<h1 align=center><a href="../index.html">Earth Impact Effects Program</a></h1>
<h3 align=center><a href="http://www.cfa.harvard.edu/~rmarcus/index.html">Robert Marcus</a>, <a href="http://www.purdue.edu/eas/people/faculty/melosh.html">H. Jay Melosh</a>, and <a href="http://www.imperial.ac.uk/people/g.collins">Gareth Collins</a></h3>
	<p>Please note:  the results below are estimates based on current (limited) understanding of the impact process and come with large uncertainties;  they should be used with caution, particularly in the case of peculiar input parameters.  All values are given to three significant figures but this does not reflect the precision of the estimate.  For more information about the uncertainty associated with our calculations and a full discussion of this program, please refer to this <a href="../ImpactEffects/effects.pdf">article</a></p> 

EOF

  }

sub reprint_form
  {

    print header();

    print <<EOF;
<head>
<title>Earth Impact Effects Program</title>
<link rel="stylesheet" href="../ImpactEarth.css">
</head>
 <!body style="font-family:calibri" text="#FFFFFF" bgcolor="#000000" link="#FFFFFF" vlink="#FFFFFF" alink="#FF0000">
 <body>

<table COLS=2 WIDTH=100%>
<tr>
<td><img class="banner_image" SRC="../imperial.png" BORDER=5></td>
<td><img class="banner_image" align=right SRC="../purduemark.png" BORDER=5></td>
</tr>
</table>

    <h1 align=center><a href="http://impact.ese.ic.ac.uk">Earth Impact Effects Program</a></h1>
<h3 align=center><a href="http://www.cfa.harvard.edu/~rmarcus/index.html">Robert Marcus</a>, <a href="http://www.purdue.edu/eas/people/faculty/melosh.html">H. Jay Melosh</a>, and <a href="http://www.imperial.ac.uk/people/g.collins">Gareth Collins</a></h3>
       	 
	       	<p>Welcome to the Earth Impact Effects Program: an easy-to-use, interactive web site for estimating the regional environmental
		consequences of an impact on Earth.  This program will estimate the ejecta distribution, ground shaking, atmospheric blast wave, and
		thermal effects of an impact as well as the size of the crater produced. </p>
		<p>Please enter values in the boxes below to describe your impact event of choice and your distance away.  Then click "Calculate
		Effects" to learn about the environmental consequences. </p>


EOF

    print "<font color=ff0000><dl><dt>Please re-enter the following items:";

    if ($valid[6] == 0) {
      print "<dd>Distance from Impact";
      if ($distance > 3.14159 * $R_earth) {
	print "<dd>Note:  The distance must be less than half the circumference of the Earth.";
      }
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
      print "<dd>Target Density";
    }
	

    print "</font></dl>";
	
    print <<EOF;
		<form action ="../cgi-bin/crater.cgi">
	
		<h3 align=left>Distance from Impact</h3>
		<p>Distance from Impact (in km)
EOF


    if ($valid[6] == 1) {	
      print "<input type=\"text\" name=\"dist\" value=$distance size=10>";
    } else {
      print"<input type=\"text\" name=\"dist\" size=10>";
    }

    print <<EOF;
		<h2 align=center>Enter Impact Parameters</h2>
		<h3 align=left>Projectile Parameters</h3>
		<blockquote>
		Projectile Diameter (in meters)
EOF


    if ($valid[0] == 1) {
      print "<input type=\"text\" name=\"diam\" value=$pdiameter size=10><br>";
    } else {
      print "<input type=\"text\" name=\"diam\" size=10><br>";
    }

    print "<p>Projectile Density (in kg/m<sup>3</sup>) ";

    if ($valid[1] == 1) {
      print "<input type=\"text\" name=\"pdens\" value=$pdensity size=10> or"; 
    } else {
      print "<input type=\"text\" name=\"pdens\" size=10> or";
    }


    print <<EOF;
		  <select name="pdens_select">
		     <option value="0">Select from a list
		     <option value="1000">1000 kg/m^3 for ice
		     <option value="1500">1500 kg/m^3 for porous rock
		     <option value="3000">3000 kg/m^3 for dense rock
		     <option value="8000">8000 kg/m^3 for iron
		  </select>
			</blockquote>
	
		<h3 align=left>Impact Parameters</h3>
		<blockquote>
		Impact Velocity (in km/s)
EOF


    if ($valid[2] == 1) {
      print "<input type=\"text\" name=\"vel\" value=$vInput size=10>";
    } else {
      print "<input type=\"text\" name=\"vel\" size=10>";
    }
    print <<EOF;

		<p>This is the velocity of the projectile before it enters the atmosphere.  The minimum impact velocity on Earth is 11 km/s.  Typical
		impact velocities are 17 km/s for asteroids and 51 km/s for comets.  The maximum Earth impact velocity for objects orbiting the sun is
		72 km/s.
	
EOF


    print "<p>Impact Angle (in degrees) ";

    if ($valid[3] == 1) {
      print "<input type=\"text\" name=\"theta\" value=$theta size=10>";
    } else {
      print "<input type=\"text\" name=\"theta\" size=10>";
    }


    print <<EOF;
	
		<p>The impact angle is measured from a plane tangent to the impact surface.  This angle is 90 degrees for a vertical impact.  The most
		probable angle of impact is 45 degrees.
		</blockquote>
		<h3 align=left>Target Parameters</h3>
		<blockquote>
		Target Density (in kg/m<sup>3</sup>)
EOF


    if ($valid[4] == 1) {
      print "<input type=\"text\" name=\"tdens\" value=$tdensity size=10> or";
    } else {
      print "<input type=\"text\" name=\"tdens\" size=10> or ";
    } 

    print <<EOF;
		<select name="tdens_select">
		     <option value="0">Select from a list
		     <option value="1000">1000 kg/m^3 for ice or water
		     <option value="1500">1500 kg/m^3 for porous rock
		     <option value="3000">3000 kg/m^3 for dense rock
		  </select>
	
		</blockquote>
	
EOF

	print <<EOF;
		<br>
		<center>
		<input type="submit" value="Calculate Effects">
		<input type="reset" value="Reset Form">
		</center>
		
		</form>
		<p>
		<br>
EOF
		
	print_pdf();
	print "<hr>\n<br>\n</body>\n</html>\n";



}                 ###  End of sub reprint_form


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
        print "<dd>The larger of these two energies is used to estimate the airblast damage.";
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

