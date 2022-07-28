'''
Python for calculating temperature profile of steak :)

Juan De Leon Solis : 20765671
Miguel Angel Guerra Gonzalez: 20808811
Oliver Erdmann : 20843970
'''
import numpy as np
from scipy.integrate import solve_ivp

# Define our variables
To = 218 + 273.15 # Initial Temperature of pan/bottom of the steak at t>0
k = 0.41 # heat transfer coefficient J/(m K s)
rho = 1.033 * 100**3 #density g/m^3
cp = 2.7 #heat capacity of steak J/ (g K)
h = 25 #air convection coefficient J/(m^2 K s)
Tinf = 25 +273.15 # room temperature in K
alpha = k/(rho*cp) #defined constant m^2/s


#time 
(t0,tend)=(0,600)

#z grid
dz=.00127 # m (allows us to have 31 nodes)
z0,zend = 0,0.0381 #thickness range of steak in m 

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



    #vectorized form before applies to all but last node
    dT=np.zeros(T.size)
    dT[:-1]=T_all[2:]-2*T_all[1:-1]+T_all[:-2]
    dT[-1]=(2*h*dz*(Tinf-T_all[-1]))/k-2*T_all[-1] +2*T_all[-2]
    return dT*(alpha/dz**2)

def get_steak_T_profile(initial_condition):
    '''
    A reusable function defined to easily call and get the temperature profile of a steak
    for different initial conditions.

    Parameters

    initial_condition : An array of size 31 (number of nodes) of initial conditions which represents
                        the temperature of each node at the point when the steak is either flipped
                        or initially placed on the pan.
    
    Returns
    
    Temperatures : A numpy array of the temperature profile containing another array for
                    each node with different temperature values for every 30 seconds.
    
    Times : Each time value at which the temperature of the nodes are taken in seconds (cumulative).

    '''
    time_interval = np.arange(0,630,30) # 600 seconds is 10 minutes, every 30 second interval
    solution=solve_ivp(ode,[t0,tend],initial_condition,t_eval=time_interval)



if __name__ == "__main__":
    #Just testing function
    Tinit=np.ones(n)*Tinf
    #solve
    time_interval = np.arange(0,630,30) # 600 seconds is 10 minutes, every 30 second interval
    solution=solve_ivp(ode,[t0,tend],Tinit,t_eval=time_interval) # 30 signifies taking a point each 30 seconds

    print('Running main')




