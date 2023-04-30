
import sys
# from termios import FF0
from tkinter.tix import Tree
from turtle import title
from PySide6.QtWidgets import QApplication
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
import numpy as np

from pickle import FALSE
from pickletools import uint8
from statistics import mode
import serial, time
import numpy as np
from ctypes import sizeof
import pyaudio
import random


import audioProcessing as aP
import cmdManager as cmdM

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 48000
CHUNK = 2048
dev_index = 3 #for audio cable
# dev_index = 1 #microphone
#RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file.wav"
  
audio = pyaudio.PyAudio()

musicProcessor = aP.AudioProcessor(CHUNK, RATE)

cmdManager = cmdM.cmdManager()



stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True, input_device_index = dev_index,
                frames_per_buffer=CHUNK)
print ("Audio stream starting...")





uiclass, baseclass = pg.Qt.loadUiType("C:/IOT_LEDS_PROD/VisuaLED/GUI/MusicGui.ui")

class MainWindow(uiclass, baseclass):
    
    arduino = serial
    serialEN = True


    def __init__(self):
        super().__init__()
        self.setupUi(self)
        pg.setConfigOptions(antialias = True)
        self.BrightnessSlider.valueChanged.connect(cmdManager.setBrightness)
        self.BrightnessSlider.valueChanged.connect(self.updateBrightnessLabel)

        self.MotorSlider.valueChanged.connect(cmdManager.setPosition)
        self.MotorSlider.valueChanged.connect(self.updateMotorAngLabel)


        self.myplot = self.Plotwidget
        self.myCurve = self.myplot.plot(pen = 'y')
        self.data = np.random.normal(size=(10,1000))
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        # self.timer.start(0.010)
        self.timer.start(0.001)

        if self.serialEN:
            self.arduino = serial.Serial('COM4', 115200, timeout=.1)
            time.sleep(0.00) #give the connection a second to settle

    def updateBrightnessLabel(self, val):
        self.BrightnessVal.setText(str(val))
        return
    def updateMotorAngLabel(self, val):
        self.motorPosLabel.setText(str(val))
        return

    def updatePlot(self, frequencies, fourierTransform, timeDomainData):

        graphMode = self.GraphMode.value()
        if graphMode == 0:

            self.myCurve.setData(frequencies, fourierTransform, fillLevel=-0.3, brush=(50,50,200,100))

            self.myplot.disableAutoRange()
            self.myplot.setYRange(0,1090000, padding = 0)

            self.myplot.setLogMode(True, False)
            self.myplot.setXRange(np.log(RATE/CHUNK)/np.log(10), np.log(RATE/2)/np.log(10), padding = 0)

            self.myplot.setLimits(yMin = 0, yMax = 300000)
            
        if graphMode == 1:
            self.myplot.setLogMode(False, False)
            self.myCurve.setData(np.arange(0,CHUNK), timeDomainData, fillLevel=-0.3, brush=(50,50,200,100))

            self.myplot.disableAutoRange()
            self.myplot.setYRange(-40000,40000, padding = 0)
            self.myplot.setXRange(0, CHUNK, padding = 0)

            self.myplot.setLimits(yMin = -40000, yMax = 40000)


        return

    def update(self):


        
        data = stream.read(CHUNK, 0)
        numpydata = np.frombuffer(data, dtype=np.int16)
        numpyFrames = np.stack((numpydata[::2], numpydata[1::2]), axis=0)  # channels on separate axes

        (fourierTransform, frequencies) = musicProcessor.fftMyMusic(numpyFrames[0,:])
        musicProcessor.mapBinsFFT(fourierTransform, frequencies, None)
        musicProcessor.finalAdjustments()
        self.updatePlot(frequencies, fourierTransform, numpyFrames[0,:])
        # print(self.enableAmpCtlr.isChecked())
        # print(self.BrightnessSlider.value())
        if self.enableAmpCtlr.isChecked() and self.mode.value() == 2:
            cmdManager.setBrightness(musicProcessor.freqBins[0])
            cmdManager.cmdValues[2] = 120
            cmdManager.setMode(1)
        elif self.enableAmpCtlr.isChecked() and self.mode.value() == 3:
            cmdManager.setMode(1) 
            cmdManager.cmdValues[2] = musicProcessor.freqBins[0]
        else:
            cmdManager.cmdValues[2] = 120
            cmdManager.setMode(self.mode.value())
        
        # cmdManager.setMode(self.mode.value())

        if musicProcessor.threshFlag:
            cmdManager.cmdValues[7] = random.randrange(255)
            musicProcessor.threshFlag = False
        elif self.fadeEN.isChecked():
            cmdManager.incrementHue(1)

        if self.serialEN:
            cmdSerial = cmdManager.prepareCMD()
            self.arduino.write(cmdSerial.encode())
            # print(f0)
            data = self.arduino.readline()
        

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
