from PIL import Image
import numpy as np
from scipy.io.wavfile import write


def text_to_binary():
    data_bytes=b""
    with open("blahaj_aaa.txt","rb") as f:
        data_bytes=f.read()
    return ''.join(format(a,'08b') for a in data_bytes)

def sine(frequency,duration,sample_rate=44100):
    t=np.linspace(0,duration,int(sample_rate*duration),endpoint=False)
    wave=0.5*np.sin(2*np.pi*frequency*t)
    return wave

def frequency_modulate(bin,base_freq=500,frq_step=500,duration=0.01,sample_rate=44100):
    modulated_wave=[]
    for bit in bin:
        print(bit)
        if bit=='1':
            freq=base_freq+frq_step
        else:
            freq=base_freq
        wave=sine(freq,duration,sample_rate)
        modulated_wave.extend(wave)
    return np.array(modulated_wave)


data=text_to_binary()
data_hidden=frequency_modulate(data)

print(data_hidden)

write('hidden.wav',44100,data_hidden.astype(np.float32))