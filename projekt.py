'''
Python for calculating temperature profile of steak :)

Juan De Leon Solis : 20765671
Miguel Angel Guerra Gonzalez: 20808811
Oliver Erdmann : 20843970
'''
import numpy as np
from scipy.optimize import fsolve
from scipy.integrate import solve_ivp

# Define our variables
To = 218 + 273.15 # Initial Temperature of pan/bottom of the steak at t>0
k = 0.41 # J/(m K s)
rho = 1.033 * 100**3 #g/m^3
cp = 1.67 #J/ (g K)
h = 25 #J/(m^2 K s)
Tinf = 25 +273.15 # room temperature K
alpha = k/(rho*cp) #m^2/s


#time 
(t0,tend)=(0,600)

#z grid
dz=.0028 # m (allows us to have 15 nodes)
z0,zend = 0,0.04 #m 

n=int((zend-z0)/dz + 1) #number of points in z
z_val=np.linspace(z0,zend,n)

#Define 
def ode(t,T):
    #t is our time
    #T is our temperature vector [T1,T2,....]
    

    T_all=np.hstack([To,T])
    #dT[0]=T_all[2]-2*T_all[1]+T_all[0]

    #last node 
    #dV[n+1]=V_all[n+2]-2*V_all[n+1]+V_all[n]
    #sub in BC
    #dV[n+1]=-2*V_all[n+1]+2 V_all[n]



    #vectorized from before applies to all but last node
    dT=np.zeros(T.size)
    dT[:-1]=T_all[2:]-2*T_all[1:-1]+T_all[:-2]
    dT[-1]=(2*h*dz*(Tinf-T_all[-1]))/k-2*T_all[-1] +2*T_all[-2]
    return dT*(alpha/dz**2)

Tinit=np.ones(n)*Tinf

#solve
solution=solve_ivp(ode,[t0,tend],Tinit,t_eval=np.arange(t0,tend,30)) # 120 signifies taking a point each 30 seconds

breakpoint()





