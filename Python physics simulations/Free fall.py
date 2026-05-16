#Free fall simulation
#y(t) = y0 + v0*t - (g*t^2)/2
#v(t) = v0 - g*t
import numpy as np
import matplotlib.pyplot as plt

#Physical parameters
v0 = 0 #initial velocity in m/s
g = 9.8 #acceleration due to gravity in m/s^2
y0 = 500 #initial height in m

t_total = np.sqrt(2*y0/g) #total time of fall
t = np.linspace(0, t_total, 100) #time array from 0 to total time

#Equation of motion solved for y(t)
y = y0 + v0*t - (g*t**2)/2

#Plotting the results
plt.plot(t, y)
plt.title('Free Fall Simulation')
plt.xlabel('Time (s)')
plt.ylabel('Height (m)')
plt.grid(True)

plt.show()
