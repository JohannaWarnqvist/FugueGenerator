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
from EvolutionaryGenerator import EvolutionaryGenerator
import random as rnd

#Important variables!
fugue = Composition()
first_voice = Track()
second_voice = Track()     
            
#input_key is a char signifying what key we are using
#input_subject is a Track, subject can be any length
def generate_fugue(key,subject):

    #If subject doesn't fill full bars fill out rest of last bar of subject with rest
    #if last bar is not full
    if not (subject[-1].is_full()): 
        #place a rest at the end of the last bar with the length of 1/(remaining fraction of bar)
        subject[-1].place_rest(int(1.0/subject[-1].space_left()))

    # Create first bar with subject in first voice and rest in second voice. 
    rest_1bar = Bar(key)
    rest_1bar.place_rest(1)
    first_voice = copy.deepcopy(subject)

    #Add same amount of "rest bars" as the number of bars in the subject
    for i in range(len(subject)):  
        second_voice.add_bar(copy.deepcopy(rest_1bar))
    

    # Create second bar with answer in second voice.
    answer = Track_Functions.create_answer(subject, key)
    
    #second_voice = second_voice + answer
    Track_Functions.add_tracks(second_voice,answer)
    
    # Generate countersubject
    eg_counter = EvolutionaryGenerator(key, nr_bars = 1, fitness_function = 'counter', input_melody = subject)
    eg_counter.run_evolution()
    counter_subject = copy.deepcopy(eg_counter.best_individual)
    
    Track_Functions.add_tracks(first_voice, counter_subject)
    

    # Save bar 2 for later modulation
    bar_2 = first_voice[-1]    
    
    # Generate development in minor in bar 5 and 6. 
    # Transposed -3 to minor + (stämma i för second voice tills vidare tom)
    minor_first_voice = Track_Functions.transpose_to_relative_minor(first_voice, key, False)
    minor_second_voice = Track_Functions.transpose_to_relative_minor(second_voice, key, False)
        
    bar_5 = minor_first_voice[0]
    
    # Generate harmony in second voice in bar 5
    eg_harmony_minor = EvolutionaryGenerator(key, nr_bars = 1, fitness_function = 'harmony', 
            input_melody = Track().add_bar(copy.deepcopy(minor_first_voice[0])))

    eg_harmony_minor.run_evolution()
    
    minor_second_voice[0] = eg_harmony_minor.best_individual[0]

    # Generate bar 3 and 4 as a modulation between bar 2 and 5
    minor_key = intervals.from_shorthand(key, 'b3', False)
    minor_key += 'm'

    eg_modulate_to_minor = EvolutionaryGenerator(key, nr_bars = 2, fitness_function = 'modulate', 
            from_bar = bar_2, to_bar = bar_5, from_key = key, to_key = minor_key)

    eg_modulate_to_minor.run_evolution()
    modulate_first_voice = copy.deepcopy(eg_modulate_to_minor.best_individual)

    # Generate second voice as harmony to the first voice in bar 3 and 4
    
    eg_second_voice_modulate = EvolutionaryGenerator(key, nr_bars = 2, fitness_function = 'harmony', 
            input_melody = modulate_first_voice, from_key = 'C', to_key = 'Am')
    
    eg_second_voice_modulate.run_evolution()    
    modulate_second_voice = copy.deepcopy(eg_second_voice_modulate.best_individual)


    # Add bar 3-6 to the voice tracks
    Track_Functions.add_tracks(first_voice, modulate_first_voice)
    Track_Functions.add_tracks(second_voice, modulate_second_voice)
    
    Track_Functions.add_tracks(first_voice, minor_first_voice)
    Track_Functions.add_tracks(second_voice, minor_second_voice)

    bar_6 = first_voice[-1]

    # Create canon in bar 9 and 10.
    # subject i first voice
    # second voice is subject but shifted (half a bar for now) 

    canon_first_voice = Track()
    canon_first_voice.add_bar(copy.deepcopy(subject[0]))
    
    bar_9 = canon_first_voice[0]

    canon_second_voice = Track_Functions.shift(subject, 2)

    # Create modulation from minor to major in 7 and 8
    
    eg_modulate_to_major = EvolutionaryGenerator(key, nr_bars = 2, fitness_function = 'modulate', 
            from_bar = bar_6, to_bar = bar_9, from_key = 'Am', to_key = 'C')

    eg_modulate_to_major.run_evolution()
    modulate_back_first_voice = copy.deepcopy(eg_modulate_to_major.best_individual)

    # Generate second voice as harmony to the first voice in bar 7 and 8
    
    eg_second_voice_modulate_back = EvolutionaryGenerator(key, nr_bars = 2, fitness_function = 'harmony', 
            input_melody = modulate_first_voice, from_key = 'Am', to_key = 'C')
    
    eg_second_voice_modulate_back.run_evolution()    
    modulate_back_second_voice = copy.deepcopy(eg_second_voice_modulate.best_individual)
    
    
    # Add bar 7-10 to the voice tracks
    Track_Functions.add_tracks(first_voice, modulate_back_first_voice)
    Track_Functions.add_tracks(second_voice, modulate_back_second_voice)
    
    Track_Functions.add_tracks(first_voice, canon_first_voice)
    Track_Functions.add_tracks(second_voice, canon_second_voice)

    Track_Functions.ending(first_voice, second_voice, subject, key)
    
    #Add voices together to create a final composition
    fugue.add_track(first_voice)
    fugue.add_track(second_voice)

    #Generate lilypond file for fugue named final_fugue
    finished_fugue = LilyPond.from_Composition(fugue)
    to_LilyPond_file(finished_fugue,"final_fugue")

    #Generate MIDI output for fugue named final_fugue
    midi_file_out.write_Composition("final_fugue.mid", fugue)

 
# nr_parts tells how many parts (inverse, reverse, minor, other start note) is wanted between first subject/answer and the last stretto.
def generate_random_fugue(key, subject, nr_parts = 1):
    #If subject doesn't fill full bars fill out rest of last bar of subject with rest
    #if last bar is not full
    if not (subject[-1].is_full()): 
        #place a rest at the end of the last bar with the length of 1/(remaining fraction of bar)
        subject[-1].place_rest(int(1.0/subject[-1].space_left()))

    # Create first bar with subject in first voice and rest in second voice. 
    rest_1bar = Bar(key)
    rest_1bar.place_rest(1)
    first_voice = copy.deepcopy(subject)

    #Add same amount of "rest bars" as the number of bars in the subject
    for i in range(len(subject)):  
        second_voice.add_bar(copy.deepcopy(rest_1bar))
    

    # Create second bar with answer in second voice.
    answer = Track_Functions.create_answer(subject, key)
    
    Track_Functions.add_tracks(second_voice,answer)
    
    # Generate countersubject
    eg_counter = EvolutionaryGenerator(key, nr_bars = 1, fitness_function = 'counter', input_melody = subject)
    eg_counter.run_evolution()
    counter_subject = copy.deepcopy(eg_counter.best_individual)
    
    Track_Functions.add_tracks(first_voice, counter_subject)
    

    # Save subject, answer and countersubject
    first_voice_first_part = copy.deepcopy(first_voice)
    second_voice_first_part = copy.deepcopy(second_voice)
    
    # Save bar 2 for later modulation
    bar_prev = first_voice[-1]

    variants = ['Minor', 'Reverse']
    iParts = 0
    while iParts < nr_parts:
            rVariant = rnd.choice(variants)
            
            if rVariant == 'Minor':
                # Generate development in minor
                # Transposed -3 to minor (stämma i second voice tills vidare tom)
                new_first_voice = Track_Functions.transpose_to_relative_minor(first_voice, key, False)
                new_second_voice = Track_Functions.transpose_to_relative_minor(second_voice, key, False)
                    
                bar_after = new_first_voice[0]
            
                # Generate harmony in second voice first bar
                eg_harmony = EvolutionaryGenerator(key, nr_bars = 1, fitness_function = 'harmony', 
                        input_melody = Track().add_bar(copy.deepcopy(new_first_voice[0])))

                eg_harmony.run_evolution()
                
                new_second_voice[0] = eg_harmony.best_individual[0]

            elif rVariant == 'Reverse':
                # Genereate inverse development
                
                new_first_voice = Track_Functions.reverse(first_voice_first_part, key)
                new_second_voice = Track_Functions.reverse(second_voice_first_part, key)
                
                bar_after = new_first_voice[0]

                # Generate harmony in second voice first bar
                eg_harmony = EvolutionaryGenerator(key, nr_bars = 1, fitness_function = 'harmony', 
                        input_melody = Track().add_bar(copy.deepcopy(new_first_voice[1])))

                eg_harmony.run_evolution()
                breakpoint()
                new_second_voice[1] = eg_harmony.best_individual[0]
                
                

            # Generate the two bars linking this new part to the previous parts

            eg_modulate = EvolutionaryGenerator(key, nr_bars = 2, fitness_function = 'modulate', 
                    from_bar = bar_prev, to_bar = bar_after)

            eg_modulate.run_evolution()
            modulate_first_voice = copy.deepcopy(eg_modulate.best_individual)

            # Generate second voice as harmony to this linking part
            
            eg_second_voice_modulate = EvolutionaryGenerator(key, nr_bars = 2, fitness_function = 'harmony', 
                    input_melody = modulate_first_voice)
            
            eg_second_voice_modulate.run_evolution()    
            modulate_second_voice = copy.deepcopy(eg_second_voice_modulate.best_individual)


            # Add new bars to the voice tracks
            Track_Functions.add_tracks(first_voice, modulate_first_voice)
            Track_Functions.add_tracks(second_voice, modulate_second_voice)
            
            Track_Functions.add_tracks(first_voice, new_first_voice)
            Track_Functions.add_tracks(second_voice, new_second_voice)

            bar_prev = first_voice[-1]
            
            iParts += 1
            

    # Create canon in bar 9 and 10.
    # subject i first voice
    # second voice is subject but shifted (half a bar for now) 

    canon_first_voice = Track()
    canon_first_voice.add_bar(copy.deepcopy(subject[0]))
    
    bar_after = canon_first_voice[0]

    canon_second_voice = Track_Functions.shift(subject, 2)

    # Create modulation from minor to major in 7 and 8
    
    eg_modulate_to_major = EvolutionaryGenerator(key, nr_bars = 2, fitness_function = 'modulate', 
            from_bar = bar_prev, to_bar = bar_after)

    eg_modulate_to_major.run_evolution()
    modulate_back_first_voice = copy.deepcopy(eg_modulate_to_major.best_individual)

    # Generate second voice as harmony to the first voice in bar 7 and 8
    
    eg_second_voice_modulate_back = EvolutionaryGenerator(key, nr_bars = 2, fitness_function = 'harmony', 
            input_melody = modulate_first_voice)
    
    eg_second_voice_modulate_back.run_evolution()    
    modulate_back_second_voice = copy.deepcopy(eg_second_voice_modulate.best_individual)
    
    
    # Add bar 7-10 to the voice tracks
    Track_Functions.add_tracks(first_voice, modulate_back_first_voice)
    Track_Functions.add_tracks(second_voice, modulate_back_second_voice)
    
    Track_Functions.add_tracks(first_voice, canon_first_voice)
    Track_Functions.add_tracks(second_voice, canon_second_voice)

    Track_Functions.ending(first_voice, second_voice, subject, key)
    
    #Add voices together to create a final composition
    fugue.add_track(first_voice)
    fugue.add_track(second_voice)

    #Generate lilypond file for fugue named final_fugue
    finished_fugue = LilyPond.from_Composition(fugue)
    to_LilyPond_file(finished_fugue,"final_fugue")

    #Generate MIDI output for fugue named final_fugue
    midi_file_out.write_Composition("final_fugue.mid", fugue) 
 

#Test for debugging
test_track = Track_Functions.init_random_track("D",True)
#test_track = Track_Functions.init_preset_track('blinka')
generate_random_fugue("D", test_track, 3)


