import matplotlib.pyplot as plt
import numpy as np

import wavefunctions
from music_scale import generate_music_scale

sample_rate = 44100

args = (1, 1, sample_rate)

f = generate_music_scale()

t  = np.arange(sample_rate)
w1 = wavefunctions.sine_wave(f["C4"], *args)
w2 = wavefunctions.sine_wave(f["E4"], *args)
w3 = wavefunctions.sine_wave(f["G4"], *args)
w123 = w1 + w2 + w3

plt.figure()
plt.title("Wave Summation")
plt.plot(t, w1, ls = "--", label = r"C4 (${:.2f} Hz$)".format(f["C4"]))
plt.plot(t, w2, ls = "--", label = r"E4 (${:.2f} Hz$)".format(f["E4"]))
plt.plot(t, w3, ls = "--", label = r"G4 (${:.2f} Hz$)".format(f["G4"]))
plt.plot(t, w123, lw = 2, label = r"C Major Chord")
plt.xlim(0, f["G4"])
plt.xlabel(r"Time ($s$)")
plt.ylabel(r"Amplitude")
plt.legend()
plt.show()
