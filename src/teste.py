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
molnyia.save_data("molnyia") # saves text file with results
molnyia.plot_track() # plots ground track

# Space Station gorund track
iss = Orbit(417 + 6371, 0.01, 51.64, time_mode="hours", delta_t = 10/3600)
iss.evaluate(0, 24)
iss.save_data("iss")
iss.plot_track()

