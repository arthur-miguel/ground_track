# Imports ground_track library
from ground_track import *

# Molnyia ground track
molnyia = Orbit( 26600,  #major semiaxis
                 0.74,   #eccentricity
                 63.4,   #inclination
                 80,     #accending node
                 270     #periapsis argument
               )

molnyia.evaluate(0, 2*molnyia.period)   # evaluates orbit at two periods

molnyia.save_data("molnyia") 	        # saves text file with results

molnyia.plot_track()                    # plots ground track
molnyia.plot_3D()                       # plots 3D orbit

Q = molnyia.apoapsis		            # gets orbit apoapsis
q = molnyia.periapsis		            # gets orbit periapsis
energy = molnyia.c3		                # gets orbit specific energy
moment = molnyia.ang_moment	            # gets orbit specific moment

print("Molnyia parameters")
print("Apoapsis: ", Q)
print("Periapsis: ", q)
print("Specific moment: ", moment)
print("Specific energy: ", energy)

tQ     = molnyia.period/2
vQ     = molnyia.v_at(180)	            # gets velocity at apoapsis
gammaQ = molnyia.gamma_at(180)          # gets flight angle at apoapsis
vq     = molnyia.v_at(0)	            # gets velocity at periapsis
gammaq = molnyia.gamma_at(0)	        # gets flight angle at periapsis

t1     = molnyia.period*0.17
f1     = molnyia.f_at(t1)               # gets true anomaly at a quarter of period
r1     = molnyia.r_at(f1)               # gets radius at a quarter of period
v1     = molnyia.v_at(f1)		        # gets velocity at a quarter of period
gamma1 = molnyia.gamma_at(f1)		    # gets flight angle at a quarter of period

t2     = molnyia.period*0.33
f2     = molnyia.f_at(t2)               # gets true anomaly at a quarter of period
r2     = molnyia.r_at(f2)               # gets radius at a quarter of period
v2     = molnyia.v_at(f2)		        # gets velocity at a quarter of period
gamma2 = molnyia.gamma_at(f2)		    # gets flight angle at a quarter of period

table = {
        0  : [0,   q, vq, gammaq],
        t1 : [f1, r1, v1, gamma1],
        t2 : [f2, r2, v2, gamma2],
        tQ : [180, Q, vQ, gammaQ]      
        }

print("\nTime of flight")
print ("{:<8} {:<15} {:<10} {:<10} {:<10}".format('Time','True anomaly','Radius','Velocity','Flight angle'))
for time, params in table.items():
    anom, radius, vel, angle = params
    print ("{:<8} {:<15} {:<10} {:<10} {:<10}".format(round(time/3600, 2), 
                                                      round(anom,2),  
                                                      round(radius,2), 
                                                      round(vel,2), 
                                                      round(angle,2)))

# Space Station gorund track
iss = Orbit(417 + 6371, 0.01, 51.64, time_mode="hours", delta_t = 10/3600)
iss.evaluate(0, 24)
iss.save_data("iss")
iss.plot_track()
