#import libraries
import numpy as np
import matplotlib.pyplot as plt

#geberate analog signal

A = 1            #Amplitude of message signal
f = 1000         #frequency
phi = 0          #phase shift
start = 0        #start time
end = 0.1        #stop time
t = np.linspace(start, end, f*100)

y = A*np.cos(2*np.pi*f*t+phi)

plt.plot(t[0:1000],y[0:1000])
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.title("Message signal")
plt.tight_layout()
plt.grid(True)
plt.show()

#convert analog signal to digital by using any technique
#sample (using ideal sampling)
ts = t[::50]
ysamp = y[::50]
plt.stem(ts[0:21],ysamp[0:21], basefmt=" ")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.title("Sampled signal (Ideal Sampling)")
plt.tight_layout()
plt.grid(True)
plt.show()

#quantize
ys=ysamp.copy()
ys[(ys<=1) & (ys>0.875)] = 1
ys[(ys<=0.875) & (ys>0.625)] = 0.75
ys[(ys<=0.625) & (ys>0.375)] = 0.5
ys[(ys<=0.375) & (ys>0.125)] = 0.25
ys[(ys<=0.125) & (ys>-0.125)] = 0
ys[(ys<=-0.125) & (ys>-0.375)] = -0.25
ys[(ys<=-0.375) & (ys>-0.625)] = -0.5
ys[(ys<=-0.625) & (ys>-0.875)] = -0.75
ys[(ys<=-0.875) & (ys>=-1)] = -1
plt.stem(ts[0:21],ys[0:21], basefmt=" ")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.title("Quantized signal")
plt.tight_layout()
plt.grid(True)
plt.show()

#convert to digital
ydig = ys.copy()
ydig[ydig==1] = 0b1000
ydig[ydig==0.75] = 0b0111
ydig[ydig==0.5] = 0b0110
ydig[ydig==0.25] = 0b0101
ydig[ydig==0] = 0b0100
ydig[ydig==-0.25] = 0b0011
ydig[ydig==-0.5] = 0b0010
ydig[ydig==-0.75] = 0b0001
ydig[ydig==-1] = 0b0000
bitstream = [int(b) for x in ydig.astype(int) for b in format(x, '04b')]

Ts = ts[1] - ts[0]     # sampling period
bits_per_sample = 4
Tb = Ts / bits_per_sample   # bit duration
bits = np.array(bitstream)
t_nrz = np.repeat(np.arange(len(bits)) * Tb, 2)
B = 1   # NRZ amplitude for bit '1'
nrz = B * np.repeat(bits, 2)
plt.step(t_nrz[0:160], nrz[0:160], where='post')
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("NRZ Unipolar Line Coding")
plt.ylim(-0.2, A + 0.2)
plt.grid(True)
plt.tight_layout()
plt.show()

#modulate the digital signal
Ac = 1            #Amplitude of message signal
fc = 200000         #frequency
tc = np.linspace(start, end, fc*100)
nrz2 = np.repeat(nrz,(len(tc)/len(t_nrz)))
mod = nrz2*Ac*np.cos(2*np.pi*fc*tc+phi)
plt.plot(tc[0:200000],mod[0:200000])
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.title("Modulated signal (BASK)")
plt.tight_layout()
plt.grid(True)
plt.show()

#demodulate
modsqr = mod**2
# plt.plot(tc[0:120000],modsqr[0:120000])
# plt.xlabel("Time")
# plt.ylabel("Amplitude")
# plt.title("Square of the Modulated signal (BASK)")
# plt.tight_layout()
# plt.grid(True)
# plt.show()
modenv = modsqr.copy()
modenv[modenv!=0] = 1;

mod_samp = modenv[::1250]
tc_samp = tc[::1250]

plt.plot(tc[0:200000],modsqr[0:200000], color = "#fac75a")
plt.step(tc_samp[0:160], mod_samp[0:160], where='post',color = "red")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Envelope of square of received signal")
plt.ylim(-0.2, A + 0.2)
plt.grid(True)
plt.tight_layout()
plt.show()

plt.step(tc_samp[0:160], mod_samp[0:160], where='post')
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Envelope")
plt.ylim(-0.2, A + 0.2)
plt.grid(True)
plt.tight_layout()
plt.show()

de_bits = mod_samp[::2]
de_t = tc_samp[::2]
de_bits = [int(b) for b in de_bits]

binary_literals = [
    ''.join(map(str, de_bits[i:i+4]))
    for i in range(0, len(de_bits), 4)
]


de_val = np.array(binary_literals, dtype=object)
de_val[de_val=='1000'] = 1
de_val[de_val=='0111'] = 0.75
de_val[de_val=='0110'] = 0.5
de_val[de_val=='0101'] = 0.25
de_val[de_val=='0100'] = 0
de_val[de_val=='0011'] = -0.25
de_val[de_val=='0010'] = -0.5
de_val[de_val=='0001'] = -0.75
de_val[de_val=='0000'] = -1

de_val = de_val.astype(float)

plt.stem(ts[0:21],de_val[0:21], basefmt=" ", label = "Samples")
plt.plot(ts[0:21],de_val[0:21], color = "red", ls = "dashed", label = "Envelope")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.title("Demodulated Samples")
plt.tight_layout()
plt.grid(True)
plt.legend()
plt.show()

#Comparision
plt.plot(ts[0:21],de_val[0:21],color = "red", label = "Demodulated")
plt.plot(t[0:1000],y[0:1000], label = "Message")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.title("Comparision")
plt.tight_layout()
plt.grid(True)
plt.legend()
plt.show()
