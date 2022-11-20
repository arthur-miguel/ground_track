import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton
from subprocess import call

tModes = ["seconds", "minutes", "hours", "days"]

def E_prime(E_, M, e): return E_ - e*np.sin(E_) - M

class Orbit:
    
    def __init__(self,
                 a,
                 e,
                 I=0,
                 Omega=0,
                 omega=0,
                 epoch=0,
                 time_mode="seconds",
                 delta_t=1,
                 mu=398600):
        
        if (time_mode not in tModes):
            self.time_mode = input("Invalid time mode, select a valid one ({}): ".format(tModes))
        else:
            self.time_mode = time_mode
            
        if (time_mode == "seconds"): self.t_factor = 3600
        if (time_mode == "minutes"): self.t_factor = 60
        if (time_mode == "hours")  : self.t_factor = 1
        if (time_mode == "days")   : self.t_factor = 1/24
        
        
        if (delta_t <= 0):
            self.delta_t = input("Invalid time-step (delta_t > 0$): ")
        
        if (a <= 0):
            self.a = input("Invalid major semiaxis (a > 0): ")
        else:
            self.a = a
            
        if (e < 0):
            self.e = input("Invalid excentricity (e >= 0): ")
        else:
            self.e = e
        
        if (I > np.pi):
            self.I = I%np.pi
        elif (I < 0):
            while(I < 0): I += 2*np.pi
            self.I = I%np.pi
        else:
            self.I = I
            
        self.Omega = Omega%(2*np.pi)
        self.omega = omega%(2*np.pi)

        self.mu = abs(mu)
        
        self.epoch = epoch
        self.period = 2*np.pi * np.sqrt(a**3/mu)
        
        self.__set_rotation_mat__()
        return

    def __set_rotation_mat__(self):
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
    
    def M_f(self):
        M =  (2*np.pi/self.period) * (self.t - self.epoch)
        for i, Mi in enumerate(M):
            while M[i] < 0         : M[i] += (2*np.pi)
            while M[i] > (2*np.pi) : M[i] -= (2*np.pi)
        self.M = np.array(M)
        return self.M

    def E_f(self):
        E = []
        for i, Mi in enumerate(self.M):
            Ei = newton(E_prime, Mi, args=(Mi, self.e,))
            while Ei < 0         : Ei+=(2*np.pi)
            while Ei > (2*np.pi) : Ei-=(2*np.pi)          
            E.append(Ei)
        self.E = np.array(E)
        return self.E

    def E2f(self):
        f = []
        for i, Ei in enumerate(self.E):
            fi = (2*np.arctan2(np.sqrt(1+self.e) * np.tan(Ei/2), np.sqrt(1-self.e)))
            while fi < 0         : fi+=(2*np.pi)
            while fi > (2*np.pi) : fi-=(2*np.pi)
            f.append(fi)
        self.f = np.array(f)
        return self.f

    def __radius(self):
        self.radius_t = self.a*(1-self.e**2)/(1 + self.e*np.cos(self.f))
        return self.radius_t

    def toEqCoords(self):
        rot = np.matmul(np.matmul(self.R_O, self.R_I), self.R_o)
        anom = [np.cos(self.f), np.sin(self.f), np.zeros(len(self.f))]
        anom = np.array(anom).T

        r = self.__radius()

        xyz = [] 
        for i, anomi in enumerate(anom):
            xyz.append(np.matmul(rot, anomi) * r[i])
        self.xyz = np.array(xyz).T
        return self.xyz

    def longitude(self):
        x, y, z = self.xyz
        long = []
        for i in range(len(x)):
            phi = np.arctan2(y[i], x[i]) - (np.pi/(12*self.t_factor))*(self.t[i] - self.epoch)
            while phi < -np.pi : phi+=(2*np.pi)
            while phi >  np.pi : phi-=(2*np.pi)
            long.append(phi)
        self.longitude_t = np.array(long)
        return self.longitude_t

    def latitude(self):
        x, y, z = self.xyz
        lat = []
        for i in range(len(x)):
            delta = np.arctan2(z[i], np.sqrt(x[i]**2 + y[i]**2))
            while delta < -np.pi/2 : delta+=(np.pi)
            while delta >  np.pi/2 : delta-=(np.pi)
            lat.append(delta)
        self.latitude_t = np.array(lat)
        return self.latitude_t
    
    def evaluate(self, t):
        self.t = t
        self.M_f()
        self.E_f()
        self.E2f()
        self.toEqCoords()
        self.longitude()
        self.latitude()
        return
    
    def save_data(self, fname="orbit.csv"):
        data = np.column_stack((self.t, self.M, self.f, self.E, self.M, self.xyz[0], self.xyz[1], self.xyz[2], self.longitude_t * (180/np.pi), self.latitude_t * (180/np.pi)))
        np.savetxt(fname, data)
        return
    
    def plot_track(self, fname):
        cmd = "gnuplot -e \"filename='{}'\" rota_solo.txt".format(fname)
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
