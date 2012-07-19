import sys
import os
import serial
import string
import time
import scipy
from scipy import signal as sc
import numpy as np
import matplotlib
matplotlib.use('MacOSX')
from matplotlib.font_manager import FontProperties

import matplotlib.pyplot as plt
import pylab
import math
import csv

signals = [   (1, '7S1', 'Horizontal', '1', 'ON'),
              (1, '0S1', 'LeftBase', 'A', 'ON'),
              (1, '1S1', 'LeftBase', 'B', 'ON'),
              (1, '2S1', 'LeftBase', 'C', 'ON'),
              (1, '0D1', 'LeftBase', 'A-B', 'ON'),
              (1, '1D1', 'LeftBase', 'A-C', 'ON'),
              (1, '3S1', 'LeftWingBend', '1', 'ON'),
              (1, '4S1', 'LeftWingBend', '2', 'ON'),
              (1, '5S1', 'LeftWingBend', '3', 'ON'),
              (1, '6S1', 'LeftWingBend', '4', 'ON'),

              (1, '7S0', 'Horizontal', '1', 'OFF'),
              (1, '0S0', 'LeftBase', 'A', 'OFF'),
              (1, '1S0', 'LeftBase', 'B', 'OFF'),
              (1, '2S0', 'LeftBase', 'C', 'OFF'),
              (1, '0D0', 'LeftBase', 'A-B', 'OFF'),
              (1, '1D0', 'LeftBase', 'A-C', 'OFF'),              
              (1, '3S0', 'LeftWingBend', '1', 'OFF'),
              (1, '4S0', 'LeftWingBend', '2', 'OFF'),
              (1, '5S0', 'LeftWingBend', '3', 'OFF'),
              (1, '6S0', 'LeftWingBend', '4', 'OFF'),

              (2, '0S1', 'LeftMid', 'A', 'ON'),
              (2, '1S1', 'LeftMid', 'B', 'ON'),
              (2, '2S1', 'LeftMid', 'C', 'ON'),
              (2, '3S1', 'LeftTip', 'A', 'ON'),
              (2, '4S1', 'LeftTip', 'B', 'ON'),
              (2, '5S1', 'Horizontal', '2', 'ON'),
              (2, '6S1', 'Horizontal', '3', 'ON'),
              (2, '7S1', 'Horizontal', '4', 'ON'),
              (2, '0D1', 'LeftMid', 'A-B', 'ON'),
              (2, '1D1', 'LeftMid', 'A-C', 'ON'),
              (2, '5D1', 'LeftTip', 'B-A', 'ON'),
              (2, '7D1', 'Horizontal_Bend', '3-4', 'ON'),

              (2, '0S0', 'LeftMid', 'A', 'OFF'),
              (2, '1S0', 'LeftMid', 'B', 'OFF'),
              (2, '2S0', 'LeftMid', 'C', 'OFF'),
              (2, '3S0', 'LeftTip', 'A', 'OFF'),
              (2, '4S0', 'LeftTip', 'B', 'OFF'),
              (2, '5S0', 'Horizontal', '2', 'OFF'),
              (2, '6S0', 'Horizontal', '3', 'OFF'),
              (2, '7S0', 'Horizontal', '4', 'OFF'),
              (2, '0D0', 'LeftMid', 'A-B', 'OFF'),
              (2, '1D0', 'LeftMid', 'A-C', 'OFF'),
              (2, '5D0', 'LeftTip', 'B-A', 'OFF'),
              (2, '7D0', 'Horizontal_Bend', '3-4', 'OFF'),

              (3, '0S1', 'RightBase', 'A', 'ON'),
              (3, '1S1', 'RightBase', 'B', 'ON'),
              (3, '2S1', 'RightBase', 'C', 'ON'),
              (3, '3S1', 'RightWingBend', '1', 'ON'),
              (3, '4S1', 'RightWingBend', '2', 'ON'),
              (3, '5S1', 'RightWingBend', '3', 'ON'),
              (3, '6S1', 'RightWingBend', '4', 'ON'),
              (3, '7S1', 'VerticalBend', '2', 'ON'),
              (3, '0D1', 'RightBase', 'A-B', 'ON'),
              (3, '1D1', 'RightBase', 'A-C', 'ON'),
              (3, '2D1', 'RightWingBend', '2-3', 'ON'),
              (3, '3D1', 'RightWingBend', '1-2', 'ON'),

              (3, '0S0', 'RightBase', 'A', 'OFF'),
              (3, '1S0', 'RightBase', 'B', 'OFF'),
              (3, '2S0', 'RightBase', 'C', 'OFF'),
              (3, '3S0', 'RightWingBend', '1', 'OFF'),
              (3, '4S0', 'RightWingBend', '2', 'OFF'),
              (3, '5S0', 'RightWingBend', '3', 'OFF'),
              (3, '6S0', 'RightWingBend', '4', 'OFF'),
              (3, '7S0', 'VerticalBend', '2', 'OFF'),
              (3, '0D0', 'RightBase', 'A-B', 'OFF'),
              (3, '1D0', 'RightBase', 'A-C', 'OFF'),
              (3, '2D0', 'RightWingBend', '2-3', 'OFF'),
              (3, '3D0', 'RightWingBend', '1-2', 'OFF'),

              (1, '0S2', 'LeftBase', 'A', 'COMP'),
              (1, '1S2', 'LeftBase', 'B', 'COMP'),
              (1, '2S2', 'LeftBase', 'C', 'COMP'),
              (1, '3S2', 'LeftWingBend', '1', 'COMP'),
              (1, '4S2', 'LeftWingBend', '2', 'COMP'),
              (1, '5S2', 'LeftWingBend', '3', 'COMP'),
              (1, '6S2', 'LeftWingBend', '4', 'COMP'),
              (1, '7S2', 'Horizontal', '1', 'COMP'),
              (1, '0D2', 'LeftBase', 'A-B', 'COMP'),
              (1, '1D2', 'LeftBase', 'A-C', 'COMP'),

              (2, '0S2', 'LeftMid', 'A', 'COMP'),
              (2, '1S2', 'LeftMid', 'B', 'COMP'),
              (2, '2S2', 'LeftMid', 'C', 'COMP'),
              (2, '3S2', 'LeftTip', 'A', 'COMP'),
              (2, '4S2', 'LeftTip', 'B', 'COMP'),
              (2, '5S2', 'Horizontal', '2', 'COMP'),
              (2, '6S2', 'Horizontal', '3', 'COMP'),
              (2, '7S2', 'Horizontal', '4', 'COMP'),
              (2, '0D2', 'LeftMid', 'A-B', 'COMP'),
              (2, '1D2', 'LeftMid', 'A-C', 'COMP'),
              (2, '5D2', 'LeftTip', 'B-A', 'COMP'),
              (2, '7D2', 'Horizontal_Bend', '3-4', 'COMP'),

              (3, '0S2', 'RightBase', 'A', 'COMP'),
              (3, '1S2', 'RightBase', 'B', 'COMP'),
              (3, '2S2', 'RightBase', 'C', 'COMP'),
              (3, '3S2', 'RightWingBend', '1', 'COMP'),
              (3, '4S2', 'RightWingBend', '2', 'COMP'),
              (3, '5S2', 'RightWingBend', '3', 'COMP'),
              (3, '6S2', 'RightWingBend', '4', 'COMP'),
              (3, '7S2', 'VerticalBend', '2', 'COMP'),
              (3, '0D2', 'RightBase', 'A-B', 'COMP'),
              (3, '1D2', 'RightBase', 'A-C', 'COMP'),
              (3, '2D2', 'RightWingBend', '2-3', 'COMP'),
              (3, '3D2', 'RightWingBend', '1-2', 'COMP')]


def smooth_values(listOFlist,N):

       g2 = []
       for i in range(len(listOFlist)):
              g2.append(float(listOFlist[i]))
       #print "ORIGINAL LIST", g2
       #print "CONVERTED SCIPY ARRAY", scipy.array(g2)
       return sc.medfilt(scipy.array(g2), kernel_size=N)


# Plot Block given the block number
def plot_gest(gest_num):
       gest_num = gest_num+1
       gest_array = []
       legend_array=[]

       fontP = FontProperties()
       fontP.set_size('small')

       Gest_block = 'Gesture%d' %gest_num
       print 'Length of Sensor Data Keys', len(sensordata.keys())

       for k in range(len(sensordata.keys())-10):
              thekey = signals[k]
              name = str(thekey[0]) +'/'+ thekey[2] + '/' + thekey[3] +'/'+ thekey[4]
              #print name
              #print Gest_block
              gest_array.append(sensordata[name][Gest_block])


       
       x = np.arange(0,len(gest_array[0]))
       print len(x)
       print len(gest_array)

       #ax1 = plt.subplot(111)
       #ax1 = plt.subplot(211)
       
       plt.figure(0)
       for i in range(len(gest_array)):
              p1 = plt.plot(x,gest_array[i])
       
       plt.title('Normalized Sensor Responses - Apex Pull')
       plt.ylabel('Normalized Sensor Value')
       plt.xlabel('Time(ms)')
       plt.grid(b=None,which='major')
       plt.xlim(0,len(x)+5)

       plt.figure(1)
       # Plot of smoothed data without glitches
       smooth_sigs=[]

       for i in range(len(gest_array)):
              smooth_sigs.append(smooth_values(gest_array[i],3))
              p2 = plt.plot(x,smooth_sigs[i],'-')
       plt.grid(b=None,which='major')
       plt.title("Smoothed Sensor Responses - Apex Pull")


       plt.figure(2)
       #ax2 = plt.subplot(111)
       min_thresh = 0.1
       for i in range(len(smooth_sigs)):
               #print "MAX", max(gest_array[i])
               #print "MIN", min(gest_array[i])
               if ((float(max(smooth_sigs[i])) - float(min(smooth_sigs[i])))>min_thresh and ((float(max(smooth_sigs[i])) - float(min(smooth_sigs[i])))<1.1)):
                      p3 = plt.plot(x,smooth_sigs[i],'-')
                      #plt.annotate(gest_array[i], y=(gest_array[i]))

                      legend_array.append(sensornames[i])
                      #print legend_array
               else:
                      continue
       plot_title = 'Refined Sensor Responses - Threshold '+ str(min_thresh)
       plt.title(plot_title)
       plt.ylabel('Normalized Sensor Value')
       plt.xlabel('Time(ms)')
       plt.grid(b=None,which='major')
       plt.ylim(0,1.4)
       ax = plt.subplot(111)
       # Shink current axis's height by 10% on the bottom
       box = ax.get_position()
       ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])



       l1 = ax.legend(legend_array, prop=fontP, ncol = 3, loc='upper center', bbox_to_anchor=(0.5, -0.1))


       




       plt.show()

############################### MAIN ####################################

filename = sys.argv[1]
line_block=[]

read_block = { (0,"learning", "ON"): 1, (1,"learning", "OFF"): 0}

datafile = open(filename,'U')
spamReader = csv.reader(datafile, dialect='excel')

runs = []
thisrun = []
for line in spamReader:
       if len(line) == 1:
              if len(thisrun) > 0:
                     runs.append(thisrun)
                     thisrun = []
       else:
              thisrun.append(line)
       #print line

sensordata = {}
sensornames = []

for i, element in enumerate(signals): #i for index using enumerate
       name = str(element[0]) +'/'+ element[2] + '/' + element[3] +'/'+ element[4]
       sensornames.append(name)

       if element[4]=="COMP":
              continue
       if name not in sensordata:
              sensordata[name] = {}
       for j, block in enumerate(runs):
              gesture_key='Gesture%d' % (j+1)

              singlesensor = []
              for row in block:
                     singlesensor.append(row[i])

              sensordata[name][gesture_key] = singlesensor


#plot gesture 1
plot_gest(1)















