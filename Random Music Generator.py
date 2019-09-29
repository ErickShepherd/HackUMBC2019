
FLAT = "b"
DOUBLE_FLAT = "bb"
SHARP = "#"
DOUBLE_SHARP = "X"
NOTE_NAMES = ["E", "F", "G", "A", "B", "C", "D"]
# E below staff to F sharp above
MIDI_BASS_CLEF = list(range(40, 67))
# quarter notes -> 32nd notes
NOTE_VALUES = [1, 2, 4]


from midiutil.MidiFile import MIDIFile
import math
import random

def isPowerTwo(num):
    
    return num != 0 and ((num & (num - 1)) == 0)

def getKeySig():

    keySig = input("Please enter your key signature: ")
    # note name plus max two sharps or flats, no mixing of sharps and flats
    while keySig[0] not in NOTE_NAMES:
        print("This is not a valid key.")
        keySig = input("Please enter your key signature: ")
    while len(keySig) == 3 and keySig[1] != keySig[2]:
        print("This is not a valid key.")
        keySig = input("Please enter your key signature: ")
    while len(keySig) < 1 or len(keySig) > 3:
        print("This is not a valid key.")
        keySig = input("Please enter your key signature: ")
    return keySig

def getNumBars():

    numBars = int(input("Please enter the number of measures: "))
    # must enter at least one measure
    while numBars < 1:
        print("This is not a valid number of measures.")
        numBars = int(input("Please enter the number of measures: "))
    return numBars

def getMeasureBeats():

    numBeats = int(input("Please enter the number of beats in the measure: "))
    while numBeats < 1:
        print("This is not a valid number of beats.")
        numBeats = int(input("Please enter the number of beats in the measure: "))
    return numBeats

def getSubDiv():

    numSubDiv = int(input("Please enter the number of subdivisions in the measure: "))
    subDivBool = isPowerTwo(numSubDiv)

    while subDivBool == False:
        print("This is not a valid number of subdivisions. The subdivisions must be a power of two.")
        numSubDiv = int(input("Please enter the number of subdivisions in the measure: "))
        subDivBool = isPowerTwo(numSubDiv)
    return numSubDiv
    
def getTempo():

    tempo = int(input("Please enter the tempo for the song: "))
    while tempo < 1:
        print("This tempo is not valid. The tempo must be greater than 1 BPM.")
        tempo = int(input("Please enter the tempo for the song: "))
    return tempo

    
if __name__ == "__main__":

    # creates the MIDIFile object with one track
    MyMIDI = MIDIFile(1, deinterleave=False)
    
    # these values are essentially constant
    track  = 0
    channel = 0
    volume = 100

    time = 0

    # adds track name and tempo
    track_name = input("What do you want to call the track? ")
    MyMIDI.addTrackName(track, time, track_name)
    tempo = getTempo()

    # gets key signature 
    # keySig = getKeySig()

    # asks user how many measures they want the song to be
    numBars = getNumBars()

    # time signature
    print("What time signature will you use?")
    print()
    numerator = getMeasureBeats()
    denominator = getSubDiv()
    denominator = int(math.log(denominator, 2))
    clocks_per_tick = 24
    notes_per_quarter = 8
    MyMIDI.addTimeSignature(track, time, numerator, denominator, clocks_per_tick)


    # total_time represents the number of notes
    total_time = (numerator * numBars)
    while time < total_time:
        # put me in addNote for pitch
        rand_note = random.choice(MIDI_BASS_CLEF)
        rand_duration = 1/(random.choice(NOTE_VALUES))
        MyMIDI.addNote(track, channel, rand_note, time, rand_duration, volume)
        time += float(1/(random.choice(NOTE_VALUES)))

    # write file to disk
    name_file = input("What do you want to name the file (name.midi)? ")
    binfile = open(name_file, 'wb')
    MyMIDI.writeFile(binfile)
    binfile.close()


