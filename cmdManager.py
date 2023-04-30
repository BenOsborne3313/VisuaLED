import collections
import numpy as np


class cmdManager:

    def __init__(self):

        #all vals  8bit int.
        self.cmdValues = [0, 0, 255, 255, 255, 255, 255, 180, 100]

    def setMode(self, mode):
        self.cmdValues[0] = mode
        return
    
    def setPosition(self, position):
        self.cmdValues[1] = int(position*180/100)
        print(f"Motor Angle: {self.cmdValues[1]}")
        return

    def setFrequency(self, freqVec):
    
        if(len(freqVec) == len(self.freqVec)):
            self.cmdValues[2:7]

    def setFrequency(self, freq, bin):
        self.cmdValues[2+bin] = freq
    
    def setHue(self, hue):
        self.cmdValues[7] = hue
        return

    def incrementHue(self, inc):
        self.cmdValues[7] = self.cmdValues[7]+inc
        while (self.cmdValues[7]>255):
            self.cmdValues[7] = self.cmdValues[7]-255

        return

    def setBrightness(self, brightness):

        brightness = abs(brightness)
        brightness = int(brightness*255/100)
        if (brightness > 255):
            brightness = 255
        self.cmdValues[8] = brightness
        return

    def prepareCMD(self):

        cmdString = "<"
        for i in range(0, 8):
            cmdString = cmdString + str(int(self.cmdValues[i]))
            cmdString = cmdString  + ", "

        cmdString = cmdString + str(self.cmdValues[8])
        cmdString = cmdString + ">"
        return cmdString

    

    
