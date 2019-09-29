"""

A module to generate midi files

Module metadata:

    Author 01:      Thomas Owens (OwensT30@gmail.com)
    Author 02:      Erick Shepherd (ErickShepherd@UMBC.edu)
    Event:          HackUMBC Fall 2019
    Team:           Swan Song
    Date created:   2019-09-29
    Last updated:   2019-09-29

Summary:

    This module generates random midi files.

"""

# Third party imports.
import numpy as np
from midiutil.MidiFile import MIDIFile

# Local application imports.
import music_scale

# Dunder definitions.
__author__  = ["Thomas Owens", "Erick Shepherd"]
__version__ = "1.0.0"


def populate(midi_file):
    
    midi_file.addNote(track, channel, pitch, time, duration, volume, annotation = None)


def f(time_signature,
      tempo):
    
    midi_file = MIDIFile()
    midi_file.addTrackName(track, time, track_name)
    midi_file.addTimeSignature(track, time, numerator, denominator, clocks_per_tick, notes_per_quarter=8)
    midi_file.addTempo(track, time, tempo)
    midi_file.addKeySignature(track, time, accidentals, accidental_type, mode, insertion_order=0)
    midi_file.addCopyright(track, time, notice)
    
    track    = 0   # Track numbers are zero-origined
    channel  = 0   # MIDI channel number
    pitch    = 60  # MIDI note number
    time     = 0   # In beats
    duration = 1   # In beats
    volume   = 100 # 0-127, 127 being full volume
    
    with open(filename, "wb") as output_file:
        
        midi_file.writeFile(output_file)
