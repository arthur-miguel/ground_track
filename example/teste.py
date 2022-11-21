# Imports ground_track library
from ../ground_track import *

# Molnyia ground track
molnyia = Orbit( a = 26600, #major semiaxis
                0.74, #eccentricity
                63.4 * (np.pi/180), #inclination
                80 * (np.pi/180), #accending node
                270 * (np.pi/180) #periapsis argument
               )
molnyia.evaluate(np.linspace(0, 2*molnyia.period, 10000)) # evaluates orbit at two periods
molnyia.save_data("molnyia.txt") # saves text file with results
molnyia.plot_track() # plots ground track

# Space Station gorund track
iss = Orbit(417 + 6371, 0.01, 51.64 * (np.pi/180))

iss.evaluate(np.linspace(0, 24*3600, 10000))
iss.save_data("iss.txt")
iss.plot_track()

