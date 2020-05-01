import random as rnd
import numpy as np
import copy
import math
import copy
from mingus.core import *
from mingus.containers import *
import track_functions as Track_Functions

class EvolutionaryGenerator():

    def __init__(self, key, nr_bars = 2):
        "Initialize all the parameters"
        
        # When testing to regenerate same case:
        #rnd.seed(1)
        #np.random.seed(1)

        # == Parameters ==
        self.population_size = 2
        self.nr_generations = 2;
        
        self.probability_rest = 0.05
        
        self.crossover_probability = 0.8;
        self.mutation_probability = 1/(nr_bars*4);
        self.tournament_selection_parameter = 0.75;
        
        self.tournament_size = 2;
        self.nr_copies = 1;  
        
        self.pitch_probability = 0.5
        self.pause_probability = 0.5

        self.nr_bars = nr_bars
        self.key = key
        
        self.best_individual = None
        self.max_fitness_value = 0
        
        # Deciding here which note lengths that are allowed. Maybe should be done somewhere else?
        #self.possible_lengths = [1, 4/3, 2, 8/3, 4, 16/3, 8, 32/3, 16, 32]
        self.possible_lengths = [1, 2, 4, 8, 16]
        
        
    def run_evolution(self):
        
        # Initialize population
        self.population = self.initialize_population()
        
        
        fitness_values = np.zeros(self.population_size)
        self.max_fitness_value = 0
        for iGen in range(self.nr_generations):
            
            # == Calculate fitness and save best individual ==
            fitness_values = self.calculate_fitness(self.population)
            
            # Save a copy of the best individual
            best_individual_index = np.argmax(fitness_values)        
            self.best_individual = copy.deepcopy(self.population[best_individual_index])
            
            # Print best individual and its fitness value if better than before
            if fitness_values[best_individual_index] > self.max_fitness_value:
                print(f"Generation: {iGen}")
                print(f"Best individual: {self.best_individual}")
                print(f"Fitness: {fitness_values[best_individual_index]}")
                self.max_fitness_value = fitness_values[best_individual_index]
            
            # == Tournament selection ==
            tmp_population = []
            for i in range(self.population_size):
                index_selected = self.tournament_selection(fitness_values, self.tournament_selection_parameter, self.tournament_size)
                individual_selected = copy.deepcopy(self.population[index_selected])
                tmp_population.append(individual_selected)
            
            
            # == Crossover ==
            for iCross in range(0, self.population_size-1, 2):
                chromosome1 = self.population[iCross]
                chromosome2 = self.population[iCross + 1]
                
                r_cross = rnd.random()
                if r_cross < self.crossover_probability:
                    crossed_pair = self.cross_over([chromosome1, chromosome2])
                    tmp_population[iCross] = crossed_pair[0]
                    tmp_population[iCross + 1] = crossed_pair[1]
                
            # TODO: Add the rest of the algorithm when they are translated to mingus 
            """
            # == Mutation ==            
            for i in range(self.population_size):
                tmp_population[i] = self.mutate(tmp_population[i])
            
            
            # == Elitism ==            
            tmp_population = self.insert_best_individual(tmp_population, self.best_individual)
            
            
            # == Save generation ==
            self.population = tmp_population
        """
        
    
    def initialize_population(self, meter = (4,4), min_pitch = -12, max_pitch = 24):
        """Create the population consisting of the wanted number of
        randomly generated melodies.
        """
        population = []
        
        scale_tones = scales.get_notes(key = self.key)
        
        for i in range(self.population_size):
            melody = Track()            
            
            for i in range(self.nr_bars):
                bar = Bar(self.key, meter)
                while not bar.is_full():
                    #breakpoint()
                    # Decide length of a note. Maximum length is what is left of this bar.
                    length_left = 1 - bar.current_beat
                    
                    length = 0.5
                    while 1/length > length_left:
                        length = rnd.choice(self.possible_lengths)
                    
                    
                    # Decide pitch of a note                
                    r = rnd.random()
                    if r < self.probability_rest:
                        pitch_tone = None
                        # Add note to bar with the decided length                        
                        bar.place_rest(length)

                    else:
                        # Choose one random tone in the scale
                        note_letter = rnd.choice(scale_tones)
                        
                        # Choose one random octave, with more chance to get close to 4.
                        octave = round(np.random.normal(loc = 4, scale = 0.5))
                             
                        # Note: Might be problematic of a octave number that is too high or too low is chosen.
                        note = Note(note_letter, octave)
                                            
                        # Add note to bar with the decided length                        
                        bar.place_notes(note, length)

                # Add note to subject
                melody.add_bar(bar)
                
            population.append(melody)
        
        print(f"Initial population: {population}")
        return population
    
    def cross_over(self, chromosomes):
        """Change chromosome by using crossover between two chromosomes.
        It decides a beat to split and exchange tails after this beat
        between the two chromosomes.
        """
        
        # Decide at which semiquaver to cross
        nr_note_slots = self.nr_bars
        bar_to_break_in = rnd.randrange(nr_note_slots)
        beat_to_break_at = rnd.randrange(16)/16
        
        
        
        # Initialize list to save heads and tails of each chromosome      
        head_chromosome = [Track(),Track()]
        tail_chromosome = [Track(),Track()]
        # Place to save the half bars that should be part of tail
        end_head_chromosome = [Bar(), Bar()]
        start_tail_chromosome = [Bar(), Bar()]
        
        for iChrom in range(2):
            
            bar_nr = 0
            for bar in chromosomes[iChrom]:
                if bar_nr < bar_to_break_in:
                    head_chromosome[iChrom].add_bar(bar)
                
                elif bar_nr > bar_to_break_in:
                    tail_chromosome[iChrom].add_bar(bar)
                
                else:
                    if beat_to_break_at == 0:
                        tail_chromosome[iChrom].add_bar(bar)
                        bar_nr += 1
                        continue
                    
                    beat = 0
                    note_index = 0
                    note_pitch = bar[note_index][2]
                    note_duration = bar[note_index][1]
                    print(f"break beat: {beat_to_break_at}")
                    while beat < 1.0:
                        print(f"current beat = {beat}")
                        if beat + 1/bar[note_index][1] <= beat_to_break_at:
                            end_head_chromosome[iChrom].place_notes(note_pitch, note_duration)
                        
                        elif beat >= beat_to_break_at:
                            if beat == beat_to_break_at:
                                start_tail_chromosome[iChrom].current_beat = beat_to_break_at
                                
                            start_tail_chromosome[iChrom].place_notes(note_pitch, note_duration)
                        
                        else:                            
                            # Divide to one part from beat to breakpoint, and one the length left over starting at breakpoint
                            first_part_duration = 1/(beat_to_break_at - beat)
                            second_part_duration = 1/(1/note_duration - 1/first_part_duration)
                            
                            end_head_chromosome[iChrom].place_notes(note_pitch, first_part_duration)
                            start_tail_chromosome[iChrom].current_beat = beat_to_break_at
                            start_tail_chromosome[iChrom].place_notes(note_pitch, second_part_duration)
                        beat += 1/bar[note_index][1]
                        
                bar_nr += 1
        
        middle_bars = []
        cross_chromosomes = []
        for i in range(2):
        
            # Combine the two middle parts in the new way
            middle_bars.append(self.combine_bars(end_head_chromosome[i], start_tail_chromosome[1-i]))
        
            # Add the changed middlebar to the head_chromosome
            head_chromosome[i].add_bar(middle_bars[i])
                
            # Create a new chromosome by adding the new tail to the head
            Track_Functions.add_tracks(head_chromosome[i], tail_chromosome[1-i])
            new_chromosome = head_chromosome[i]
            
            # Add the new chromosome to the list to be returned
            cross_chromosomes.append(new_chromosome)
        
        
        
        
            """notes = chromosomes[iChrom].get_notes()
            for note in notes:
                if beat + (1/note[1]) < break_point:
                    # Testing
                    if note[1] < 0:
                        breakpoint()
                    
                    # Add the whole note to head
                    head_chromosome[iChrom].append(note)
                                
                elif beat < break_point:
                    # Split the note in two, with the first one in head and second in tail
                    
                    note1 = copy.deepcopy(note)
                    breakpoint()
                    print(note1)
                    
                    note1[1] = (1/(break_point-beat))
                    
                    note2 = copy.copy(note)
                    note2[1] = 1/((1/note[1]) - (1/note1[1]))
                    note2[0] = note1[0] + (1/note1[1])

                    # Testing
                    if note1[1] < 0 or note2[1] < 0:
                        breakpoint()
                    
                    head_chromosome[iChrom].append(note1)
                    tail_chromosome[iChrom].append(note2)
                
                else:
                    # Testing
                    if note[1] < 0:
                        breakpoint()
                    
                    # Add the whole note to tail
                    tail_chromosome[iChrom].append(note)
                    
                    
                beat += 1/note[1]
          
        # Create the new chromosomes by combining one chromosomes head with the other's tail.
        list_cross_chromosomes = [head_chromosome[0] + tail_chromosome[1], head_chromosome[1]+tail_chromosome[0]]
        
        cross_chromosomes = [Track(), Track()]
        for chromosome in list_cross_chromosomes:
            b = Bar()
            for note in chromosome:
                added = b.place_notes(note[2], note[1])
                if b.is_full:
                    chromosome.add_bar(b)
                    b = Bar()
        """
        
        return cross_chromosomes

    def combine_bars(self, bar1, bar2):
    
        new_bar = Bar()
        end_bar1 = bar1.current_beat
        start_bar2 = bar2[0][0]
        
        if end_bar1 > start_bar2:
            breakpoint()
            raise ValueError('Bars overlapping.')
        
        if end_bar1 < start_bar2:
            difference_duration = 1/(start_bar2 - end_bar1)
            bar1.place_rest(difference_duration)
            end_bar1 = bar1.current_beat
        
        # perfect combo
        if end_bar1 == start_bar2:
            for note in bar1:
                note_duration = note[1]
                note_type = note[2]
                
                if note_type is None:
                    new_bar.place_rest(note_duration)
                else:
                    new_bar.place_notes(note_type, note_duration)
                    
            for note in bar2:
                note_duration = note[1]
                note_type = note[2]
                
                if note_type is None:
                    new_bar.place_rest(note_duration)
                else:
                    new_bar.place_notes(note_type, note_duration)
        
        return new_bar

    
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


    # TODO: Translate to mingus
    def mutate(self, chromosome):
        """Mutate each gene with a certain probability. Can either split the note into two 
        notes of same pitch, shorten tone and add pause at the rest part or longer the note 
        and delete any notes that where there previously."""
        #mutate the note by either splitting, merging with next or shortening adding a pause

        breakpoint()
        mutated_chromosome = Track()
        nr_notes_in_chromosome = len(chromosome[1])
        self.mutation_probability = 2/nr_notes_in_chromosome
        
        notes = chromosome.get_notes()
        
        ind = 0
        current_beat = 0
        while ind < nr_notes_in_chromosome:
        
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
            notes = melody.get_notes()
            
            for note in notes:
                if note[-1] is None:
                        fitness += note[1]*1/self.nr_bars
                else:
                    distance = Note('C').measure(note[-1][0])
                    fitness += (note[1] * 10*abs(distance))/self.nr_bars

            if fitness == 0:
                fitness_values[iPop] = 2
            else:
                fitness_values[iPop] = 1/fitness
        
        return fitness_values
    
    
    # TODO: Translate to mingus
    def insert_best_individual(self, tmp_population, best_individual):
        """Insert the individual with highest fitness in the previous
        generation to the new generation.
        """
        
        for i in range(self.nr_copies):
            tmp_population[i] = best_individual

        return tmp_population