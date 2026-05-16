#Parabolic motion on python

import numpy as np
import matplotlib.pyplot as plt

#Physical Parameters
x_0 = 0 #Inial x coordinate in m
y_0 = 0 #Initial y coordinate in m
v_0 = float(input("Type initial velocity:")) #Initial velocity in m/s
g = 9.8 #Gravity acceleration in m/s^2
dt = 0.01 
theta = float(input("Type the angle in degrees:")) 

theta_rad = theta*np.pi/ 180 #Conversion to radians

#Defining inital velocities
v_x = v_0*np.cos(theta_rad) #Horizontal velocity equation
v_y = v_0*np.sin(theta_rad) #Vertical velocity equation

#Updating the motion
x = x_0
y = y_0

x_values = [] #Guardar os valores de x (Historico de x)
y_values = [] #Guardar os valores de y (Historico de y)

while y >= 0:
    x_values.append(x) #Guarde o valor atual de x dentro da lista
    y_values.append(y) #Guarde o valor atual de y dentro da lista 
    x = x + v_x*dt
    y = y + v_y*dt
    
    v_y = v_y - g*dt #Updating velocity in y coordinate

#Plotting the results
plt.plot(x_values, y_values)
plt.xlabel("Vertical Position (m)")
plt.ylabel("Horizontal Position (m)")
plt.title("Parabolic motion")
plt.grid(True)

plt.show()
