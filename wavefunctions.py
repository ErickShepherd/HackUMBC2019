"""

A module to generate audio wave signals

Module metadata:

    Author 01:      Erick Shepherd (ErickShepherd@UMBC.edu)
    Event:          HackUMBC Fall 2019
    Team:           Swan Song
    Date created:   2019-09-29
    Last updated:   2019-09-29

Summary:

    This module supplies a set of functions to produce arbitrary audio wave
    signals.

"""

# Third party imports.
import numpy as np

# Dunder definitions.
__author__  = ["Erick Shepherd"]
__version__ = "1.0.0"


def sine_wave(frequency, duration, volume, sampling_rate):
    
    """
    
    Generates a sine wave signal.
    
    """
    
    A = volume
    f = frequency
    t = np.arange(np.floor(sampling_rate * duration).astype(np.uint32))
    T = f / sampling_rate
    
    waveform = A * np.sin(2 * np.pi * t * T).astype(np.float32)
    
    return waveform
