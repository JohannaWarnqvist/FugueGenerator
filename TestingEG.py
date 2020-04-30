from Scale import Scale
from EvolutionaryGenerator import EvolutionaryGenerator

key = "C"

eg = EvolutionaryGenerator(key)
eg.run_evolution()

print(eg.max_fitness_value)
print(eg.best_individual)

#print(eg.population)