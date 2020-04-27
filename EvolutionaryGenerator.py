import random as rnd
import numpy as np
import copy
from Note import Note
from Scale import Scale
import math
import copy


class EvolutionaryGenerator():

    def __init__(self, scale, nr_bars = 2):
        "Initialize all the parameters"
        
        # When testing to regenerate same case:
        #rnd.seed(1)
        #np.random.seed(1)

        # == Parameters ==
        self.population_size = 100
        self.nr_generations = 1000;
        
        self.crossover_probability = 0.8;
        self.mutation_probability = 1/(nr_bars*4);
        self.tournament_selection_parameter = 0.75;
        
        self.tournament_size = 2;
        self.nr_copies = 1;  
        
        self.pitch_probability = 0.5
        self.pause_probability = 0.5

        self.nr_bars = nr_bars
        self.scale = scale
        
        self.run_evolution()
        
    def run_evolution(self):
        
        # Initialize population
        self.population = self.initialize_population()
        
        fitness_values = np.zeros(self.population_size)
        max_fitness_value = 0
        for iGen in range(self.nr_generations):
            
            # == Calculate fitness and save best individual ==
            fitness_values = self.calculate_fitness(self.population)
            
            # Save a copy of the best individual
            best_individual_index = np.argmax(fitness_values)        
            best_individual = copy.deepcopy(self.population[best_individual_index])
            
            # Print best individual and its fitness value if better than before
            if fitness_values[best_individual_index] > max_fitness_value:
                print(iGen)
                print(best_individual)
                print(fitness_values[best_individual_index])
                max_fitness_value = fitness_values[best_individual_index]
            
            # == Tournament selection ==
            tmp_population = []
            for i in range(self.population_size):
                index_selected = self.tournament_selection(fitness_values, self.tournament_selection_parameter, self.tournament_size)
                tmp_population.append(self.population[index_selected])
            

            # == Crossover ==
            for iCross in range(0, self.population_size-1, 2):
                chromosome1 = self.population[iCross]
                chromosome2 = self.population[iCross + 1]
                
                r_cross = rnd.random()
                if r_cross < self.crossover_probability:
                    crossed_pair = self.cross_over([chromosome1, chromosome2])
                    tmp_population[iCross] = crossed_pair[0]
                    tmp_population[iCross + 1] = crossed_pair[1]
                
            
            # == Mutation ==            
            for i in range(self.population_size):
                tmp_population[i] = self.mutate(tmp_population[i])

            
            # == Elitism ==            
            tmp_population = self.insert_best_individual(tmp_population, best_individual)
            
            
            # == Save generation ==
            self.population = tmp_population
        
    
    def initialize_population(self):
        """Create the population consisting of the wanted number of
        randomly generated melodies
        """
        population = []
        
        for i in range(self.population_size):
            melody = []
            min_pitch = -12
            max_pitch = 24
            
            beat = 0   
            while beat < self.nr_bars * 16:
            
                # Testing
                if len(melody) > 1:
                    if melody[-1].beat > melody[-2].beat + melody[-2].length:
                        breakpoint()

                # Decide pitch of a note                
                r = rnd.random()
                if r < 0.05:
                    pitch_tone = None
                else:
                    pitch_list = self.scale.get_part_of_scale(min_pitch, max_pitch)
                    pitch_tone = rnd.choice(pitch_list)
                    
                # Decide length of a note, length 1 = quarter note. Max half note or what is left in bar if less than half note.
                length = rnd.randrange(1,min(self.nr_bars*16-beat,16)+1)
                
                # Scale to quarter notes due to Note class
                length_tone = length*0.25
                beat_note = beat*0.25
                
                # Create note object at the current beat

                note = Note(pitch_tone, length_tone, beat_note)
                
                # Add note to subject
                melody.append(note)
                
                beat += length
                
            population.append(melody)
    
        return population
    
    def cross_over(self, chromosomes):
        """Change chromosome by using crossover between two chromosomes.
        It decides a beat to split and exchange tails after this beat
        between the two chromosomes.
        """
        
        # Decide at which semiquaver to cross
        nr_note_slots = self.nr_bars*16        
        break_point = rnd.randrange(1,nr_note_slots)
        
        # Initialize list to save heads and tails of each chromosome      
        head_chromosome = [[],[]]
        tail_chromosome = [[],[]]
        
        for iChrom in range(2):
            beat = 0        
            for note in chromosomes[iChrom]:
                if beat + 4*note.length < break_point:
                    # Testing
                    if note.length < 0:
                        breakpoint()
                    
                    # Add the whole note to head
                    head_chromosome[iChrom].append(note)
                                
                elif beat < break_point:
                    # Split the note in two, with the first one in head and second in tail
                    
                    note1 = copy.copy(note)
                    note1.length = 0.25*(break_point-beat)
                    
                    note2 = copy.copy(note)
                    note2.length = note.length - note1.length
                    note2.beat = note1.beat + note1.length

                    # Testing
                    if note1.length < 0 or note2.length < 0:
                        breakpoint()
                    
                    head_chromosome[iChrom].append(note1)
                    tail_chromosome[iChrom].append(note2)
                
                else:
                    # Testing
                    if note.length < 0:
                        breakpoint()
                    
                    # Add the whole note to tail
                    tail_chromosome[iChrom].append(note)
                    
                    
                beat += 4*note.length
          
        # Create the new chromosomes by combining one chromosomes head with the other's tail.
        cross_chromosomes = [head_chromosome[0] + tail_chromosome[1], head_chromosome[1]+tail_chromosome[0]]
        
        return cross_chromosomes


    def tournament_selection(self, fitness_values, 
            tournament_selection_parameter, tournament_size):
        "Select index of new individual by using tournament selection"
    
        # == Choose individuals for the tournament ==
        
        chosen_indices = [rnd.randrange(self.population_size) for i in range(tournament_size)]
        
        # == Sort chosen indices with highest fitness first ==
        
        chosen_fitness_values = [fitness_values[i] for i in chosen_indices] 

        value_and_index = [] 
          
        for i in range(len(chosen_fitness_values)): 
              value_and_index.append([chosen_fitness_values[i],chosen_indices[i]]) 
        value_and_index.sort() 
        sort_index = [] 
          
        for x in value_and_index: 
              sort_index.append(x[1]) 
          
        
        # == Run the tournament selection ==
        
        for i in range(tournament_size - 1):
            r = rnd.random()
            if r < tournament_selection_parameter:
                index_selected = sort_index[i]
                return index_selected
        index_selected = sort_index[-1]
        return index_selected


    def mutate(self, chromosome):
        """Mutate each gene with a certain probability. Can either split the note into two 
        notes of same pitch, shorten tone and add pause at the rest part or longer the note 
        and delete any notes that where there previously."""
        #mutate the note by either splitting, merging with next or shortening adding a pause

        #breakpoint()
        mutated_chromosome = []
        self.mutation_probability = 2/len(chromosome)
        ind = 0
        current_beat = 0
        while ind < len(chromosome):
        
            # If completely covered by previous note, skip this note
            if chromosome[ind].beat + chromosome[ind].length <= current_beat:
                ind += 1
                continue
            
            # Note: Makes ordinary copy now, might cause trouble if the Note class changes
            note = copy.copy(chromosome[ind])
            
            # Check if the previous note is partly covered by previous note            
            if chromosome[ind].beat < current_beat:
                note.length = chromosome[ind].beat + chromosome[ind].length - current_beat
                note.beat = current_beat
                mutated_chromosome.append(note)

            else:
                
                r = rnd.random()            
                if r < self.mutation_probability:

                    # Either change the pitch of the note                    
                    r_pitch = rnd.random()
                    if r_pitch < self.pitch_probability:
                        
                        if note.pitch == None:
                            if len(mutated_chromosome) < 1:
                                if chromosome[ind].pitch != None:
                                    pitch = round(np.random.normal(loc = chromosome[ind].pitch, scale = 4))
                                else:
                                    pitch = round(np.random.normal(loc = self.scale.key, scale = 4))
                            else:
                                if mutated_chromosome[-1].pitch != None:
                                    pitch = round(np.random.normal(loc = mutated_chromosome[-1].pitch, scale = 4))
                                else:
                                    pitch = round(np.random.normal(loc = self.scale.key, scale = 4))
                            note.pitch = pitch
                        else:
                            pitch_change = round(np.random.normal(scale = 2))
                            note = copy.copy(chromosome[ind])
                            note.pitch += pitch_change
                        mutated_chromosome.append(note)
                    # Or change the length of the note
                    else:
                        # Decide how much to change the length
                        length_change = round(np.random.normal(scale = chromosome[ind].length*0.25))
                        if note.length + length_change > 0:
                            # If the note still has a positive length, make the change and add the note to the chromosome
                            note.length += length_change
                            mutated_chromosome.append(note)
                        else:
                            # If note length becomes less than zero, set it to zero and set the length_change to negative the previous note length
                            note.length = 0
                            length_change = -note.length
                            
                        # If making the note shorter, fill up the space
                        if length_change < 0:                    
                            # Decide if the note should be split
                            r_split = rnd.random()
                            if r_split < self.pause_probability:
                                new_note_pitch = note.pitch
                                new_note_length = -length_change
                                new_note_beat = note.beat + note.length
                                new_note = Note(new_note_pitch, new_note_length, new_note_beat)
                                mutated_chromosome.append(new_note)
                            # If not splitting, add pause for the rest
                            else:
                                new_note_pitch = None
                                new_note_length = -length_change
                                new_note_beat = note.beat + note.length
                                new_note = Note(new_note_pitch, new_note_length, new_note_beat)
                                mutated_chromosome.append(new_note)
                                current_beat += note.length + new_note.length
                else:
                    mutated_chromosome.append(note)
            current_beat += note.length
            ind += 1
        return mutated_chromosome
        
    
    def calculate_fitness(self, population):
        """Calculate the fitness for each chromosome and return an array
        with the fitness values
        """
        fitness_values = np.zeros(self.population_size)        
        for iPop in range(self.population_size):
            melody = population[iPop]
            fitness = 0
            for iNote in range(len(melody)):
                if melody[iNote].pitch == None:
                    fitness += 4*melody[iNote].length*1
                else:
                    fitness += (4*melody[iNote].length * 10*abs(melody[iNote].pitch))/self.nr_bars
            if fitness == 0:
                fitness_values[iPop] = 2
            else:
                fitness_values[iPop] = 1/fitness
        
        return fitness_values
    
    
    
    def insert_best_individual(self, tmp_population, best_individual):
        """Insert the individual with highest fitness in the previous
        generation to the new generation.
        """
        
        for i in range(self.nr_copies):
            tmp_population[i] = best_individual

        return tmp_population