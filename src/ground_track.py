#!/usr/bin/python
##############################################################
#
#   Python library for orbit ground track ploting
#
#   Authors: Arthur Gabardo*, Andre Canani, Vinicus Pereira
#
#   Date: 18/11/2022
#
#   Mail: arthur.miguel@grad.ufsc.br
#
#############################################################


import numpy as np
from subprocess import call
from scipy.optimize import newton


tModes = ["seconds", "minutes", "hours", "days"]

def E_prime(E_, M, e): return E_ - e*np.sin(E_) - M

class Orbit:
    """
    Orbit object, major semiaxis and eccentricity are required, other parameters are optional
    params: a         = major semiaxis
            e         = eccentricity
            I         = inclination
            Omega     = accending node longitude
            omega     = periapsis argument
            epoch     = starting time
            time_mode = input time unit
            delta_t   = time-step
            mu        = standard gravitational parameter
    """
    def __init__(self,
                 a,
                 e,
                 I=0,
                 Omega=0,
                 omega=0,
                 epoch=0,
                 time_mode="seconds",
                 delta_t=10,
                 mu=398600):

        if (time_mode not in tModes):
            self.time_mode = input("Invalid time mode, select a valid one ({}): ".format(tModes))
        else: self.time_mode = time_mode

        if (time_mode == "seconds"): self.t_factor = 1
        if (time_mode == "minutes"): self.t_factor = 1/60
        if (time_mode == "hours")  : self.t_factor = 1/3600
        if (time_mode == "days")   : self.t_factor = 1/86400


        if (delta_t <= 0):
            self.delta_t = input("Invalid time-step (delta_t > 0$): ")
        else : self.delta_t = delta_t

        if (a <= 0):
            self.a = input("Invalid major semiaxis (a > 0): ")
        else: self.a = a

        if (e < 0):
            self.e = input("Invalid excentricity (e >= 0): ")
        else: self.e = e

        if (I > np.pi):
            self.I = (I%180) * (np.pi/180)
        elif (I < 0):
            while(I < 0): I += 360
            self.I = (I%180) * (np.pi/180)
        else: self.I = I * (np.pi/180)

        self.Omega = Omega%(360) * (np.pi/180)
        self.omega = omega%(360) * (np.pi/180)

        self.mu = abs(mu) * (1/self.t_factor)**2

        self.epoch = epoch
        self.period = 2*np.pi * np.sqrt(self.a**3/self.mu)

        self.__set_rotation_mat__()
        return

    def __set_rotation_mat__(self):
        """Sets rotation matices based on orbit parameters"""
        self.R_O = np.array([[np.cos(self.Omega), -np.sin(self.Omega), 0],
                             [np.sin(self.Omega),  np.cos(self.Omega), 0],
                             [                 0,                   0, 1]])

        self.R_o = np.array([[np.cos(self.omega), -np.sin(self.omega), 0],
                             [np.sin(self.omega),  np.cos(self.omega), 0],
                             [                 0,                   0, 1]])

        self.R_I = np.array([[1,              0,               0],
                             [0, np.cos(self.I), -np.sin(self.I)],
                             [0, np.sin(self.I),  np.cos(self.I)]])
        return

    def __M_f__(self):
        """Calculates mean anomaly at given time"""
        M =  (2*np.pi/self.period) * (self.t - self.epoch)
        for i, Mi in enumerate(M):
            while M[i] < 0         : M[i] += (2*np.pi)
            while M[i] > (2*np.pi) : M[i] -= (2*np.pi)
        self.M = np.array(M)
        return self.M

    def __E_f__(self):
        """Calculates eccentic anomaly from mean anomaly using newton-raphson method"""
        E = []
        for i, Mi in enumerate(self.M):
            Ei = newton(E_prime, Mi, args=(Mi, self.e,))
            while Ei < 0         : Ei+=(2*np.pi)
            while Ei > (2*np.pi) : Ei-=(2*np.pi)
            E.append(Ei)
        self.E = np.array(E)
        return self.E

    def __E2f__(self):
        """Converts eccentric anomaly to true anomaly"""
        f = []
        for i, Ei in enumerate(self.E):
            fi = (2*np.arctan2(np.sqrt(1+self.e) * np.tan(Ei/2), np.sqrt(1-self.e)))
            while fi < 0         : fi+=(2*np.pi)
            while fi > (2*np.pi) : fi-=(2*np.pi)
            f.append(fi)
        self.f = np.array(f)
        return self.f

    def __radius__(self):
        """Computes orbit radius at a given true anomaly"""
        self.radius_t = self.a*(1-self.e**2)/(1 + self.e*np.cos(self.f))
        return self.radius_t

    def __toEqCoords__(self):
        """Transforms orbit plane coordinates to equatorial coordinates"""
        rot = np.matmul(np.matmul(self.R_O, self.R_I), self.R_o)
        anom = [np.cos(self.f), np.sin(self.f), np.zeros(len(self.f))]
        anom = np.array(anom).T

        r = self.__radius__()

        xyz = []
        for i, anomi in enumerate(anom):
            xyz.append(np.matmul(rot, anomi) * r[i])
        self.xyz = np.array(xyz).T
        return self.xyz

    def __longitude__(self):
        """Calculates longitude based on earths rotation and equatorial coordinates"""
        x, y, z = self.xyz
        long = []
        for i in range(len(x)):
            phi = np.arctan2(y[i], x[i]) - (np.pi/(3600*12*self.t_factor))*(self.t[i] - self.epoch)
            while phi < -np.pi : phi+=(2*np.pi)
            while phi >  np.pi : phi-=(2*np.pi)
            long.append(phi)
        self.longitude_t = np.array(long)
        return self.longitude_t

    def __latitude__(self):
        """Calculates latitude based on equatorial coordinates"""
        x, y, z = self.xyz
        lat = []
        for i in range(len(x)):
            delta = np.arctan2(z[i], np.sqrt(x[i]**2 + y[i]**2))
            while delta < -np.pi/2 : delta+=(np.pi)
            while delta >  np.pi/2 : delta-=(np.pi)
            lat.append(delta)
        self.latitude_t = np.array(lat)
        return self.latitude_t

    def __interpolate__(self, arr, t0):
        idx = np.abs(self.t - t0).argmin()
        if self.t[idx] - t0 == 0 : return arr[idx]
        elif self.t[idx] - t0 > 0 :
            t1 = self.t[idx-1]; M1 = arr[idx-1]
            t2 = self.t[idx]; M2 = arr[idx]
        else:
            t1 = self.t[idx]; M1 = arr[idx]
            t2 = self.t[idx+1]; M2 = arr[idx+1]
        return (M1 - M2)/(t1 - t2) * (t0 - t1) + M1

    def evaluate(self, begin=None, end=None):
        """
        Computes orbit kinematics at a time interval
        param: begin = begining of time interval (default is epoch)
               end   = end of time interval (default is one period)
        """
        if begin is None : begin = self.epoch
        if end is None : end = self.period
        t = np.arange(begin, end, self.delta_t )
        self.t = t
        self.__M_f__()
        self.__E_f__()
        self.__E2f__()
        self.__toEqCoords__()
        self.__longitude__()
        self.__latitude__()
        return

    def save_data(self, fname="orbit"):
        """
        Saves orbit data to text file
        param: fname = output file name
        return: a text file with following values in each column
                time | true anom. | ecc. anom. | mean anom. | x | y | z | long. | lat.
        """
        data = np.column_stack((self.t, self.f, self.E, self.M, self.xyz[0], self.xyz[1], self.xyz[2], self.longitude_t * (180/np.pi), self.latitude_t * (180/np.pi)))
        np.savetxt(fname, data)
        self.fname = fname
        return

    def plot_track(self, output=None):
        if output is None : output = self.fname + ".png"
        if self.time_mode == "seconds" : tscale = 1.0/60
        elif self.time_mode == "minutes" : tscale = 1.0
        elif self.time_mode == "hours" : tscale = 60.0
        else : tscale = 60*24.0
        cmd = "gnuplot -p -e \"filename='{}'; outputfile='{}'; delta_t = {}\" rota_solo.plt".format(self.fname, output, tscale)
        call(cmd, shell=True)
        #long = self.longitude_t; lat = self.latitude_t
        #pos = np.where(np.abs(np.diff(long)) >= 0.5)[0]+1
        #long = np.insert(long, pos, np.nan)
        #lat = np.insert(lat, pos, np.nan)

        #worldm = cv.imread(background)
        #worldm = cv.cvtColor(worldm, cv.COLOR_BGR2RGB)
        #h, w, _ = worldm.shape
        #plt.imshow(worldm, extent=[-180, 180, -90, 90])
        #plt.plot(long * (180/np.pi), lat * (180/np.pi), color="red")
        #plt.tight_layout()
        #plt.savefig(fname)
        #plt.show()
        return

    def M_at(self, t):
        return self.__interpolate__(self.M, t)

    def E_at(self, t): 
        return self.__interpolate__(self.E, t)

    def f_at(self, t):
        return self.__interpolate__(self.f, t)

    def r_at(self, t):
        return self.__interpolate__(self.radius_t, t)

    def long_at(self, t):
        return self.__interpolate__(self.longitude_t, t)

    def lat_at(self, t):
        return self.__interpolate__(self.latitude_t, t)