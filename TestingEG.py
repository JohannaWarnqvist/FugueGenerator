from Scale import Scale
from EvolutionaryGenerator import EvolutionaryGenerator
from mingus.core import *
from mingus.containers import *

key = "C"

eg = EvolutionaryGenerator(key, fitness_function = 'C')

#eg = EvolutionaryGenerator(key, nr_bars = 2, fitness_function = 'pauses', global_max = 2)
eg.run_evolution()

print(eg.max_fitness_value)
print(eg.best_individual)

#note = eg.mutate_pitch(NoteContainer('C-5'))
#print(note)

#print(eg.population)