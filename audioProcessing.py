import numpy as np
"""Contains helper functions for processing audio

-FFT

"""

class AudioProcessor:

    
    def __init__(self, CHUNK, RATE, maxVal = 160000, NBinsEnc = 5):
        """
        Constructor

        :param self: audioProcessing object
        :param CHUNK: N samples
        :param RATE: sampling rate in Hz
        :param maxVal: maximum value
        :param NBinsEnc: Number of bins for lossy encoding

        """
        self.CHUNK = CHUNK
        self.RATE = RATE
        self.hanningWindow = np.hanning(self.CHUNK)
        self.freqBins = np.zeros(NBinsEnc)
        self.prevFreqBins = np.zeros(NBinsEnc)
        self.maxVal = maxVal
        self.threshFlag = False

    def fftMyMusic(self, data):
        """
        Performes FFT of music data. Computes Frequency Vector

        :param data: audio data
        :returns (fourierTransform1, frequencies): touple of fourier transform data and frequency bin data.

        """
        
        windowedData = self.hanningWindow*data

        fourierTransform = np.fft.fft(windowedData,axis = 0)          # Normalize amplitude
        fourierTransform = abs(fourierTransform)/len(fourierTransform)
        fourierTransform1= 2*abs(fourierTransform[range(int(len(data)/2))]) # Exclude sampling frequenc

        values      = np.arange(len(fourierTransform1))

        frequencies = (values+1)*(self.RATE/2)/len(fourierTransform1)

        fourierTransform1 = fourierTransform1*fourierTransform1*(frequencies)/((self.RATE/2))

        return (fourierTransform1, frequencies)


    def mapBinsFFT(self, fourierTransform, frequencies, frequencyRanges):
        """
        condenses frequency information into length(frequencyRanges) number of bins by taking tha max values in specified ranges

        :param: fourierTransform: FT data. Frequency domain
        :param: frequencies: Frequencies of FFT bins.
        :param: frequencyRanges: array of tuples specifying frequency ranges.
        """
        # freqBinI_end = next(x for x, val in enumerate(frequencies) if val > 40)
        # freqBinI_start = next(x for x, val in enumerate(frequencies) if val > 10)
        freqBinI_end = 4
        freqBinI_start = 1
        freRangeInterest = fourierTransform[freqBinI_start:freqBinI_end+1]
        

        self.freqBins[0] = np.amax(freRangeInterest)
        return

    def finalAdjustments(self):
        """TODO replace with proper implementation"""
        
        if self.freqBins[0] > self.maxVal:
            self.freqBins[0] = self.maxVal
        self.freqBins[0] = int(self.freqBins[0]*130/self.maxVal)
        if (self.freqBins[0] < 5):
            self.freqBins[0] = 5

        self.freqBins[0] = self.freqBins[0]-5



        if(self.freqBins[0] < self.prevFreqBins[0]-15):
            self.freqBins[0] = self.prevFreqBins[0] - 15

        if (self.freqBins[0] > 30 and self.prevFreqBins[0] < 30) :
            print("YEEEET")
            self.threshFlag = True
        self.prevFreqBins[0] = self.freqBins[0]
        # print("B0: " + str(self.freqBins[0]) + " P0: " + str(self.prevFreqBins[0]))
        
        return
    