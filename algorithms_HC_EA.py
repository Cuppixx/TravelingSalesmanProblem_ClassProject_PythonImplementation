# pylint: skip-file
from city import distance
import time
import random


def calc_tour_length(tsp, tour):
    cities = tsp["CITIES"]
    length = 0
    for i in range(tsp["DIMENSION"]):
        length += distance(cities[tour[i - 1]], cities[tour[i]])
    return length


def node_xchg_step(tour):
    i = random.randint(0, len(tour) - 1)
    k = random.randint(0, len(tour) - 1)
    tour[i], tour[k] = tour[k], tour[i]
    return tour


def HC_tour(tsp, max_iterations):
    start_time = time.time()
    tour = [i for i in range(tsp["DIMENSION"])]

    random.shuffle(tour)
    tour_len = calc_tour_length(tsp, tour)
    visited_tours = 1

    # best solution found so far
    best_tour = tour
    best_tour_len = tour_len

    # iterate max_iterations times
    while visited_tours < max_iterations:
        # derive a new tour
        new_tour = node_xchg_step(list(best_tour))
        new_tour_len = calc_tour_length(tsp, new_tour)
        visited_tours += 1

        # found a better one?
        if new_tour_len < best_tour_len:
            print('improved from', best_tour_len, 'to', new_tour_len, 'by', best_tour_len-new_tour_len, 'visited tours', visited_tours)
            best_tour = new_tour
            best_tour_len = new_tour_len

    time_consumed = time.time()-start_time
    print('time consumed', time_consumed, 'tours visited', visited_tours, 'number of tours per second', visited_tours/time_consumed)
    return (best_tour_len)


def calc_HC_tour(tsp):
    return HC_tour(tsp, 100000)


# EA implementation for p2
def initialize_population(tsp, population_size):
    population = []
    for _ in range(population_size):
        tour = [i for i in range(tsp["DIMENSION"])]
        random.shuffle(tour)
        population.append(tour)
    return population


def select_individuals(tsp, population, k):
    tournament = random.choices(population, k=k)
    tournament.sort(key=lambda tour: calc_tour_length(tsp, tour))  
    return tournament[0], tournament[1]


def order_crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [None]*size
    child[start:end] = parent1[start:end]
    p2_index = end
    c_index = end
    while None in child:
        if parent2[p2_index] not in child:
            child[c_index] = parent2[p2_index]
            c_index = (c_index + 1) % size
        p2_index = (p2_index + 1) % size
    return child


def partially_mapped_crossover(parent1, parent2):
    size = len(parent1)
    offspring1 = [-1] * size
    
    start, end = sorted(random.sample(range(size), 2))
    
    offspring1[start:end+1] = parent1[start:end+1]
    
    def map_segment(offspring, parent, other_parent):
        for i in range(start, end + 1):
            if other_parent[i] not in offspring:
                current_value = other_parent[i]
                position = i
                while offspring[position] != -1:
                    position = other_parent.index(parent[position])
                offspring[position] = current_value
    
    map_segment(offspring1, parent1, parent2)
    
    def fill_rest(offspring, parent):
        for i in range(size):
            if offspring[i] == -1:
                offspring[i] = parent[i]
    
    fill_rest(offspring1, parent2)
    
    return offspring1


def swap_mutation(route):
    idx1, idx2 = random.sample(range(len(route)), 2)
    route[idx1], route[idx2] = route[idx2], route[idx1]
    return route


def inversion_mutation(route):
    idx1, idx2 = sorted(random.sample(range(len(route)), 2))
    route[idx1:idx2] = reversed(route[idx1:idx2])
    return route


def create_child(selected_population, recombination_op, mutation_op):
    parent1, parent2 = random.sample(selected_population, 2)
    
    match recombination_op:
        case 0: child = order_crossover(parent1, parent2)
        case 1: child = partially_mapped_crossover(parent1, parent2)

    if random.randint(0, 100) < 25: # Change the probability that a mutation is applied to the child (def: 25)
        match mutation_op:
            case 0: child = swap_mutation(child)
            case 1: child = inversion_mutation(child)
 
    return child


def create_offspring(selected_population, population_size):
    new_population = []
    while len(new_population) < population_size:
        new_population.append(create_child(selected_population, 1, 1)) # Change the recombination and mutation operators used (def: 1 and 1)
    
    return new_population


def evaluate_fitness(tsp, population):
    fitness_values = []
    for tour in population:
        fitness = calc_tour_length(tsp, tour)
        fitness_values.append(fitness)
    return fitness_values


def get_best_tour(population, tsp):
    fitness_values = evaluate_fitness(tsp, population)
    best_index = fitness_values.index(min(fitness_values))
    best_tour = population[best_index]
    return best_tour


def EA_tour(tsp, population_size, max_generations):
    start_time = time.time()

    population = initialize_population(tsp, population_size)

    for generation in range(max_generations):
        min_k = population_size / 2 # Change the minimum value of k aka the min amount of individuals viewed by the tournament selection (def: 2)
        k = max(int((1 - generation / max_generations) * population_size), int(min_k))

        selected_population = select_individuals(tsp, population, k)
        population = create_offspring(selected_population, population_size)

    time_consumed = time.time()-start_time
    print('time consumed', time_consumed)
    return calc_tour_length(tsp, get_best_tour(population, tsp))


def calc_EA_tour(tsp):
    print("--> Calc EA Tour now!")
    return EA_tour(tsp, 30, 3500) # Change population size (def: 30) and max generation (def: 3500; max: 100.000)


def calc_EA_tour_txt(tsp):
    file = open("bestresults.txt", "w")
    runs = 30
    tour_len_sum = 0
    for i in range(runs):
        best_tour_len = calc_EA_tour(tsp)
        print("EA LENGTH RUN",i+1,":        {}".format(best_tour_len),"\n")
        file.write(str(best_tour_len))
        file.write("\n")
        tour_len_sum += best_tour_len
    avg_tour_len = round(tour_len_sum/runs, 2)
    return avg_tour_len
