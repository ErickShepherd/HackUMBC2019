"""

A module to generate arbitrary music scales

Module metadata:

    Author 01:      Erick Shepherd (ErickShepherd@UMBC.edu)
    E-mail:         ErickShepherd@UMBC.edu
    Event:          HackUMBC Fall 2019
    Team:           Swan Song
    Date created:   2019-09-29
    Last updated:   2019-09-29

Summary:

    This module supplies a set of functions to produce arbitrary music scales
    given a set of note names, a number of octaves, and a reference frequency.

"""

# Standard library imports.
from itertools import combinations

# Third party imports.
import pyaudio
import numpy as np
import pandas as pd

# Local application imports.
import wavefunctions

# Dunder definitions.
__author__  = ["Erick Shepherd"]
__version__ = "1.1.0"

# Constant definitions.
MIDI_MINIMUM = 0
MIDI_MAXIMUM = 127
SUBCONTRA_C  = 16.352
SEMITONES    = 12
OCTAVES      = 9
NOTE_NAMES   = ["C",  "C#", "D",  "D#",
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
    
    for semitone, name in enumerate(names, start = 1):
        
        note_frequencies[name] = []
        
        for octave in range(-1, octaves + 1):
                        
            frequency = compute_frequency(octave,
                                          semitone,
                                          semitones,
                                          reference)
            
            note_frequencies[name].append(frequency)
            
    note_frequencies = pd.DataFrame(note_frequencies)
    note_frequencies.set_index(np.arange(-1, octaves + 1), inplace = True)
    note_frequencies.index.name = "octave"
    
    return note_frequencies


def generate_scale_names(names = NOTE_NAMES, octaves = OCTAVES):
    
    """
    
    Given parameters for the desired scale, this function produces a
    pandas.DataFrame of note names for a custom music scale.
    
    """

    note_names = {}
        
    for semitone, name in enumerate(names, start = 1):
        
        note_names[name] = []
        
        for octave in range(-1, octaves + 1):
            
            designation = f"{name}{octave}"
            
            note_names[name].append(designation)
    
    note_names = pd.DataFrame(note_names)
    note_names.set_index(np.arange(-1, octaves + 1), inplace = True)
    note_names.index.name = "octave"
    
    return note_names


def generate_music_scale(names               = NOTE_NAMES,
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
    number_of_notes = semitones * (octaves + 2)
        
    notes = {names[i] : frequencies[i] for i in range(number_of_notes)}
    notes = pd.Series(notes)
    
    return notes


def generate_major_notes():
    
    frequencies = generate_music_scale()
    frequencies = frequencies.filter(regex = r"^[^#]*$")
    
    return frequencies


def generate_minor_notes():
    
    frequencies = generate_music_scale()
    frequencies = frequencies.filter(regex = r".*#.*$")
    
    return frequencies


def generate_minor_thirds():
    
    """
    
    Generates an array of frequencies of minor thirds.
    
    """
    
    frequencies = generate_music_scale()
    notes       = pd.Series(frequencies.index.values, index = frequencies)
    
    note_pairs    = np.array(list(combinations(frequencies, 2)))
    desired_ratio = round(frequencies["A4"] / frequencies["C4"], 2)
    ratios        = np.round(note_pairs[:, 1] / note_pairs[:, 0], 2)
    
    frequencies_to_notes = np.vectorize(lambda frequency: notes[frequency])
    
    minor_third_frequency_pairs = note_pairs[ratios == desired_ratio]
    minor_third_note_pairs = frequencies_to_notes(minor_third_frequency_pairs)
    
    return minor_third_note_pairs


def generate_midi_minor_thirds():
    
    """
    
    Generates an array of MIDI scales of minor thirds.
    
    """
    
    midi_map = generate_midi_scale(enforce_range = False)
    notes    = generate_minor_thirds()
    
    notes_to_midi = np.vectorize(lambda note: midi_map[note])
    
    midi = notes_to_midi(notes)
    mask = np.all((MIDI_MINIMUM <= midi) & (midi <= MIDI_MAXIMUM), axis = 1)
    midi = midi[mask]
    
    return midi


def generate_major_thirds():
    
    """
    
    Generates an array of frequencies of major thirds.
    
    """
    
    frequencies = generate_music_scale()
    notes       = pd.Series(frequencies.index.values, index = frequencies)
    
    note_pairs    = np.array(list(combinations(frequencies, 2)))
    desired_ratio = round(frequencies["E4"] / frequencies["C4"], 2)
    ratios        = np.round(note_pairs[:, 1] / note_pairs[:, 0], 2)
    
    frequencies_to_notes = np.vectorize(lambda frequency: notes[frequency])
    
    major_third_frequency_pairs = note_pairs[ratios == desired_ratio]
    major_third_note_pairs = frequencies_to_notes(major_third_frequency_pairs)
    
    return major_third_note_pairs


def generate_midi_major_thirds():
    
    """
    
    Generates an array of MIDI scales of major thirds.
    
    """
    
    midi_map = generate_midi_scale(enforce_range = False)
    notes    = generate_major_thirds()
    
    notes_to_midi = np.vectorize(lambda note: midi_map[note])
    
    midi = notes_to_midi(notes)
    mask = np.all((MIDI_MINIMUM <= midi) & (midi <= MIDI_MAXIMUM), axis = 1)
    midi = midi[mask]
    
    return midi


def generate_major_chords():
    
    """
    
    Generates an array of frequencies of major chords.
    
    """
    
    frequencies = generate_music_scale()
    notes       = pd.Series(frequencies.index.values, index = frequencies)
    
    note_pairs    = np.array(list(combinations(frequencies, 2)))
    desired_ratio = round(frequencies["E4"] / frequencies["C4"], 2)
    ratios        = np.round(note_pairs[:, 1] / note_pairs[:, 0], 2)
    
    frequencies_to_notes = np.vectorize(lambda frequency: notes[frequency])
    
    major_chord_frequency_pairs = note_pairs[ratios == desired_ratio]
    major_chord_note_pairs = frequencies_to_notes(major_chord_frequency_pairs)
    
    return major_chord_note_pairs
    

def generate_midi_major_chords():
    
    """
    
    Generates an array of MIDI scales of major chords.
    
    """
    
    midi_map = generate_midi_scale(enforce_range = False)
    notes    = generate_major_chords()
    
    notes_to_midi = np.vectorize(lambda note: midi_map[note])
    
    midi = notes_to_midi(notes)
    mask = np.all((MIDI_MINIMUM <= midi) & (midi <= MIDI_MAXIMUM), axis = 1)
    midi = midi[mask]
    
    return midi
    
    
def generate_midi_scale(enforce_range = True):
    
    """
    
    Generates the MIDI note scale from Stuttgart pitch.
    
    """
    
    notes = generate_music_scale()
    midi  = (SEMITONES * np.log2(notes / notes["A4"]) + 69).astype(np.int8)
    
    if enforce_range:
        
        mask = (MIDI_MINIMUM <= midi) & (midi <= MIDI_MAXIMUM)
        midi = midi[mask]
    
    return midi

    
def generate_waveform(frequencies,
                      duration      = 1.0,
                      volume        = 1.0,
                      wavefunction  = wavefunctions.sine_wave,
                      sampling_rate = 44100):
    
    """
    
    Sums frequencies to generate a waveform.
    
    """
    
    frequencies = np.asarray(frequencies)
    
    waveform = np.zeros(np.floor(sampling_rate * duration).astype(np.uint32))
    
    for frequency in frequencies:
        
        waveform += wavefunction(frequency, duration, volume, sampling_rate)
        
    return waveform
    
    
def play_sound(waveform, sampling_rate = 44100):
    
    """
    
    Plays a sound.
    
    """
    
    player   = pyaudio.PyAudio()
    
    stream_kwargs = {"format"   : pyaudio.paFloat32,
                     "channels" : 1,
                     "rate"     : sampling_rate,
                     "output"   : True}
    
    stream = player.open(**stream_kwargs)

    stream.write(waveform)
    stream.stop_stream()
    stream.close()

    player.terminate()
