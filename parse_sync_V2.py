import sys, os
import string
import time
import scipy
from scipy import signal as sc
import numpy as np

import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.use('MacOSX')
matplotlib.rcParams['backend.qt4']='PySide'

import pylab
import math
import csv

import matplotlib.pyplot as plt
#from matplotlib.pyplot import draw, show
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties


import PySide
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *
from PySide.QtUiTools import *

from multiprocessing import Process

import struct
from struct import *
import datetime
from datetime import datetime

################################################****************************###########################################


def twos_comp(val, bits):
    #"""compute the 2's compliment of int value val"""
    if( (val&(1<<(bits-1))) != 0 ):
      val = val - (1<<bits)
    return val


def convert_timestamp(times):
    import datetime

    values_utc = []
    times_utc = {}
    t = datetime.datetime(1900, 1, 1)

    for key, value in times.iteritems():
          if key not in times_utc: 
                 times_utc[key]=[]

                 for i in range(len(value)):
                        delta = datetime.timedelta(seconds=value[i])
                        t_utc = t + delta
                        times_utc[key].append(t_utc)

    print "TIME VALUE Of and Example Signal In UTC", times_utc['/Fungible1.1/1/LeftBase/A-B/COMP'][0]
    return times_utc

def smooth_data(times,signs):
    signs_new ={}

    for key,value in signs.iteritems():
          if key not in signs_new: 
                 
                 signs_new[key]=[]
                 for index, val in enumerate(value):
                        if (index < len(value)-1):
                               if (abs(value[index] - value[index-1])>=10 and abs(value[index+1] - value[index])>=10): 
                                      value[index] = value [index-1]
                               signs_new[key]=value               
    return (times, signs_new)

# #Define the Plot Function
# def draw_sensorplots(times, signals, plotmode):
#        plt.ion()
#        plot_array=[]
#        time_array=[]
#        legend_array=[]

#        #times = convert_timestamp(times) #convert the timestamps to UTC 

#        print "IN THE CONVERSION PROCESS", len(times['/Fungible1.1/1/LeftBase/A-B/COMP'])


#        if plotmode == "all":
#               #Plot all the sensor signals on one plot together
#               plt.figure(0)

#               for key in sorted(signals.iterkeys()):
#                      plot_array.append(signals[key])

#               for key in sorted(times.iterkeys()):
#                      time_array.append(times[key]) 

#               #print signals['/Fungible1.1/1/LeftBase/A-B/COMP']
#               print len(signals['/Fungible1.1/1/LeftBase/A-B/COMP'])
#               #print times['/Fungible1.1/1/LeftBase/A-B/COMP']
#               print len(times['/Fungible1.1/1/LeftBase/A-B/COMP'])

#               legend_array.append(signals.keys())
#               #print signals.keys()
#               #print "Number of Captured Signals", len(signals.keys( ))

#               for i in range(len(plot_array)):
#                      #x = np.arange(0,len(time_array[i]))
#                      p1 = plt.plot(time_array[i],plot_array[i])
              
#               ax = plt.subplot(111)
#               plt.title("All Plots")
#               plt.grid(b=None,which='major')
#               plt.ylabel(' Sensor Value From MapperRec')
#               plt.xlabel('Time ')

#               for label in ax.xaxis.get_ticklabels():
#                      label.set_rotation(55)
#                      label.set_fontsize(10) 



#               fontP = FontProperties()
#               fontP.set_size('small')
#               box = ax.get_position() 
#               ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9]) # Shink current axis's height by 10% on the bottom
#               #      l1 = ax.legend(legend_array, prop=fontP, ncol = 3, loc='upper center', bbox_to_anchor=(0.5, -0.1))

#        else: 
#               #Only plot the signal that's requested by the user
#               #print sig_times[0]
#               plt.figure()

#               for key, value in signals.iteritems():
#                      plot_array.append(signals[key])

#                      if key == plotmode: 
#                             print key
#                             #x = np.arange(0,len(signals[key]))
#                             p1 = plt.plot(times[key],signals[key])
#                             plot_name = "Plot for Signal: " + str(plotmode)
#                             plt.title(plot_name)
#                             plt.grid(b=None,which='major')
#                             plt.ylabel(' Sensor Value From MapperRec')
#                             plt.xlabel('Time (Seconds)')
#                             plt.ylim(min(signals[key])-10,max(signals[key])+10)
                            
#                             ax = plt.subplot(111)

#                             for label in ax.xaxis.get_ticklabels():
#                                    label.set_rotation(55)
#                                    label.set_fontsize(10) 
                            
#                             legend_array.append(key)
#                             box = ax.get_position()
#                             ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9]) # Shink current axis's height by 10% on the bottom
#                             ax.legend(legend_array, "upper right")
#        plt.draw()
# ##################################********************#######################

# print "Before moving to plots"

# # Plot all the signals
# #draw_sensorplots(sigtimes, signals,"all")

# # Plot only the signal for the given name 
# # for key, value in signals.iteritems():
# #        #print key
# #        draw_sensorplots(signals,key)

# # Plot the signals for the mapped signals (taken from the mapping json file "Fungible_EnergyForBallagumi_June222012_V2")
# draw_sensorplots(sigtimes, signals,'/Fungible1.1/2/Horizontal/2/COMP')
# #draw_sensorplots(sigtimes, signals,'/Fungible1.1/1/LeftWingBend/1/COMP')
# #draw_sensorplots(sigtimes, signals,'/Fungible1.1/3/RightWingBend/1/COMP')


# (sigtimes_sm, signals_sm) = smooth_data(sigtimes,signals)

# draw_sensorplots(sigtimes_sm, signals_sm,'/Fungible1.1/2/Horizontal/2/COMP')


# # Make sure that the drawn plots don't close at the end
# raw_input("Press Enter to Exit")
# plt.close('all')

# # shows the plots and keeps program running as long as plot is open 
# #plt.show()

class mapperData():

    def __init__(self):

      self.signals={} # A dict keeping count of the signal values for each signal
      self.sigtimes={} # A dict keeping count of the timestamps for each signal
      self.signal_names=[]
      self.signal_values=[]
      self.timestamps_seconds = []
      self.duration_seconds = []
      self.filename = ""

    def changeToDuration(self):

      for t in self.timestamps_seconds:
            delta = int(t) - int(timestamps[0])
            self.duration_seconds.append(delta)

    def parseData(self):
      try: 
        if len(self.filename) > 2: 
          datafile = open(self.filename,'U')
          data_line = csv.reader(datafile, dialect='excel')

          for line in data_line:

                 line = str(line)
                 line = line.replace("']","")
                 line = line.replace("['","")
                 line = line.strip()

                 #Get Values from Line
                 line_sections = line.split(" ")
                 signal_names.append(line_sections[2])
                 signal_values.append(int(line_sections[5]))
                 signal_timestamps_seconds.append(int(line_sections[0]))

          self.duration_seconds = changeToDuration(self.timestamps_seconds)
          # print "ONE Example of a Signal Name and Value"
          # print signal_names[0]
          # print signal_timestamps_seconds[0]
          # print signal_values[0]
          # print signal_duration_seconds[0]

          print len(signal_names), " ", len(signal_values), " ", len(signal_timestamps_seconds), " ", len(signal_duration_seconds)


          for i, sig in enumerate(signal_names):

                 current_name = signal_names[i]
                 current_val = signal_values[i]
                 current_time = signal_duration_seconds[i]

                 # Modify the sensor data before feeding them to the dictionary
                 current_val = twos_comp(current_val,8)

                 if current_name not in signals:
                        signals[current_name] = []
                        signals[current_name].append(current_val)

                        sigtimes[current_name] = []
                        sigtimes[current_name].append(current_time)
                 else:
                        signals[current_name].append(current_val)
                        sigtimes[current_name].append(current_time)

          print len(signals['/Fungible1.1/1/LeftBase/A-B/COMP'])
          print len(sigtimes['/Fungible1.1/1/LeftBase/A-B/COMP'])

      except: 
        print "Exception, Filename not found"



class SensorView(QWidget):

    def __init__(self):
        super(SensorView, self).__init__()

        self.currentData = mapperData()

        self.initUI()

    def initUI(self):

      self.button = QPushButton("Display Plots")
      self.button.setGeometry(10,10,400,30)
      self.button.setParent(self)
      self.button.clicked.connect(self.plotQSignal)

      # self.audioPanel = QFrame()
      # self.audioPanel.setGeometry(0,0,400,200)

      # self.sensorPanel = QFrame()
      # self.sensorPanel.setGeometry(0,0,400,200)

      # self.audioScene = QGraphicsScene()
      # self.audioView = QGraphicsView(self.audioScene,self.audioPanel)
      # self.audioView.setSceneRect(0,0,self.audioPanel.width(),self.audioPanel.height())

      # self.sensorScene =  QGraphicsScene()
      # self.sensorView = QGraphicsView(self.sensorScene,self.sensorPanel)
      # self.sensorView.setSceneRect(0,0,self.sensorPanel.width(),self.sensorPanel.height())

      # self.painter = QPainter(self)
      # self.pen = QPen(Qt.red, 1, Qt.DashDotLine, Qt.RoundCap, Qt.RoundJoin)
      # self.audioScene.addLine(0,0,self.audioPanel.width(),self.audioPanel.height(),self.pen)

      # hbox = QVBoxLayout()
      # hbox.addWidget(self.button)
      # hbox.addWidget(self.audioPanel)
      # hbox.addWidget(self.sensorPanel)
      # hbox.setAlignment(self,Qt.AlignHCenter)
      # hbox.setSpacing(10)

      # self.setLayout(hbox)
      self.setGeometry(500,300,500,500)
      self.setWindowTitle('Ballagumi Data Sync')
      self.show()

    def plotQSignal(self):

      self.plotWindow = QMainWindow()
      self.plotWindow.resize(600,600)

      # generate the plot
      fig = Figure(figsize=(500,400), dpi=72, facecolor=(1,1,1), edgecolor=(0,0,0))

      # subplot 1 - Audio Data Stream
      ax1 = fig.add_subplot(211)
      ax1.plot([0,1])
      ax1.set_xlabel('Time (Seconds)')
      ax1.set_ylabel('Audio Data from Synth')
      ax1.grid(b=None,which='major')

      # subplot 2 - Sensor Data Stream
      ax2 = fig.add_subplot(212)
      ax2.plot([0,1],'r')
      ax2.set_xlabel('Time (Seconds)')
      ax2.set_ylabel('Sensor Data from Ballagumi')
      ax2.grid(b=None,which='major')
      
      self.canvas = FigureCanvas(fig)

      self.plotWindow.setCentralWidget(self.canvas)
      self.plotWindow.show()

######### END OF QWIDGET CLASS - ON TO MAIN ##########

def main():

    app = QApplication(sys.argv)
    ex = SensorView()

    if len(sys.argv) == 2:

      ex.currentData.filename = sys.argv[1]
      print ex.currentData.filename
    
    else:

      print "Error, mapperRec File Not Included"
      sys.exit()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()











