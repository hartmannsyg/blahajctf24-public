from scipy.io.wavfile import read
import numpy as np

def read_audio(file):
    sample_rate,data=read(file)
    return sample_rate,data

def calc_freq(signal_chunk,sample_rate):
    zero_crossing=np.where(np.diff(np.signbit(signal_chunk)))[0]
    num_crossing=len(zero_crossing)
    duration=len(signal_chunk)/sample_rate
    estimated_freq=num_crossing/(2*duration)
    return estimated_freq

sample_rate,modulated_wave=read_audio("hidden.wav")
sample_rate=44100
duration=0.01

bits=""

for i in range(0,len(modulated_wave),int(sample_rate*duration)):
    chunk=modulated_wave[i:i+441]
    detected_freq=calc_freq(chunk,sample_rate)
    if (detected_freq==float(950)):
        bits+="1"
    else:
        bits+="0"

data=''.join([chr(int(bits[i:i+8],2)) for i in range(0,len(bits),8)])
print(data)