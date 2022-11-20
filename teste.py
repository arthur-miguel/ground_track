from ground_track import *

iss = Orbit( a = 417 + 6371,
             e = 0.01,
             I = 51.64 * (np.pi/180))

iss.evaluate(np.linspace(0, 24*3600, 10000))
fname = "iss.txt"
iss.save_data(fname)
iss.plot_track(fname)

molnyia = Orbit(26600, 0.74, 63.4 * (np.pi/180), 80 * (np.pi/180), 270 * (np.pi/180))
molnyia.evaluate(np.linspace(0, 24*3600, 10000))
molnyia.save_data("molnyia.txt")
molnyia.plot_track("molnyia.txt")
