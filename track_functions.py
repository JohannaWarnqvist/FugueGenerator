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
    return track

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
    #copy value of reference to prevent changing value of subject
    transposed_track = copy.deepcopy(track)
    #calculate transposed track and return
    transposed_track = transposed_track.transpose(interval,up)

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

