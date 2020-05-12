# ==============================================
# Document for all different fitness functions.
# ==============================================

#import random as rnd
import numpy as np
#import copy
#import math
#from mingus.core import *
from mingus.containers import *
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
