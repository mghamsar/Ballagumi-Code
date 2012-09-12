import sys, os
import string
import time
import struct
from struct import *
import datetime
from datetime import datetime
import scipy
from scipy import signal as sc
from scipy.io.wavfile import read, write
import numpy as np
from multiprocessing import Process

import PySide
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *
from PySide.QtUiTools import *

import pylab
import math
import csv

import matplotlib
matplotlib.rcParams['backend.qt4']='PySide'

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt

################################################****************************###########################################

class mapperData():

    def __init__(self):

      self.signals = {} # A dict keeping count of the signal values for each signal
      self.times = {} # A dict keeping count of the timestamps for each signal
      self.smoothsignals = {}
      self.signal_names = []
      self.signal_values = []
      self.timestamps_seconds = []
      self.duration_seconds = []
      self.filename = ""
      self.audio_filename = ""

    def changeToDuration(self):

      for t in self.timestamps_seconds:
            delta = int(t) - int(self.timestamps_seconds[0])
            self.duration_seconds.append(delta)

    def changeNTPToUTC(self,times):
      import datetime

      values_utc = []
      times_utc = {}
      t = datetime.datetime(1900, 1, 1)

      for key, value in self.times.iteritems():
            if key not in times_utc: 
                   times_utc[key]=[]

                   for i in range(len(value)):
                          delta = datetime.timedelta(seconds=value[i])
                          t_utc = t + delta
                          times_utc[key].append(t_utc)
      print "TIME VALUE Of and Example Signal In UTC", times_utc['/Fungible1.1/1/LeftBase/A-B/COMP'][0]
      return times_utc

    def getTwosComp(self,val, bits):
        #"""compute the 2's compliment of int value val"""
        if( (int(val) & (1<<(bits-1))) != 0 ):
          val = int(val) - (1<<bits)
        return val

    def parseAudioData(self):

      self.rate, self.audioInput = read(self.audio_filename)
      #self.audioInput = fromfile(open(self.audio_filename),int16)

      print 'Sampling Rate', self.rate, "   "#, self.audioInput

    def plotAudioData(self,subplot):

      p2_x = np.arange(0,len(self.audioInput))
      p2 = subplot.plot(p2_x,self.audioInput)
      subplot.set_xlabel('Time (Seconds)')
      subplot.set_ylabel('Audio Data from Synthesizer')
      subplot.grid(b=None,which='major')


    def parseData(self):
      
      if len(self.filename) >= 2:

        datafile = open(self.filename,'U')
        data_line = csv.reader(datafile, dialect='excel')

        for line in data_line:
          line = str(line)
          line = line.replace("']","")
          line = line.replace("['","")
          line = line.strip()

          #Get Values from Line
          line_sections = line.split(" ")
          self.signal_names.append(line_sections[2])
          self.signal_values.append(float(line_sections[5]))
          self.timestamps_seconds.append(int(line_sections[0]))

        self.changeToDuration()

        for i, sig in enumerate(self.signal_names):

           current_name = self.signal_names[i]
           current_val = self.signal_values[i]
           current_time = self.duration_seconds[i]

           # Modify the sensor data before feeding them to the dictionary
           current_val = self.getTwosComp(current_val,8)

           if current_name not in self.signals:
                  self.signals[current_name] = []
                  self.signals[current_name].append(current_val)

                  self.times[current_name] = []
                  self.times[current_name].append(current_time)
           else:
                  self.signals[current_name].append(current_val)
                  self.times[current_name].append(current_time)
      else: 
        print "Exception, Filename Not Available"
      
    # Plot all the sensor signals on one plot together
    def plot_allsensorsignals(self,subplot):
        
        plot_array=[]
        time_array=[]
        legend_array=[]

        for key in sorted(self.signals.iterkeys()):
               plot_array.append(self.signals[key])

        for key in sorted(self.times.iterkeys()):
               time_array.append(self.times[key]) 

        legend_array.append(self.signals.keys())

        for i in range(len(plot_array)):
              p1 = subplot.plot(time_array[i],plot_array[i])
              subplot.set_xlabel('Time (Seconds)')
              subplot.set_ylabel('Sensor Data from Ballagumi')
              subplot.grid(b=None,which='major')
        
        for label in subplot.xaxis.get_ticklabels():
               label.set_rotation(55)
               label.set_fontsize(10)

        fontP = FontProperties()
        fontP.set_size('small')
        box = subplot.get_position() 
        subplot.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9]) # Shink current axis's height by 10% on the bottom
        #l1 = subplot.legend(legend_array, prop=fontP, ncol = 3, loc='upper center', bbox_to_anchor=(0.5, -0.1))

    def plot_sensorsignal(self,subplot,signalname):
        
        plot_array=[]
        time_array=[]
        legend_array=[]
     
        for key, value in self.signals.iteritems():
          plot_array.append(self.signals[key])

          if key == signalname:

            print 'Found Key', key, 'Matching Signal Name', signalname
            p1 = subplot.plot(self.times[key],self.signals[key])
            plot_name = "Plot for Signal: " + str(signalname)
            subplot.set_xlabel('Time (Seconds)')
            subplot.set_ylabel('Audio Data from Synth')
            subplot.grid(b=None,which='major')

            for label in subplot.xaxis.get_ticklabels():
                   label.set_rotation(55)
                   label.set_fontsize(10) 

            legend_array.append(key)
            box = subplot.get_position()
            subplot.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9]) # Shink current axis's height by 10% on the bottom
            subplot.legend(legend_array, "upper right")

    def smooth_data(self):

        for key,value in self.signals.iteritems(): 
          if key not in self.smoothsignals:        
            self.smoothsignals[key]=[]

            for index, val in enumerate(value):
                if (index < len(value)-1):
                   if (abs(value[index] - value[index-1])>=10 and abs(value[index+1] - value[index])>=10): 
                          value[index] = value [index-1]
                   self.smoothsignals[key] = value

class SensorView(QWidget):

    def __init__(self):
        super(SensorView, self).__init__()
        self.currentData = mapperData()
        self.initUI()

    def initUI(self):

      self.button = QPushButton("Display Plots")
      self.button.setGeometry(10,50,400,30)
      self.button.setParent(self)
      self.button.clicked.connect(self.plotQSignal)

      self.signalComboBox = QComboBox()
      self.signalComboBox.setGeometry(10,10,400,30)
      self.signalComboBox.setParent(self)
      self.signalComboBox.activated.connect(self.getSignalName)

      # self.setLayout(hbox)
      self.setGeometry(500,300,450,350)
      self.setWindowTitle('Ballagumi Data Sync')
      self.show()
    
    def fillQBox(self): 
    # Add all the signal names from the device to the combobox
      if dict(self.currentData.signals):
        for name in self.currentData.signals.iterkeys():
          #print name
          self.signalComboBox.addItem(name)
      else:
        print "Empty Signals Dictionary"

    def getSignalName(self):
      print 'Selected Sensor Signal', self.signalComboBox.currentText()
      self.current_signal = self.signalComboBox.currentText()

    def plotQSignal(self):

      self.plotWindow = QMainWindow()
      self.plotWindow.resize(600,600)

      # generate the plot
      fig = Figure(figsize=(500,400), dpi=72, facecolor=(1,1,1), edgecolor=(0,0,0))

      # subplot 1 - Audio Data Stream
      ax1 = fig.add_subplot(211)
      self.currentData.plot_sensorsignal(ax1,self.current_signal)

      # subplot 2 - Sensor Data Stream
      ax2 = fig.add_subplot(212)
      self.currentData.plotAudioData(ax2)
      #self.currentData.plot_allsensorsignals(ax2)
      
      self.canvas = FigureCanvas(fig)

      self.plotWindow.setCentralWidget(self.canvas)
      self.plotWindow.show()

######### END OF QWIDGET CLASS - ON TO MAIN ##########

def main():

    app = QApplication(sys.argv)
    ex = SensorView()

    if len(sys.argv) == 3:

      ex.currentData.filename = sys.argv[1]
      ex.currentData.audio_filename = sys.argv[2]
      ex.currentData.parseData()
      ex.currentData.parseAudioData()
    
    elif len(sys.argv) == 2:
      
      ex.currentData.filename = sys.argv[1]
      ex.currentData.parseData()
      ex.currentData.audioInput = [0,1]
      #ex.currentData.parseAudioData()

    else:

      print "Error, mapperRec File Not Included"
      sys.exit()

    ex.fillQBox()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

# (times, signals_sm) = smooth_data(times,signals)











