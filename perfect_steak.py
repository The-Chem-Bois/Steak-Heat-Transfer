'''
authors:
Oliver Erdmann # 20843970 - github @ Polsander
Juan De Leon Solis # 20765671
Miguel Guerra # 20808811

This file is designed to solve and present data for finding out how to cook the perfect steak
We use the heat_function import as the MOL tool used to compute the temperature profile of the steak

The goal of this code is to compute what a reasonable time is to cook 
'''
import numpy as np
from heat_function import get_steak_T_profile
import matplotlib.pyplot as plt

#Define our nodes and intervals:
dz=.00127 # m (allows us to have 31 nodes)
z0,zend = 0,0.0381 #thickness range of steak in m 
n=int((zend-z0)/dz + 1) #number of points in z

# Define function that allows to get new Temperature profile for initial conditions
def get_new_IC(array, time_position):
    #Array is the temperatures of all nodes and times
    # time_position is the time we want to flip at
    target_profile = []
    for node in array:
        target_profile.append(node[time_position])
    #since the steak gets flipped, all values must be reversed
    target_profile = np.flip(target_profile)
    return target_profile

# First we place the steak on our 190 degree celsius pan, with all nodes being room temp
# Define initial condition and find Temperature profile
T_room = 25 + 273.15 #Kelvin
IC_1 = np.ones(n)*T_room

Temperature_1, time_1 = get_steak_T_profile(IC_1)

print(f'After 10 minutes, the internal (middle) temperature of the steak is found to be\
 {round(Temperature_1[15][-1] -273.15,2)} degrees celsiuis. A perfectly cooked medium steak is 60 degrees C\
 in the center. Furthermore the temperature of the bottom of the steak is {round(Temperature_1[0][-1]-273.15,2)}\
 celsius, and has been close to that temperature for a prolonged time, which means the bottom is definitely burned to a crisp.\n')

print('To prevent the meat from burning before it even has a chance to cook, we can choose to flip \
at 5 minutes. This will allow the other side of the steak to nicely cook, while preventing the bottom\
from burning due to prolonged heat exposure from the pan')

#5 mins is the time index at 10
print(f'\n After 5 mins of cooking,\
\nBottom Temperature:{round(Temperature_1[0][10]-273.15,2)} °C \nMiddle Temperature: {round(Temperature_1[15][10]-273.15,2)} °C\n')
IC_2 = get_new_IC(Temperature_1, 10)
Temperature_2, time_2 = get_steak_T_profile(IC_2)

print("Cooking the steak on the second flip, at 5 minutes we get the following temperatures:")
print(f"New Bottom : {round(Temperature_2[0][10]-273.15,2)}°C \nMiddle: {round(Temperature_2[15][10]-273.15,2)}°C \
\nWe flip again to stay conservative and not burn the steak")
# Flip one more time (flipping at minute 5, so index 10)
IC_3 = get_new_IC(Temperature_2, 10)
Temperature_3, time_3 = get_steak_T_profile(IC_3)
print("\nCooking for 3 minutes, we get:")
print(f"New Bottom : {round(Temperature_3[0][6]-273.15,2)}°C \nMiddle: {round(Temperature_3[15][6]-273.15,2)}°C \
\nOur steak is done and is perfectly cooked to medium")

#Obtain array of all nodes
nodes = np.arange(0,n)
#Get the last conditions of our final steak temperature profile
IC_4 = np.flip(get_new_IC(Temperature_3,6))

#Plotting steak temperature profile at flip
plt.figure(1)
plt.plot(nodes, np.flip(IC_2) -273.15, label="No flip, 5 mins cooking")
plt.plot(nodes, IC_3 -273.15, label="1st flip, 5 mins cooking")
plt.plot(nodes, IC_4 -273.15, label="2nd flip, 3 mins cooking")
plt.legend()
plt.title("Final Temperature profile of Steak at flips")
plt.xlabel("Nodes (fixed)")
plt.ylabel("Temperature (°C)")
plt.show()

#Plotting the change of temperature at the internal node
Internal_T = np.hstack([Temperature_1[15][:11],Temperature_2[15][:11],Temperature_3[15][:7]])
times = np.hstack([time_1[:11],time_2[:11]+time_1[10],time_3[:7]+time_2[10]+time_1[10]])


plt.figure(2)
plt.plot(times,Internal_T-273.15)
plt.plot(times[10],Internal_T[10]-273.15, "ro", label="first flip")
plt.plot(times[21],Internal_T[21]-273.15, "go",label="second flip")
plt.ylabel("Temperature (°C)")
plt.xlabel("Time (s)")
plt.title("Middle (Internal Node) Temperature of the Steak")
plt.legend()
plt.show()