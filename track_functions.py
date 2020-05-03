#---------------------------------------------
#In this file we create different functions that modify Tracks that can later be used to 
# modify subject in main 
#---------------------------------------------

from mingus.containers import Track
from mingus.containers import Bar
from mingus.containers import NoteContainer
from mingus.containers import Note
import mingus.core.intervals as intervals
import mingus.core.notes as notes
import mingus.core.scales as scales
import mingus.core.keys as keys
import copy
import random


#--------------------------------------------------------------------
#HELPER FUNCTIONS 
#TODO: write a function for merging two tracks into 1 (play both tracks simultaneously)
#--------------------------------------------------------------------

def add_tracks(track1, track2):
    for i in range(len(track2)):  
        track1.add_bar(track2[i])

#def merge_tracks(track1,track2):


#--------------------------------------------------------------------
#INIT PRESETS
#TODO: Write better and more thought out presets for testing 
#--------------------------------------------------------------------
def init_preset_track(num):
    track = Track()
    if num==1: #C-chord
        nc = NoteContainer(["C","E"])
        track.add_notes(nc)
        track + "E"
        track + "A-3"
        track.add_notes(None)
        track + "C-5"
        track + "E-5"
        nc2 = NoteContainer(["F","G"])
        track.add_notes(nc2)
        track + "G-5"
        track + "C-6"
    if num==2:
        track + "Gb"
        track + "B-3"
        track + "D"
        track + "E"
        track + "Gb"
        track + "F"
        track + "A#"
        track + "B"
        track + "C-5"
        track + "D-5"
    if num ==3:
        test_scale = scales.Major("C")
        for i in range(7):
            track + test_scale[i]
    return track


#--------------------------------------------------------------------
# Transpose NEEDS FIX! 
# TODO: Transpose doesn't work for transposing more than an octave
# interval is for example " 7" = major seventh, "b4" = minor fourth
# More info on Mingus web page under intervals - intervals from shorthand
#--------------------------------------------------------------------

#alt method using nmb_of_halfnotes (an int) as input
def transpose_from_halfnote(track,nmb_of_halfnotes,up =True):
    #determine interval from nmb_of_steps
    lookup = ["b2"," 2","b3"," 3", " 4", "#4", " 5", "b6", " 6", "b7", " 7"]
    interval = lookup[nmb_of_halfnotes-1]
    
    # Use transpose_track to get a transposed copy of the track
    transposed_track = transpose(track, interval, up)
    
    # Return transposed track
    return transposed_track

# A start to a function to use in bar 5 and 6. Does not yet actually do anything.
# When done, it should be able to transpose a melody from C major to A minor
"""def transpose_to_relative_minor(track,original_key,harmonic)
    new_key = intervals.minor_third(original_key)
    # Get the notes of the minor scale
    new_scale = scales.get_notes(new_key.lower())
    # If harmonic minor, use the major 7th
    if harmonic == True:
        new_scale[6] = notes.augment(new_scale[6])
    return track"""

def transpose_to_relative_minor(track, original_key, harmonic):
    transposed_track = copy.deepcopy(track)
    if original_key in keys.major_keys:
        old_scale = keys.get_notes(original_key)
        new_key = keys.relative_minor(original_key)
        new_scale = keys.get_notes(new_key)
        
        if harmonic:
            new_scale[6] = notes.augment(new_scale[6])
            new_scale[6] = notes.reduce_accidentals(new_scale[6])
        
        
        input_notes = transposed_track.get_notes()
        for bar in input_notes:

            #Check if the nc contained in the bar/"note" is a pause, then do nothing
            nc = bar[-1]
            if nc is None:
                continue
            
            #Otherwise
            else:
                #For every actual note in the note containers (important if there is a chord)
                for note in nc:
                    if note.name in old_scale:
                        index = old_scale.index(note.name)
                        note.name = new_scale[index]
                    else:
                        note.transpose("b3")
                        note.name = notes.reduce_accidentals(note.name)
    else:
        print("input key is not major key")   
    return transposed_track

#TEST for Transpose to relative minor 
""""
test_track = init_preset_track(2)
print(test_track)
print(transpose_to_relative_minor(test_track, "Cb", True))
"""

def transpose(track, interval, up):
    "Return a copy of the track, transposed the given interval up if up = True, otherwise down."
    
    # Copy value of reference to aviod problems with overwriting    
    transposed_track = copy.deepcopy(track)
    
    # Calculate transposed track
    input_notes = transposed_track.get_notes()
    for note in input_notes:
        # Try to check if the note container is None. If not, transpose it.
        # note is technically a note container, might be good to know sometime.
        if note[-1] is None:
                continue                    
        else:
            note[-1].transpose(interval, up)
    
    # Return transposed track
    return transposed_track

#NEEDS TO FIX TRANSPOSE OVER OCTAVE
#Helper octave function maybe?
def octave(track, nmb_of_octaves, up=True):
    return track
      
#--------------------------------------------------------------------
#REVERSE DONE
#Returns an copied and inverted track of input track
#--------------------------------------------------------------------
def reverse(track):
    # Copy value of reference to aviod problems with overwriting    
    input_track = copy.deepcopy(track)
    #empty track to write to later
    reversed_track = Track()

    #create a reversed list of notes from input track
    input_notes = input_track.get_notes()
    reversed_notes = reversed(list(input_notes))
    
    #Add notes to reversed_track
    for note in reversed_notes:
        reversed_track.add_notes(note[-1])

    # Return reversed track
    return reversed_track

#--------------------------------------------------------------------
#INVERSE - IN PROGRESS
#TODO Add the right accidentals to the notes depending on the scale
#returns a copied and inverted track of input track. Inverts around the starting note of the input track
#--------------------------------------------------------------------
def inverse(track):
    # Copy value of reference to aviod problems with overwriting 
    inversed_track = copy.deepcopy(track)

    #"note" generator
    input_notes = inversed_track.get_notes()
    #note[-1] is a note container
    #note[-1][0] is a note

    #take out the first actual note from the "note" generator
    start_note = next(input_notes)[-1][0]

    #save the note name value without axidentals for camparison with the scale string
    base_note_value = start_note.name[0]

    #create a string with the ordered notes from the cmaj scale starting from the note after 
    #the base_note_value until the base_note_value is read again. This is used to calculate the
    #inversed notes later on
    Cmaj_scale = "CDEFGABCDEFGAB"
    scale = Cmaj_scale.split(base_note_value)[1]

    #Its not pretty nut it seems to work
    #For every bar/"note" we get out of the note generator
    for bar in input_notes:

        #Check if the nc contained in the bar/"note" is a pause, then do nothing
        nc = bar[-1]
        if nc is None:
             continue
        
        #Otherwise
        else:
            #For every actual note in the note containers (important if there is a chord)
            for note in nc:

                #initial value for an offset variable 
                diff = 0

                #If the note doesn't have the same note name (eg. "C" or "D") as the base note 
                #We calculate how many steps in the major scale we have to take to find 
                # A note that corresponds the one we have without accidentals. 
                # (eg. base_note_val ="C", note = "Eb" we have to take 2 steps to find "E" in Cmaj)
                if not (note.name[0] == base_note_value):
                    diff = scale.index(note.name[0]) + 1

                #Calculation of octave, a little messy but works    
                if base_note_value == "C":
                    if note.name[0] == "C":
                        note.octave = start_note.octave + (start_note.octave - note.octave)
                    else:
                        note.octave = start_note.octave + (start_note.octave - note.octave - 1)

                else:
                    if note.name[0] == "C" or scale.index("C") == (6-diff):
                        note.octave = start_note.octave + (start_note.octave - note.octave + 1)
                    else:
                        note.octave = start_note.octave + (start_note.octave - note.octave)
                
                #Use offset to assign the note the correct note value in C-maj
                if not (note.name[0] == base_note_value):
                    note.name = scale[-diff]
                else:
                    note.name = base_note_value
                
                #TODO Add the right accidentals to the notes depending on the scale
                
                
    #return inversed track
    return inversed_track       

#--------------------------------------------------------------------
#INIT RANDOM (1-BAR) TRACK
# Can be used to initalize a random subject, if is_subject is set to True. This gives a random bar that
# starts on the root note of the key. 
#--------------------------------------------------------------------
# Limitations (intended and uninteded) so far:
#   - duration is either half, quarter or eigth note. This is set to create a 'meaningful' melody.
#   there could be more options but it should probably be weighed towards these values
#   - the pitch range is only root to 7th. maybe it would be better to center the range around the root note
#   - the randomization is uniform
#   - it can't generate any pauses
#   - it only returns a single bar (useful for subjects but we might want to create longer random tracks ?)
# ----------------------------------
def init_random_track(key, is_subject):
    notes = keys.get_notes(key)
    bar = Bar()
    while bar.current_beat < 1 :
        # Randomize pitch and duration of each note. 
        duration = 2**random.randint(1,3)
        pitch = notes[random.randint(0,6)] 
        
        # If it is intened to be a subject, set the first note to the root.
        if bar.current_beat == 0 and is_subject == True:
            pitch = notes[0]
        
        # If the randomized duration doesn't fit in the bar, make it fit
        if 1/duration > 1 - bar.current_beat:
            duration = 1 / (1- bar.current_beat)
        
        # Place the new note in the bar
        bar.place_notes(pitch, duration)
    
    # Create a track to contain the randomized bar
    track = Track()
    track + bar
    
    # Return the track
    return track


#--------------------------------------------------------------------
#CHANGE-SPEED DONE
# Changes the speed of a track 
# up = true if you want to speed up, up = False if you want to slow down
# factor determines how much to speed up / slow down if factor = 2 we will either dubbel of half the speed 
#--------------------------------------------------------------------
def change_speed(track, factor, up=True):
    changed_track = Track()
    #if factor is 0 we return an empty track
    if (factor != 0.0) : 

        input_track = copy.deepcopy(track)
        input_notes = input_track.get_notes()

        #if we want to speed up (notespeed *= factor)
        if up:
            for note in input_notes:
                changed_track.add_notes(note[-1],int(note[1]*factor))

        #if we want to slow down (notespeed *= (1/factor))
        else:
            for note in input_notes:
                changed_track.add_notes(note[-1], int(note[1]/factor))
                

    return changed_track    

#----------------------------------
# TODO
#-----------------------------------

#augumentation/diminition


#ev. normalize notes to scale?
