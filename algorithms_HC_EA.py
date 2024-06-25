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

# implementation of a hill climber
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

# implementation of an Evolutionary Algorithm
def EA_tour(tsp, population_size, max_generations):
    start_time = time.time()
    tour = [i for i in range(tsp["DIMENSION"])]
    random.shuffle(tour)
    tour_len = calc_tour_length(tsp, tour)




    time_consumed = time.time()-start_time
    print('time consumed', time_consumed)
    return (tour_len)


def calc_EA_tour(tsp):
    return EA_tour(tsp, 20, 5000)

def calc_EA_tour_txt(tsp):
    file = open("bestresults.txt", "w")
    runs = 30
    tour_len_sum = 0
    for i in range(runs):
        best_tour_len = calc_EA_tour(tsp)
        print("EA LENGTH RUN",i+1,":        {}".format(best_tour_len))
        file.write(str(best_tour_len))
        file.write("\n")
        tour_len_sum += best_tour_len
    avg_tour_len = round(tour_len_sum/runs, 2)
    return avg_tour_len
