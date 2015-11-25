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

datos=n.loadtxt("DR9Q.dat", usecols=(80,81,82,83))

banda_i=datos[:,0]*3.631
error_i=datos[:,1]*3.631
banda_z=datos[:,2]*3.631
error_z=datos[:,3]*3.631

ajuste=n.polyfit(banda_i,banda_z,1)

m=ajuste[0]
coef=ajuste[1]

print m
print coef




def intervalo(datos):

    '''Recibe los datos y devuelve los intervalos de confianza
    de los parametros m y n de la recta mx+n y las muestras generadas'''

    banda_i=datos[:,0]*3.631
    error_i=datos[:,1]*3.631
    banda_z=datos[:,2]*3.631
    error_z=datos[:,3]*3.631
   
    N_mc = 100000
    m = n.zeros(N_mc)
    coef=n.zeros(N_mc)
    for i in range(N_mc):
        r = n.random.normal(0,1,size=len(banda_i))
        datos_i=banda_i+error_i*r
        datos_z=banda_z+error_z*r
        ajuste=n.polyfit(datos_i, datos_z, 1)
        m[i]=ajuste[0]
        coef[i]=ajuste[1]

    m=n.sort(m)
    coef=n.sort(coef)
    limite_bajo_m=m[int(N_mc*0.025)]
    limite_alto_m=m[int(N_mc*0.975)]

    limite_bajo_coef=coef[int(N_mc*0.025)]
    limite_alto_coef=coef[int(N_mc*0.975)]
    print "El intervalo de confianza de m al 95% es: [{}:{}]".format(limite_bajo_m, limite_alto_m)
    print "El intervalo de confianza de n al 95% es: [{}:{}]".format(limite_bajo_coef, limite_alto_coef)
    return [m,coef]


[a,b]=intervalo(datos)

x=n.linspace(0,450,1001)

p.plot(banda_i,banda_z, '*', label='datos reales')
p.plot(x,m*x+coef, linewidth=2, label='ajuste lineal')
p.xlabel('Flujo banda i x10^-6[Jy]')
p.ylabel('Flujo banda z x10^-6[Jy]')
p.legend(loc='upper right')
p.show()

p.hist(a,bins=100)
p.xlabel('m')
p.ylabel('Frecuencia')
p.title('Distribucion de m')
p.show()

p.hist(b,bins=100)
p.xlabel('n')
p.ylabel('Frecuencia')
p.title('Distribucion de n')
p.show()

