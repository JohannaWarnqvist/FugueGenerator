#---------------------------------------------
#In this file we create dirrefent functions that modify Tracks that can later be used to 
# modify subject in main 
#---------------------------------------------

from mingus.containers import Track
from mingus.containers import Bar
import mingus.core.intervals as intervals
import copy

#---------------------------------
#FUNCTIONS
#----------------------------------

#Init preset track 
def init_preset_track(num):
    track = Track()
    if num==1:
        track + "C"
        track + "A"
        track + "D"
        track + "F"
        track + "G"
        track + "E"
        track.add_notes(None)
        track.add_notes(None)
    return track


#TODO (Fixed ish) neither built in nor alternative method cad handle pauses!


#Transpose - track.transpose(interval, up = True):
# type_of_interval is for example " 7" = major seventh, "b4" = minor fourth
# You can use the numbers 1-7 combined with an optional accidental prefix to get the interval from a certain note.
# Any number of accidentals can be used, but -again- use it cautiously. No prefix means that you want the major interval,
# a ‘b’ will return the minor interval, ‘bb’ the diminished, ‘#’ the augmented.
# up is boolean that determines wheter to transpose it up (True) or down (False)

#alt method using nmb_of_halfnotes (an int) as input
def transpose_from_halfnote(track,nmb_of_halfnotes,up =True):
    #determine interval from nmb_of_steps
    lookup = ["b2"," 2","b3"," 3", " 4", "#4", " 5", "b6", " 6", "b7", " 7"]
    interval = lookup[nmb_of_halfnotes-1]
    
    # Use transpose_track to get a transposed copy of the track
    transposed_track = transpose_track(track, interval, up)
    
    # Return transposed track
    return transposed_track
   

def transpose_track(track, interval, up):
    "Return a copy of the track, transposed the given interval up if up = True, otherwise down."
    
    # Copy value of reference to aviod problems with overwriting    
    transposed_track = copy.deepcopy(track)
    
    # Calculate transposed track
    notes = transposed_track.get_notes()
    for note in notes:
        # Try to check if the note container is None. If not, transpose it.
        # note is technically a note container, might be good to know sometime.
        try:               
            if note[-1] == None:
                continue                    
        except:
            note[-1].transpose(interval, up)
    
    # Return transposed track
    return transposed_track
      

#Invert 
def invert(track):
    return track

#----------------------------------
# TODO
#-----------------------------------
#Init random track
#Reverse
#.....

