# Starter code based on https://projects.raspberrypi.org/en/projects/temperature-log 
# and https://github.com/raspberrypilearning/temperature-log
#modified by Loyda Yusufova 2/6/2024

from gpiozero import CPUTemperature
from time import sleep, strftime, time
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.animation as animation
import psutil
import os
    
# Create figure for plotting
fig = plt.figure()
temp_plt = fig.add_subplot(3, 1, 1)
util_plt = fig.add_subplot(3, 1, 2)
freq_plt = fig.add_subplot(3, 1, 3)
xtime = []
ytemp = []
yutil = []
yfreq = []

plt.subplots_adjust(top=0.97, bottom=0.14, left=0.30, right=0.7, hspace=0.7,wspace=0.035) 

# Initialize communication cpu_temperature
cpu = CPUTemperature()

comm = 'cpufreq-info -f -c 0'

# This function is called periodically from FuncAnimation
def animate(i, xtime, ytemp, yutil, yfreq):
    # Add x to lists
    xtime.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    
    #--------------------------------------------------------------------------
    # Read temperature (Celsius) from gpiozero
    temp=cpu.temperature
    ytemp.append(temp)

    # Limit x and y lists to 20 items
    xtime = xtime[-20:]
    ytemp = ytemp[-20:]

    # Draw x and y lists
    temp_plt.clear()
    temp_plt.plot(xtime, ytemp)
    
    # Format plot
    for label in temp_plt.get_xticklabels():
        label.set_rotation(40)
        label.set_horizontalalignment('right')
    temp_plt.set_title('Temperature Over Time')
    temp_plt.set_ylabel('Temperature (deg C)')
    
    #-------------------------------------------------------------------------- 
    cpu_usage = int(psutil.cpu_percent())

    # Add y to lists
    yutil.append(cpu_usage)

    # Limit x and y lists to 20 items
    yutil = yutil[-20:]

    # Draw x and y lists
    util_plt.clear()
    util_plt.plot(xtime, yutil)

    # Format plot
    for label in util_plt.get_xticklabels():
        label.set_rotation(40)
        label.set_horizontalalignment('right')
    util_plt.set_title('CPU Utilization Over Time')
    util_plt.set_ylabel('CPU Utilization (percentage)')
    
    #-------------------------------------------------------------------------- 
    cpu_freq_out = os.popen(comm)
    cpu_freq = int(cpu_freq_out.read())

    # Add y to lists
    yfreq.append(cpu_freq)

    # Limit x and y lists to 20 items
    yfreq = yfreq[-20:]

    # Draw x and y lists
    freq_plt.clear()
    freq_plt.plot(xtime, yfreq)

    # Format plot
    for label in freq_plt.get_xticklabels():
        label.set_rotation(40)
        label.set_horizontalalignment('right')
    freq_plt.set_title('CPU Frequency Over Time')
    freq_plt.set_ylabel('CPU frequency (MHz)')

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xtime, ytemp, yutil, yfreq), interval=5000)
plt.show()
