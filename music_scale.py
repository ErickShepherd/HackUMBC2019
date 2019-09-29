"""

A module to generate arbitrary music scales

Module metadata:

    Author:         Erick Shepherd
    E-mail:         ErickShepherd@UMBC.edu
    Event:          HackUMBC Fall 2019
    Team:           Swan Song
    Date created:   2019-09-29
    Last updated:   2019-09-29

Summary:

    This module supplies a set of functions to produce arbitrary music scales
    given a set of note names, a number of octaves, and a reference frequency.

"""

# Third party imports.
import pyaudio
import pandas as pd

# Local application imports.
import wavefunctions

# Dunder definitions.
__author__  = "Erick Shepherd"
__version__ = "1.1.0"

# Constant definitions.
SUBCONTRA_C = 16.352
SEMITONES   = 12
OCTAVES     = 9
NOTE_NAMES  = ["C",  "C#", "D",  "D#",
               "E",  "F",  "F#", "G",
               "G#", "A",  "A#", "B"]


def compute_frequency(octave,
                      semitone,
                      semitones = SEMITONES,
                      reference = SUBCONTRA_C):
    
    """
    
    Given information about the desired note and the musical scale, this
    function computes the corresponding frequency in Hertz (Hz).
    
    """
    
    frequency = 2 ** (octave + (semitone - 1) / semitones) * reference
    
    return frequency


def generate_scale_frequencies(names     = NOTE_NAMES,
                               octaves   = OCTAVES,
                               reference = SUBCONTRA_C):
    
    """
    
    Given parameters for the desired scale, this function produces a
    pandas.DataFrame of note frequencies for a custom music scale.
    
    """
    
    semitones        = len(names)
    note_frequencies = {}
    
    for semitone, name in enumerate(names):
        
        note_frequencies[name] = []
        
        for octave in range(octaves):
            
            frequency = compute_frequency(octave,
                                          semitone,
                                          semitones,
                                          reference)
            
            note_frequencies[name].append(frequency)
            
    note_frequencies = pd.DataFrame(note_frequencies)
    note_frequencies.index.name = "octave"
    
    return note_frequencies


def generate_scale_names(names = NOTE_NAMES, octaves = OCTAVES):
    
    """
    
    Given parameters for the desired scale, this function produces a
    pandas.DataFrame of note names for a custom music scale.
    
    """

    note_names = {}
        
    for semitone, name in enumerate(names):
        
        note_names[name] = []
        
        for octave in range(octaves):
            
            designation = f"{name}{octave}"
                        
            note_names[name].append(designation)
    
    note_names = pd.DataFrame(note_names)
    note_names.index.name = "octave"
    
    return note_names


def generate_musical_scale(names               = NOTE_NAMES,
                           octaves             = OCTAVES,
                           reference_frequency = SUBCONTRA_C):
    
    """
    
    Given parameters for the desired scale, this function produces a
    pandas.Series of note name:frequency pairs for a custom music scale.
    
    """
    
    semitones        = len(names)
    note_names       = generate_scale_names(names, octaves)
    note_frequencies = generate_scale_frequencies(names,
                                                  octaves,
                                                  reference_frequency)
    
    names           = note_names.values.flatten()
    frequencies     = note_frequencies.values.flatten()
    number_of_notes = semitones * octaves
        
    notes = {names[i] : frequencies[i] for i in range(number_of_notes)}
    notes = pd.Series(notes)
    
    return notes

    
def play_sound(frequency,
               duration      = 1.0,
               volume        = 1.0,
               wavefunction  = wavefunctions.sine_wave,
               sampling_rate = 44100):
    
    """
    
    Plays a sound.
    
    """
    
    player   = pyaudio.PyAudio()
    waveform = wavefunction(frequency, duration, volume, sampling_rate)
        
    stream_kwargs = {"format"   : pyaudio.paFloat32,
                     "channels" : 1,
                     "rate"     : sampling_rate,
                     "output"   : True}
    
    stream = player.open(**stream_kwargs)

    stream.write(waveform)
    stream.stop_stream()
    stream.close()

    player.terminate()
