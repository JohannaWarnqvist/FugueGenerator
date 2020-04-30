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
    if num==2:
        bar = Bar()
        bar.place_rest(1)
        track.add_bar(bar)
    return track


#Transpose WORKS!
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
    notes = transposed_track.get_notes()
    for note in notes:
        # Try to check if the note container is None. If not, transpose it.
        # note is technically a note container, might be good to know sometime.
        if note[-1] is None:
                continue                    
        else:
            note[-1].transpose(interval, up)
    
    # Return transposed track
    return transposed_track
      

#Reverse WORKS
#Returns an copied and inverted track of input track
def reverse(track):
    # Copy value of reference to aviod problems with overwriting    
    input_track = copy.deepcopy(track)
    #empty track to write to later
    reversed_track = Track()

    #create a reversed list of notes from input track
    notes = input_track.get_notes()
    reversed_notes = reversed(list(notes))
    
    #Add notes to reversed_track
    for note in reversed_notes:
        reversed_track.add_notes(note[-1])

    # Return reversed track
    return reversed_track

#----------------------------------
# TODO
#-----------------------------------
#Init random track
#Reverse
#.....

