#---------------------------------------------
#In this file we create dirrefent functions that modify Tracks that can later be used to 
# modify subject in main 
#---------------------------------------------

from mingus.containers import Track

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
    return track

#Transpose
def transpose(track):
    return track

#Invert 
def invert(track):
    return track

#----------------------------------
# TODO
#-----------------------------------
#Init random track
#Reverse
#.....

