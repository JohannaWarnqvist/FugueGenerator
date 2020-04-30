#--------------------------------------------------------------
# This document works as the Main file for fugue generation
# Contains the global variables that defines the fugue, voices, key and subject
# The function generate fugue generates a finished fugue composition
# The subject can be any length!
#--------------------------------------------------------------

from mingus.containers import Composition
from mingus.containers import Bar
from mingus.containers import Track
import mingus.core.intervals as intervals

import mingus.extra.lilypond as LilyPond
from Mingus_LilyPond_helper import to_LilyPond_file
import track_functions as Track_Functions
from mingus.midi import midi_file_out
import copy

#Important variables!
fugue = Composition()
first_voice = Track()
second_voice = Track() 

#Very useful helper function
def add_tracks(track1, track2):
    for i in range(len(track2)):  
        track1.add_bar(track2[i])

#input_key is a char signifying what key we are using
#input_subject is a Track, subject can be any length
def generate_fugue(key,subject):

    #TODO 
    #Fill out rest of bar of subject with rest(i did this but it caused problems with transpose so transpose needs to be fixed first)
    
    subject_length = len(subject)

    # Create first bar with subject in first voice and rest in second voice. 
    rest_1bar = Bar(key)
    rest_1bar.place_rest(1)
    first_voice = copy.deepcopy(subject)
    #Kind of ugly way of writing add same amount of "rest bars" as the number of bars in the subject
    for i in range(subject_length):  
        second_voice.add_bar(copy.deepcopy(rest_1bar))
    

    # Create second bar with answer in second voice. Countersubject comes later.
    answer = Track_Functions.transpose_from_halfnote(subject , 7)
    # same as using
    # answer = copy.deepcopy(subject)
    # answer = answer.transpose(" 5")

    add_tracks(second_voice,answer)



    #second_voice = second_voice + answer

    # Create development in minor in bar 5 and 6. 
    # Create stretto in bar 9 and 10.

    #INSERT MORE CODE HERE
    

    #Add voices together to create a final composition
    fugue.add_track(first_voice)
    fugue.add_track(second_voice)

    #Generate lilypond file for fugue named final_fugue
    finished_fugue = LilyPond.from_Composition(fugue)
    to_LilyPond_file(finished_fugue,"final_fugue")

    #Generate MIDI output for fugue named final_fugue
    midi_file_out.write_Composition("final_fugue.mid", fugue)

 

#Test for debugging
test_track = Track_Functions.init_preset_track(1)
generate_fugue("C",test_track)
