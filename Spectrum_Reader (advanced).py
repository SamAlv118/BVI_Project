import wave
from PIL import Image
import numpy as np

samplingrate = 44100 # default for computer audio files
duration = 5 # in seconds
lowerF, upperF = 428274940, 999308193.333333  # Lower and Upper bounds of the spectrum converted into frequencies
                                               # 300-700 nm wavelengths -> 428274940-999308193.333333 MHz frequencies


#This section is about reading in the spectrum image and finding the absorption lines
wavelengths = np.arange(300, 700, 1)
img = Image.open('gradient.png')
pixels = img.load()
px = 0

for x in range(img.width):
    r, g, b = pixels[x, 0]                #this is reading each pixel's RGB values, we want to find and store each black pixel as a 0
    if r == 0 and g == 0 and b == 0:
        wavelengths[px] = 0               
    px += 1

img.close()

#these are just functions to help the process along

def NmToHz(ar):
    for i in range(len(ar)):
        if ar[i] == 0:
            pass
        else:
            ar[i] = (299792458000/ar[i])/(10**6) - 300
    return ar

def ZeroToFreqIndex(ar):
    zeros = []
    for i in range(len(ar)):
        if ar[i] == 0:
            zeros.append(i * 551)    #multiply by 551 because each pixel gets exactly 551 samples in the audio file, thats 44100*5/400 -> samplingrate * duration / pixels
    return zeros

zeros = ZeroToFreqIndex(wavelengths)


# These frequencies are inaudible to humans, so we will divide by 10^6 
# and subtract by 300 to get these in an audible range.
# Tweak this formula as needed

lowerF = (lowerF / 10**6) - 300   # 128.27 Hz for 300nm
upperF = (upperF / 10**6) - 300   # 699.3 Hz for 700nm

time = np.linspace(0, duration, (samplingrate * duration), endpoint = False)

# we need to create a sinusoidal wave function for the pitch
# the wave function will look like y = Asin(2*pi*f*t). notice though that the frequency is a function of time
# so actually, the function should have some sort of "acceleration" and thus, in strictly the time domain,
# y = Asin(2*pi*t^2) is a rough approximation, check ipad notes for further explanation to derive expression below
phase = 2 * np.pi * (lowerF * time + (upperF - lowerF) / (2 * duration) * (time**2)) 
sine_wave = np.flip(np.sin(phase))


#this is going to locate the zeros in the wavelengths and mute the audio where each zero is located
#it is important to measure from the start of the mute, that should be the exact wavelength that is missing
for x in range(len(zeros)):
    for y in range(4000):                 #this extends the mute artificially so you can hear the audio stop. remember, this audio has a refresh rate of 44100 per second, if only 1 sample is taken out, you wont hear that
        if x+y < len(sine_wave):
            sine_wave[zeros[x] + y] = 0

#---------------------CALCULATION TUTORIAL---------------------
#To calculate wavelengths audibly, use a stopwatch beginning with the audio file, recording each stoppage time
#example using 656 hydrogen line.
#if you hear the audio stop at 4.5 seconds, you multiply this by the samplingrate to get the total number of frames that have passed since the beginning of the audio file
#you then divide by 551 which is the number of sampling frames given to each pixel in the spectrum (220500 frames/400 pixels)
#then add 300 to account for the fact that your number starts from 0 but the spectrum is actually shifted and starts at 300 nm
#---------------------------------------------------------------

one_channel = (sine_wave * 32767).astype(np.int16) #this converts each output from the sine wave into a 16-bit integer that can be read as audio

#the mono samples array is parameterizing the motion of the speaker cone. at +32767, the cone is fully engaged,
#at 0, the cone is neutral, and at -32767, the cone is fully retracted. as the sine wave's phase shortens with time,
#there will be less integers between the peaks of +32767, resulting in a shorter time between peaks due to the computer's
#sampling rate being constant.

#for exact numbers, at 700 Hz with a 44100 sampling rate, 44100/700 = 63 integers per full cycle
#and at 128 Hz, 44100/128 = ~344 integers per full cycle
#this "skipping" makes a higher pitch to the human ear 

# Duplicate the mono sample into a 2d matrix where each row is a timestep - take for example the frequencies. [128.27, 128.27] would be the first row which means at t=0, it plays the frequency 128.27 Hz
two_channel = np.column_stack((one_channel, one_channel)).flatten() #flatten turns this back into a 1d array that reads the same as outlined above
#the purpose of this is to mimic the sound from the left speaker to the right speaker,
#not super important but it would only produce sound in the left ear without this line if you're wearing headphones


# creating a wave file
with wave.open('test.wav', 'wb') as f:
    f.setparams((2, 2, samplingrate, 0, 'NONE', 'not compressed')) # default is (nchannels=2, sampwidth=2, framerate=44100, nframes=0, comptype='NONE', compname='not compressed')
    f.writeframes(two_channel.tobytes())

f.close()
