'''
Example of the use of the class Gammatone available in the library. It implements a fitlerbank of IIR gammatone filters as 
described  in Slaney, M., 1993, "An Efficient Implementation of the Patterson-Holdsworth  Auditory Filter Bank". Apple Computer Technical Report #35. 
In this example, a white noise is filtered by a gammatone filterbank and the resulting cochleogram is plotted.
'''
from brian import *
set_global_preferences(usenewbrianhears=True,
                       useweave=True,use_gpu = False)
from brian.hears import *


dBlevel=50*dB  # dB level of the input sound in rms dB SPL
sound=whitenoise(100*ms,samplerate=44*kHz).ramp() #generation of a white noise
sound=sound.atlevel(dBlevel) #set the sound to a certain dB level


nbr_center_frequencies=50
b1=1.019  #factor determining the time constant of the filters
center_frequencies=erbspace(100*Hz,1000*Hz, nbr_center_frequencies)  #center frequencies with a spacing following an ERB scale
gammatone =Gammatone(sound,center_frequencies,b=b1 ) #instantiation of the filterbank

gt_mon=gammatone.buffer_fetch(0, len(sound)) #processing


figure()
imshow(flipud(gt_mon.T),aspect='auto')    
show()




    