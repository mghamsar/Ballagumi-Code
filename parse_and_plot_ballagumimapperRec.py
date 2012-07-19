import sys
import os
import string
import time
import scipy
from scipy import signal as sc
import numpy as np
import matplotlib
matplotlib.use('MacOSX')
from matplotlib.font_manager import FontProperties

import matplotlib.pyplot as plt
from matplotlib.pyplot import draw, show
import pylab
import math
import csv

from multiprocessing import Process

################################################****************************###########################################


def modulo_sensorvalue(sensorval):
       sensorval = sensorval % 255
       #print "DIfferential Sensor Modified Values:", sensorval
       if (sensorval >= 128 and sensorval < 130):
              sensorval = sensorval % 128                                                        
              #print "Single Ended SENSOR Modified Values", sensorval
       return sensorval

def twos_comp(val, bits):
    #"""compute the 2's compliment of int value val"""
    if( (val&(1<<(bits-1))) != 0 ):
        val = val - (1<<bits)
    return val

def convert_timestamp(times):
       for key, value in times.iteritems():
              print "TIME VALUES IN NTP"
              print value[0]



#Define the Plot Function
def draw_sensorplots(times, signals, plotmode):
       plt.ion()
       plot_array=[]
       legend_array=[]

       if plotmode == "all":
              #Plot all the sensor signals on one plot together
              plt.figure(0)

              for key, value in signals.iteritems():
                     #print 'Length of each signal', len(signals[key])
                     plot_array.append(signals[key])
              legend_array.append(signals.keys())
              print signals.keys()
              print "Number of Captured Signals", len(signals.keys( ))

              for i in range(len(plot_array)):
                     x = np.arange(0,len(plot_array[i]))
                     p1 = plt.plot(x,plot_array[i])
              
              ax = plt.subplot(111)
              plt.title("All Plots")
              plt.grid(b=None,which='major')
              plt.ylabel(' Sensor Value From MapperRec')
              plt.xlabel('Number of Samples')
              fontP = FontProperties()
              fontP.set_size('small')
              box = ax.get_position() 
              ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9]) # Shink current axis's height by 10% on the bottom
              l1 = ax.legend(legend_array, prop=fontP, ncol = 3, loc='upper center', bbox_to_anchor=(0.5, -0.1))

       else: 
              #Only plot the signal that's requested by the user
              plt.figure()
              sig_times = convert_timestamp(times)

              for key, value in signals.iteritems():
                     plot_array.append(signals[key])

                     if key == plotmode: 
                            print key
                            x = np.arange(0,len(signals[key]))
                            p1 = plt.plot(x,signals[key])
                            plot_name = "Plot for Signal: " + str(plotmode)
                            plt.title(plot_name)
                            plt.grid(b=None,which='major')
                            plt.ylabel(' Sensor Value From MapperRec')
                            plt.xlabel('Number of Samples')
                            plt.ylim(min(signals[key])-10,max(signals[key])+10)

                            ax = plt.subplot(111)
                            legend_array.append(key)
                            box = ax.get_position()
                            ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9]) # Shink current axis's height by 10% on the bottom
                            ax.legend(legend_array, "upper right")
       plt.draw()


##################################********************#######################

filename = sys.argv[1]
datafile = open(filename,'U')
data_line = csv.reader(datafile, dialect='excel')

signals={} # A dict keeping count of the signal values for each signal
sigtimes={} # A dict keeping count of the timestamps for each signal
signal_names=[]
signal_values=[]
signal_timestamps_seconds=[]

for line in data_line:

       line = str(line)
       line = line.replace("']","")
       line = line.replace("['","")
       line = line.strip()
       #print line

       #Spliting the Line Now
       line_sections = line.split(" ")
       signal_names.append(line_sections[2])
       signal_values.append(int(line_sections[5]))
       signal_timestamps_seconds.append(int(line_sections[0]))

print "ONE Example of a Signal Name and Value"
print signal_names[302714]
print signal_values[302714]
print signal_timestamps_seconds[302714]

print len(signal_names), " ", len(signal_values), " ", len(signal_timestamps_seconds)


for i, sig in enumerate(signal_names):

       current_name = signal_names[i]
       current_val = signal_values[i]
       current_time = signal_timestamps_seconds[i]

       # Modify the sensor data before feeding them to the dictionary
       current_val = twos_comp(current_val,8)

       if current_name not in signals:
              signals[current_name] = []
              signals[current_name].append(current_val)
              #print current_name, signals[current_name]
              sigtimes[current_name] = []
              sigtimes[current_name].append(current_time)
       else:
              signals[current_name].append(current_val)
              sigtimes[current_name].append(current_time)

# Print a given key & value pair to make sure it's collecting the right values 
# for key, value in signals.iteritems() :
#        if key == signal_names[0]:
#               #print key, value
#               continue

# Plot all the signals
draw_sensorplots(sigtimes, signals,"all")

# Plot only the signal for the given name 
# for key, value in signals.iteritems():
#        #print key
#        draw_sensorplots(signals,key)

# Plot the signals for the mapped signals (taken from the mapping json file "Fungible_EnergyForBallagumi_June222012_V2")
draw_sensorplots(sigtimes, signals,'/Fungible1.1/2/Horizontal/2/COMP')
draw_sensorplots(sigtimes, signals,'/Fungible1.1/1/LeftWingBend/1/COMP')
draw_sensorplots(sigtimes, signals,'/Fungible1.1/3/RightWingBend/1/COMP')

# Make sure that the drawn plots don't close at the end
raw_input("Press Enter to Exit")
plt.close('all')

# shows the plots and keeps program running as long as plot is open 
#plt.show()













