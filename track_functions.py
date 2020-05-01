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
import copy


#---------------------------------
#FUNCTIONS
#----------------------------------

#Init preset track 
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
    return track


#Transpose NEEDS FIX! Transpose doesn't work for transposing mpore than an octave
# interval is for example " 7" = major seventh, "b4" = minor fourth
# More info on Mingus web page under intervals - intervals from shorthand

#alt method using nmb_of_halfnotes (an int) as input
def transpose_from_halfnote(track,nmb_of_halfnotes,up =True):
    #determine interval from nmb_of_steps
    lookup = ["b2"," 2","b3"," 3", " 4", "#4", " 5", "b6", " 6", "b7", " 7"]
    interval = lookup[nmb_of_halfnotes-1]
    
    # Use transpose_track to get a transposed copy of the track
    transposed_track = transpose(track, interval, up)
    
    # Return transposed track
    return transposed_track
   

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
#Helper octave function
def octave(track, nmb_of_octaves, up=True):
    return track
      

#Reverse WORKS
#Returns an copied and inverted track of input track
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

#Inverse IN PROGRESS
#returns a copied and inverted track of input track. Inverts around the starting note of the input track
#Problems(probably not the right notation for the scale?)


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

#----------------------------------
# TODO
#-----------------------------------
#Init random track
#augumentation/diminition
#overlap tracks function (merge two track to become one )
#.....

