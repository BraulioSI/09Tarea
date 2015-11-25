from __future__ import division
from math import *
#from scipy import integrate as int
from scipy.optimize import (leastsq, curve_fit)
from scipy.integrate import ode
import pyfits #modulo para leer archivos fits
import matplotlib.pyplot as p #modulo para graficar
import numpy as n #este modulo es para trabajar con matrices como en matlab
import matplotlib as mp
from mpl_toolkits.mplot3d import Axes3D
import random

datos=n.loadtxt('hubble.txt')  #datos

dist=datos[:,0]   #distancia
vel=datos[:,1]     #velocidad

def linea(H,x):     #funcion a fitear
    return H*x


a1= curve_fit(linea,dist,vel)   #ley v=Hd
a2= curve_fit(linea,vel,dist)   #ley d=v/H
H0=(a1[0]+(1.0/a2[0]))/2.0      #promedio

print H0


def intervalo(datos):

    '''Devuelve el intervalo de confianza
        y la muestra de datos'''
   
    N=len(datos)
    N_boot = 100000
    H = n.zeros(N_boot)
    for i in range(N_boot):
        s = n.random.randint(low=0, high=N, size=N)
        distancia = datos[s,0]
        vel = datos[s,1]
        a1 = curve_fit(linea,distancia, vel)
        a2 = curve_fit(linea,vel, distancia)
        a = (a1[0] + (1.0/a2[0])) / 2
        H[i] = a

    H=n.sort(H)
    limite_bajo=H[int(N_boot*0.025)]
    limite_alto=H[int(N_boot*0.975)]
    print "El intervalo de confianza al 95% es: [{}:{}]".format(limite_bajo, limite_alto)
    return H

    
H=intervalo(datos)

x=n.linspace(0,2.5,251)

p.plot(dist,vel, '*', label='datos reales')
p.plot(x,linea(H0,x), linewidth=2, label='ajuste lineal')
p.xlabel('Distancia [Mpc]')
p.ylabel('Velocidad [km/s]')
p.legend(loc='upper right')
p.title('Ley de Hubble')
p.show()

p.hist(H,bins=100)

p.xlabel('H0 [km/s/Mpc]')
p.ylabel('Frecuencia')

p.title('Distribucion de H0')
p.show()
