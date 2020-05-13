# ==============================================
# Document for all different fitness functions.
# ==============================================

#import random as rnd
import numpy as np
#import copy
#import math
#from mingus.core import *
from mingus.containers import *
import track_tests as measure
#import track_functions as Track_Functions
#import fitness_functions as Fitness_Functions 

def calculate_fitness_C(self, population):
        """Calculate the fitness for each chromosome and return an array
        with the fitness values
        """
        fitness_values = np.zeros(self.population_size)        
        for iPop in range(self.population_size):
            melody = population[iPop]
            fitness = 0
            notes = melody.get_notes()
            
            for note in notes:
                if note[-1] is None:
                        fitness += (1/note[1])*1/self.nr_bars
                else:
                    distance = Note('C').measure(note[-1][0])
                    fitness += (note[1] * 10*abs(distance))/self.nr_bars

            if fitness == 0:
                fitness_values[iPop] = 2
            else:
                fitness_values[iPop] = 1/fitness
        
        return fitness_values


def calculate_fitness_pauses(self, population):
        fitness_values = np.zeros(self.population_size)
        for iPop in range(self.population_size):
            melody = population[iPop]
            fitness = 0
            notes = melody.get_notes()
            
            for note in notes:
                if note[-1] is None:
                        fitness += 1/note[1]
                        
            fitness_values[iPop] = fitness
        return fitness_values

# TODO: Create the fitness function for the countersubject
def calculate_fitness_counter(self, population, input_melody):
    "Return a countersubject to the input_melody"
    
    # Until it is fixed, just return what fitness function C gives.
    return calculate_fitness_C(self, population)
    
    
# TODO: Create the fitness function for the countersubject
def calculate_fitness_modulate(self, population, from_bar, to_bar, from_key, to_key):
    "Return a melody that modulates from from_bar to to_bar"
    
    # Until it is fixed, just return what fitness function C gives.
    return calculate_fitness_C(self, population)
    
    
# TODO: Create the fitness function for a harmony to another melody
def calculate_fitness_harmony(self, population, input_melody):
    "Return a harmony to the input_melody"
    fitness_values = np.zeros(self.population_size)
    
    """
    # I started to try to write a fitness function. It works, but should be one of several 'tests'. And I don't know
    # any common practice in how to write a fitness function, how to distribute 'points' and so on, feel free to edit /Viktoria
    
    # -- The following block checks if there are thirds or sixths between the voices. --
    # It gives one "point" for each beat that fulfills the criteria. 
    good_intervals = [3,4,8,9]          # minor/major third, minor/major sixth
    for iPop in range(self.population_size):
        fitness = 0
        for beat in range(4):
            interval = Track_Tests.interval_at_beat(input_melody,population[iPop],beat,Halftones=True)
            if interval == None:
                continue
            if abs(interval) in good_intervals:
                fitness += 1
        fitness_values[iPop] = fitness"""
    return fitness_values

def calculate_fitness_test(self, population, input_melody):
    # Population is a list of melodies(Tracks) to test
    # Fitness values is a numpy list of fitness scores corresponding to the melodies in population 
    # iPop is current index of population list   
    fitness_values = np.zeros(self.population_size) 
    

    default_bias = 10.0
    #Helper funtion, creates and adds punishments for differing from "perfect values"
    def near_calc(population_value, perfect_value, bias):
        #We can change this to be an input to change the impact of different functions later 
        return abs(population_value - perfect_value) * bias *(-1.0)
        
    
    #The bigger the fraction the bigger the reward/punishment is
    def more_calc(population_fraction, bias):
        #We can change this to be an input to change the impact of different functions later 
        return population_fraction * bias
        

    #VARIABLES TO CHANGE: These are the "perfect" values
    #frac = fraction/percentage of ...., nmb = number of...., rep = repetitions
    frac_repeating_note_length = 0.3   
    nmb_chords_between_tracks = 5.0
    nmb_note_length_clusters = 6.0
    nmb_of_passage_rep = 1.0
    len_of_passage_rep = 3.0
                       

    #For every melody in population calculate fitness THIS IS THE BIG CALCULATION PART
    for iPop in range(self.population_size):
        melody = population[iPop]
        notes = melody.get_notes()
        fitness = 1.0
        #----------------------------------------------------------------------------------------------------------------    
        #Measure closeness to ideal value
        #Function that measures:                                                   Ideal value:                    Bias:
        fitness += near_calc(measure.repeating_note_length(melody),                frac_repeating_note_length,     default_bias)
        #fitness += near_calc(measure.average_numb_of_chords(melody,input_melody),  nmb_chords_between_tracks,      default_bias)       Error in merge 
        fitness += near_calc(measure.average_note_length_clusters(melody),         nmb_note_length_clusters,       default_bias)
        
        (x,y,frac_repeating_passage) = measure.repeating_passages(melody)
        fitness += near_calc(x,                                                    nmb_of_passage_rep,             default_bias)
        fitness += near_calc(y,                                                    len_of_passage_rep,             default_bias)
        #-----------------------------------------------------------------------------------------------------------------
        #Funtion that calculates fraction                                          Bias:
        #Rewards:
        fitness += more_calc(frac_repeating_passage,                               default_bias) #Calculated previously
        (on_beat,on_half_beat) = measure.count_notes_on_beat(melody)
        fitness += more_calc(on_beat,                                              default_bias)
        fitness += more_calc(on_half_beat,                                         default_bias)
        #fitness += more_calc(measure.count_notes_in_scale(melody),                 default_bias)            #Needs to get key somehow 

        #Punishments
        fitness += more_calc(- measure.repeating_note_pitch(melody,True),           default_bias)
        fitness += more_calc(- measure.count_tritone_or_seventh_in_two_skips(melody),default_bias)
          

        #Add resulting fitness value to list
        fitness_values[iPop] = fitness
        
        
    return fitness_values

    