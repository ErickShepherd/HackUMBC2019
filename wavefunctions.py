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
from scipy import signal

# Dunder definitions.
__author__  = ["Erick Shepherd"]
__version__ = "1.0.0"


def wave(wavefunction, frequency, duration, volume, sampling_rate):
    
    """
    
    Generates a generic waveform from a given wavefunction.
    
    """
    
    A = volume
    f = frequency
    t = np.arange(np.floor(sampling_rate * duration).astype(np.uint32))
    T = f / sampling_rate
    
    waveform = A * wavefunction(2 * np.pi * t * T).astype(np.float32)
    
    return waveform
    
    
def sine_wave(frequency, duration, volume, sampling_rate):
    
    """
    
    Generates a sine wave signal.
    
    """
    
    function = np.sin
    waveform = wave(function, frequency, duration, volume, sampling_rate)
    
    return waveform


def square_wave(frequency, duration, volume, sampling_rate):
    
    """
    
    Generates a square wave signal.
    
    """
    
    function = signal.square
    waveform = wave(function, frequency, duration, volume, sampling_rate)
    
    return waveform


def sawtooth_wave(frequency, duration, volume, sampling_rate):
    
    """
    
    Generates a sawtooth wave signal.
    
    """
    
    function = signal.sawtooth
    waveform = wave(function, frequency, duration, volume, sampling_rate)
    
    return waveform


def triangle_wave(frequency, duration, volume, sampling_rate):
    
    """
    
    Generates a triangle wave signal.
    
    """
    
    function = lambda t: 2 * np.abs(signal.sawtooth(t)) - 1
    waveform = wave(function, frequency, duration, volume, sampling_rate)
    
    return waveform
