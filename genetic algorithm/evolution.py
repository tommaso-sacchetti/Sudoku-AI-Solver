import random
import time
import signal
import sys
import os

import sudoku

TOURNEY_SIZE = 3
POP_SIZE = 20000

class Evolution:

    def __init__(self, fitness_function, genome, local_size=10, verbose=True):
        """local_size: Size of the local neighbourhood.
        The population is a circular list where solutions only compete against nearby solutions.
        Makes convergence slower. Crossover more likely to give fit solutions when made between similar genomes."""

        self.fitness_function = fitness_function
        self.population = []
        self.first_genome = genome
        self.verbose = verbose
        self.local_size = local_size

        self.iterations = 0
        self.pop_size = POP_SIZE
        self.tourney_size = TOURNEY_SIZE
        self.best_found = 0
        self.best_genome = None
        self.best_fitness = 0
        self.last_eden = 0
        self.userstop = False
        self.file_bestfit_iterations = open("bestfit_iterations.txt", "a")
        self.file_bestfit_time = open("bestfit_time.txt", "a")
        self.start_time = time.time()

        self.eden_state()

    def _check_best(self, genome):
        """Calculate fitness of genome and check if it is the best found so far
        """
        genome.fitness = self.fitness_function(genome)

        if genome.fitness < self.best_fitness or self.best_genome is None:
            self.best_fitness = genome.fitness
            self.best_genome = genome.copy()
            self.best_found = self.iterations - self.last_eden
            if self.verbose:
                print("Best fitness: %d\tNumber of iterations: %d\n\n" %(self.best_fitness, self.iterations))
                sudoku.print_sudoku(sudoku.splitup(genome.genes))

        self.file_bestfit_iterations.write(str(self.best_fitness) + ' ' + str(self.iterations) + '\n')

        self.file_bestfit_time.write(str(self.best_fitness) + ' ' + str(time.time() - self.start_time) + '\n')

        # sudoku.clear()

    def eden_state(self):
        """Kill the population and create a new random population
        """
        self.best_fitness = 0
        self.last_eden = self.iterations
        self.best_genome = None
        self.population = []

        for _ in range(self.pop_size):
            self.population.append(self.first_genome.fresh())

        for element in self.population:
            self._check_best(element)

        # Orders the population by the fitness function (computationally expensive but it's una tantum in case the eden_state is called just at the beginning of the runtime)
        # self.population.sort(key = lambda x: x.fitness)

    def tourney_selection_local(self):
        if not self.local_size:
            return [random.randrange(len(self.population))
                    for _ in range(self.tourney_size)]

        midpoint = random.randrange(len(self.population))
        chosen_competitors = [midpoint]
        for _ in range(self.tourney_size - 1):
            i = midpoint + random.randrange(-self.local_size, self.local_size)
            i %= len(self.population) #works for negative too!
            chosen_competitors.append(i)
        
        competitors_id = [(self.population[i].fitness, i) for i in chosen_competitors]

        competitors_id.sort() # Sort it by the fitness

        self.population[competitors_id[-1][1]] = self._make_child(competitors_id[0][1], competitors_id[1][1]) # sobsitutes the worst element of the tourney with the new child

        self._check_best(self.population[competitors_id[-1][1]])

    def tourney_selection(self):
        # Randomly choose TOURNEY_SIZE elements and make them compete
        chosen_competitors = [random.randrange(len(self.population)) for _ in range(self.tourney_size)]

        competitors_id = [(self.population[i].fitness, i) for i in chosen_competitors]

        competitors_id.sort() # Sort it by the fitness

        self.population[competitors_id[-1][1]] = self._make_child(competitors_id[0][1], competitors_id[1][1]) # sobsitutes the worst element of the tourney with the new child

        self._check_best(self.population[competitors_id[-1][1]])

    def elite_selection(self):
        if random.random() > 0.75:
            self.population[-1] = self._make_child(0,1) # sobsitute the last element with the child of the two best
        else:
            self.population[-1] = self._make_child(0, random.randrange(len(self.population)))
        self._check_best(self.population[-1])
        self.population.sort(key = lambda x: x.fitness)

    def _make_child(self, id1, id2):
        return self.population[id1].spawn(self.population[id2])

    def evolve(self, target_fitness=None, use_restarts=True):
        """Evolve for a number of seconds
        
        use_restarts (true per default): the method restards after numerous iterations without improvements"""

        self.userstop = False
        def stop(signum, frame):
            """A Ctrl-C signal handler"""
            self.userstop = True
            if self.verbose:
                print('\n**Exiting**\n')
            
        oldhandler = signal.signal(signal.SIGINT, stop)

        try:
            while not self.userstop and self.best_fitness > target_fitness or target_fitness is None:
                
                # Restart in case the iterations from the last eden are too many
                """
                max_inactive = max(self.best_found * 2, self.pop_size * 10)
                thisrun = self.iterations - self.last_eden
                if use_restarts and thisrun > max_inactive:
                    if self.verbose:
                        print("\n\n**Restarting**\n\n")
                    self.eden_state() 
                """
                self.iterations += 1
                
                # IMPLEMENT TOURNAMENT AND ELITE SELECTION, CHECK FOR THE MAX_INACTIVE SWITCHING FROM ITERATIONS TO GENERATIONS

                # self.tourney_selection()

                # self.elite_selection()

                self.tourney_selection_local()
        finally: 
            signal.signal(signal.SIGINT, oldhandler)
            self.file_bestfit_iterations.close()
            self.file_bestfit_time.close()

        self.file_bestfit_iterations.close()
        self.file_bestfit_time.close()