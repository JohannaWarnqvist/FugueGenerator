#--------------------------------------------------------------
#This document works as the Main file for fugue generation
#Contains the global variables that defines the fugue, voices, key and subject
# The function generate fugue generates a finished fugue composition
#--------------------------------------------------------------

from mingus.containers import Composition
from mingus.containers import Bar
from mingus.containers import Track

import mingus.extra.lilypond as LilyPond
from Mindus_LilyPond_helper import to_LilyPond_file
import track_functions as Track_Functions
from mingus.midi import midi_file_out

#Important variables!
fugue = Composition()
first_voice = Track()
second_voice = Track()
subject = Track()

#input_key is a char signifying what key we are using
#input_subject is a Track
def generate_fugue(input_key,input_subject):
    subject = input_subject
    key = input_key

    # Create first bar with subject in first voice and pause in second voice. 
    pause = Bar(key)
    pause.place_rest(1)
    first_voice = subject
    second_voice.add_bar(pause)

    # Create second bar with answer in second voice. Countersubject comes later.
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
