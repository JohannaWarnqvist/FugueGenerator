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