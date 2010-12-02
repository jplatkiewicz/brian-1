from brian import *
set_global_preferences(usenewbrianhears=True,
                       useweave=True,use_gpu = False)
from brian.hears import *

from scipy.io import savemat
from time import time

dBlevel=50*dB  # dB level in rms dB SPL
sound=Sound.load('/home/bertrand/Data/Toolboxes/AIM2006-1.40/Sounds/aimmat.wav')

sound=sound.atlevel(dBlevel)


print 'fs=',sound.samplerate,'duration=',len(sound)/sound.samplerate

simulation_duration=len(sound)/sound.samplerate


nbr_center_frequencies=500
b1=1.019
#center_frequencies=erbspace(100*Hz, 1000*Hz, nbr_center_frequencies)
center_frequencies=log_space(100*Hz, 1000*Hz, nbr_center_frequencies)
gammatone =GammatoneFilterbank(sound,center_frequencies,b=b1 )


gammatone.buffer_init()
t1=time()
gt_mon=gammatone.buffer_fetch(0, len(sound))
print 'the simulation took',time()-t1,' seconds to run'


data=dict()
data['out']=gt_mon.T
savemat('/home/bertrand/Data/MatlabProg/AuditoryFilters/gT_slaney_BH.mat',data)

figure()
imshow(flipud(gt_mon.T),aspect='auto')    
show()




    