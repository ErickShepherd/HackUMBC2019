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
    
    track    = 0   # Track numbers are zero-origined
    channel  = 0   # MIDI channel number
    #pitch    = 60  # MIDI note number
    #time     = 0   # In beats
    duration = 2   # In beats
    volume   = 100 # 0-127, 127 being full volume
    
    m = music_scale.generate_midi_major_thirds()
        
    for time in range(100):
    
        for pair in m[np.random.choice(np.arange(m.shape[0]), 100)]:
                        
            for pitch in pair:
                                
                midi_file.addNote(track, channel, pitch, time, duration, volume, annotation = None)

    return midi_file


def make_midi_file():
    
    midi_file = MIDIFile()
    midi_file = populate(midi_file)
#    midi_file.addTrackName(track, time, track_name)
#    midi_file.addTimeSignature(track, time, numerator, denominator, clocks_per_tick, notes_per_quarter=8)
#    midi_file.addTempo(track, time, tempo)
#    midi_file.addKeySignature(track, time, accidentals, accidental_type, mode, insertion_order=0)
#    midi_file.addCopyright(track, time, notice)
#    
#    track    = 0   # Track numbers are zero-origined
#    channel  = 0   # MIDI channel number
#    pitch    = 60  # MIDI note number
#    time     = 0   # In beats
#    duration = 1   # In beats
#    volume   = 100 # 0-127, 127 being full volume
    
    filename = "sandwich.midi"
    
    with open(filename, "wb") as output_file:
        
        midi_file.writeFile(output_file)
