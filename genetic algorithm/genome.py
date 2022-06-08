import random
import copy

COPY_CHANCE = 1
FRESH_CHANCE = 1
CROSSOVER_CHANCE = 5
SWAP_CHANCE = 3

class Genome:
    """In this solution a genome is encoded as a list of elements and since in the sudoku problem the values appear the same number of times, as operations we will consider only operations that execute permutations within the elements of the gene.
    """
    
    def __init__(self, initial, spawn_chances=None):
        """The array spawn_chances is in the form of [(spawn_method, spawn_probability),(spawn_method2, spawn_probability2),...]"""

        """Spawn chances are decidable in the variables, the operations implemented and possible as spawn are: copy [copies the current genes], fresh [creates fresh genes], crossover [executes a crossover between the two parents] and swap [randomly swaps two values inside of the genes: it's considered as a random mutation of the genetic code]"""

        self.spawn_chances = ((Genome.copy, COPY_CHANCE),
                         (Genome.fresh, FRESH_CHANCE),
                         (Genome.crossover, CROSSOVER_CHANCE),
                         (Genome.swap, SWAP_CHANCE))

        self.genes = copy.copy(initial)
        self.total_target = sum(chance for _, chance in self.spawn_chances) # The total of   chances
        self.partner = None

    def spawn(self, partner):
        """Uses a partner to spawn a new child (it could potentially not use the partner's genetic code, in the case of the copy, fresh or mutation"""
        self.partner = partner
        rnd = random.randrange(self.total_target)
        i = 0
        for spawn_function, spawn_chance in self.spawn_chances:
            if rnd < i + spawn_chance:
                child = spawn_function(self)
                break
            i += spawn_chance

        del self.partner # memory purpose
        return child

    def copy(self, genes=None):
        # Maybe could be useful to initialize genes
        return Genome(self.genes, self.spawn_chances)
    
    def fresh(self):
        child = self.copy()
        random.shuffle(child.genes) # shuffles the list of values
        return child

    def swap(self):
        child = self.copy()
        i = random.randrange(len(child.genes))
        j = random.randrange(len(child.genes)) # There is not a control to check whether the two values are different, so there is a probability of 1/6561 of having a copy, let's just let nature and randomness do their thing
        child.genes[i], child.genes[j] = child.genes[j], child.genes[i]
        return child

    def crossover(self):
        genes1 = self.genes[:]
        genes2 = self.partner.genes[:]

        # Create a conflict vector that stores the position of the conflicts between the corresponding cells and fills the result array with nothing, in order to go back after the first cycle where equality is check.
        result = []
        i = 0
        conflicts = []
        while i < len(genes1):
            if genes1[i] == genes2[i]:
                result.append(genes1[i])
                genes1.pop(i)
                genes2.pop(i)
            else:
                conflicts.append(len(result))
                result.append(None)
                i += 1

        for i in conflicts:
            # 50% chance of using the first gene to choose the current value 
            if random.random() < 0.5:
                result[i] = genes1[0]
                genes2.remove(genes1.pop(0))
                # Remove the selected element from the gene1 and then removes the same element (a number in this sudoku case) from the second gene in order to keep the same quantity of equals figures inside of the gene representing the sudoku [it's necessary to permutate the values in every reproductive operation inside of this class]
            else:
                result[i] = genes2[0]
                genes1.remove(genes2.pop(0))

        return Genome(result, self.spawn_chances)   
        

        """
        result = []
        i = 0
        conflicts = []

        print("GENE1 SIZE: " + str(len(genes1)))
        print("GENE2 SIZE: " + str(len(genes2)))

        while i < len(genes1):
            print("INDEX: " + str(i))
            if genes1[i] == genes2[i]:
                result.append(genes1[i])
                genes1.pop(i)
                genes2.pop(i)
            else: 
                if random.random() < 0.5:
                    to_append = genes1[i]
                else: 
                    to_append = genes2[i]
                result.append(to_append)
                genes1.remove(to_append)
                genes2.remove(to_append)

        
        return Genome(result, self.spawn_chances)   
        
        print(conflicts)
        print(" CONFLICTS LENGTH: " + str(len(conflicts)))

        for conflict_position in conflicts:
            if random.random() < 0.5: 
                # 50% chance of using the first gene to choose the current value 
                result[conflict_position] = genes1[0]
                to_remove = genes1.pop(0)
                print("To remove: " + str(to_remove)) # Remove the selected element from the gene1 and then removes the same element (a number in this sudoku case) from the second gene in order to keep the same quantity of equals figures inside of the gene representing the sudoku [it's necessary to permutate the values in every reproductive operation inside of this class]

            else:
                result[conflict_position] = genes2[0]
                to_remove = genes2.pop(0)
                print("To remove: " + str(to_remove))
                genes1.remove(to_remove)
                # By popping we keep the memory clean and the index of the next element is always gonna be 0
            """ 
