# Imports ground_track library
from ground_track import *

# Molnyia ground track
molnyia = Orbit( 26600,  #major semiaxis
                 0.74,   #eccentricity
                 63.4,   #inclination
                 80,     #accending node
                 270     #periapsis argument
               )
molnyia.evaluate(0, 2*molnyia.period) # evaluates orbit at two periods

molnyia.save_data("molnyia") 	# saves text file with results

molnyia.plot_track()            # plots ground track
molnyia.plot_3D()               # plots 3D orbit

Q = molnyia.apoapsis		# gets orbit apoapsis
q = molnyia.periapsis		# gets orbit periapsis
energy = molnyia.c3		# gets orbit specific energy
moment = molnyia.ang_moment	# gets orbit specific moment

print("Molnyia parameters")
print("Apoapsis: ", Q)
print("Periapsis: ", q)
print("Specific moment: ", moment)
print("Specific energy: ", energy)

vQ     = molnyia.v_at(180)	# gets velocity at apoapsis
gammaQ = molnyia.gamma_at(180)  # gets flight angle at apoapsis
vq     = molnyia.v_at(0)	# gets velocity at periapsis
gammaq = molnyia.gamma_at(0)	# gets flight angle at periapsis

f1     = molnyia.f_at(molnyia.period/4) # gets true anomaly at a quarter of period
r1     = molnyia.r_at(f1)		# gets radius at a quarter of period
v1     = molnyia.v_at(f1)		# gets velocity at a quarter of period
gamma1 = molnyia.gamma_at(f1)		# gets flight angle at a quarter of period

print("Time\t True Anomaly\t Radius\t Velocity\t Flight angle")
print("{:.2f}\t {:.2f}\t {:.2f}\t {:.2f}\t {}".format(0, 0, q, vq, gammaq))
print("{:.2f}\t {:.2f}\t {:.2f}\t {:.2f}\t {}".format(molnyia.period/4, f1, r1, v1, gamma1))
print("{:.2f}\t {:.2f}\t {:.2f}\t {:.2f}\t {}".format(molnyia.period/2, 180, Q, vQ, gammaQ))


# Space Station gorund track
iss = Orbit(417 + 6371, 0.01, 51.64, time_mode="hours", delta_t = 10/3600)
iss.evaluate(0, 24)
iss.save_data("iss")
iss.plot_track()
