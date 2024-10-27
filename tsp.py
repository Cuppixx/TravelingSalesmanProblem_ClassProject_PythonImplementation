# pylint: skip-file
from itertools import permutations
import math
import random
import time


def load_distances():
    distancesFile = open("tspfiles/citiesAndDistances.txt")
    cities = distancesFile.readline().split()
    del cities[16:]
    numCities = len(cities)

    cityDistances = [[0.0] * numCities for i in range(numCities)]

    for i in range(numCities):
        distances = distancesFile.readline().split()
        del distances[0]
        del distances[16:]
        for j in range(len(distances)):
            cityDistances[i][j] = int(distances[j])
    return (cities,cityDistances)


def measure_path_length(p, distances):
    length = 0
    for i in range(len(p)):
        length += distances[p[i-1]][p[i]]
    return length


def random_walk(maximalNoOfCities, iterations = 1000000):
    shortestTourLength = sum([sum(i) for i in distances])

    for j in range(iterations):
        p=list(range(maximalNoOfCities))
        random.shuffle(p)

        tourLength = measure_path_length(p, distances)

        if tourLength < shortestTourLength:
            shortestTourLength =tourLength
            shortestTour = p

            shortestTourCities = [cities[i] for i in shortestTour]
            print(f"iteration: {j} tour: {shortestTourCities} length: {shortestTourLength}")

        elif j % 100000 == 0:
            print(f"iteration: {j}")


def brute_force(maximalNoOfCities):
    
    time_start = time.perf_counter()
    num_cities = maximalNoOfCities
    shortest_tour_length = float('inf')
    shortest_tour = None

    for perm in permutations(range(num_cities)):
        tour_length = measure_path_length(perm, distances)
        if tour_length < shortest_tour_length:
            shortest_tour_length =tour_length
            shortest_tour = perm

    shortest_tour_cities = [cities[i] for i in shortest_tour]
    time_end = time.perf_counter()

    print(f"Shortest tour found by brute force: {shortest_tour_cities} with length: {shortest_tour_length}")
    print(f"Got the optimal Tour for {maximalNoOfCities} cities in {time_end - time_start} seconds")	


def two_opt_xchg(tour, i, k):
    xchg_tour = tour[:i] + list(reversed(tour[i:k+1])) + tour[k+1:]
    return xchg_tour


def two_opt_step(tour, distances):
    num_cities = len(tour)
    shortest_length = measure_path_length(tour, distances)
    evaluated_lengths = 0

    improvement = True

    while improvement:
        improvement = False
        for i in range(num_cities - 2):
            for k in range(i + 2, num_cities):

                new_tour = two_opt_xchg(tour.copy(), i, k)
                new_length = measure_path_length(new_tour, distances)
                evaluated_lengths += 1

                if new_length < shortest_length:
                    shortest_length =new_length
                    tour = new_tour
                    improvement = True
                    break

            if improvement: 
                break

    return tour, shortest_length, evaluated_lengths


def hill_climber(distances, maximalNoOfCities):
    start_time = time.perf_counter()

    random_tour = list(range(maximalNoOfCities))
    random.shuffle(random_tour)
    print(f"Random Tour: {random_tour}")

    current_tour = random_tour.copy()
    current_length = measure_path_length(current_tour, distances)
    evaluated_lengths = 0

    while True:
        improved = False
        new_tour, new_length, evaluations = two_opt_step(current_tour.copy(), distances)
        evaluated_lengths += evaluations

        if new_length < current_length:
            current_tour, current_length = new_tour, new_length
            improved = True
            
        if not improved: break

    end_time = time.perf_counter()
    computation_time = end_time - start_time

    return current_length, evaluated_lengths, computation_time


def compute_with_2opt(maximalNoOfCities):
    (cities, distances) = load_distances()

    evaluated_lengths_array = []
    computation_times_array = []

    for n in range(5):
        tour_length, evaluated_lengths, computation_time = hill_climber(distances, maximalNoOfCities)
        evaluated_lengths_array.append(evaluated_lengths)
        computation_times_array.append(computation_time)

        print(f"For {maximalNoOfCities} cities:")
        print(f"Shortest tour length found by 2-opt hill climber: {tour_length}")
        print(f"Number of evaluated tour lengths: {evaluated_lengths}")
        print(f"Computation time: {computation_time} seconds\n\n")

    average_evaluated_lengths = sum(evaluated_lengths_array) / len(evaluated_lengths_array)
    average_computation_time  = sum(computation_times_array) / len(computation_times_array)

    print(f"Average evaluated tour lengths: {average_evaluated_lengths}")
    print(f"Average computation time: {average_computation_time} seconds")


def node_exchange(tour):
    tour = list(tour)

    random_node1 = random.randint(0,len(tour)-1)
    random_node2 = random_node1

    while random_node2 == random_node1: 
        random_node2 = random.randint(0,len(tour)-1)

    temp=tour[random_node1]
    tour[random_node1]=tour[random_node2]
    tour[random_node2]=temp

    return tour


def node_insertion(tour):
    tour = list(tour)

    random_node1 = random.randint(0,len(tour)-1)
    random_node2 = random_node1

    while random_node2 == random_node1: 
        random_node2 = random.randint(0,len(tour)-1)

    node_value = tour[random_node1]
    tour.pop(random_node1)
    tour.insert(random_node2,node_value)

    return tour


def simulated_annealing(distances, maximalNoOfCities, initial_temperature=1000, cooling_rate=0.999, stopping_temperature=0.01):
    random_tour = list(range(maximalNoOfCities))
    random.shuffle(random_tour)

    print(f"Random Tour: {random_tour}")

    current_tour, current_length = list(random_tour), measure_path_length(current_tour, distances)
    temperature = initial_temperature
    evaluated_lengths = 0

    start_time = time.perf_counter()

    exchange, insertion, xchg = 0

    while temperature > stopping_temperature:
        perturbation_operator = random.randint(0,2)
        match perturbation_operator:
            case 0:
                exchange += 1
                new_tour = node_exchange(list(current_tour))

            case 1:
                xchg += 1
                i = random.randint(0,len(current_tour)-2)
                new_tour = two_opt_xchg(list(current_tour), i, random.randint(i+1,len(current_tour)-1))

            case 2:
                insertion += 1
                new_tour = node_insertion(list(current_tour))
                
            case _: 
                new_tour = node_insertion(list(current_tour))

        new_length = measure_path_length(new_tour, distances)

        evaluated_lengths += 1
        delta_length = new_length - current_length

        if delta_length < 0 or random.random() < math.exp(-delta_length / temperature):
            current_tour, current_length = list(new_tour), new_length

        temperature *= cooling_rate

    print(f"--Simmulated Annealing--\nPicked Exchange {exchange} times\nPicked Insertion {insertion} times\nPicked xchg {xchg} times")

    end_time = time.perf_counter()
    computation_time = end_time - start_time

    return current_length, evaluated_lengths, computation_time


def compute_with_simulated_annealing(maximalNoOfCities):
    cities, distances = load_distances()

    evaluated_lengths_array = []
    computation_times_array = []

    for n in range(5):
        tour_length, evaluated_lengths, computation_time = simulated_annealing(distances, maximalNoOfCities)
        evaluated_lengths_array.append(evaluated_lengths)
        computation_times_array.append(computation_time)

        print(f"For {maximalNoOfCities} cities:")
        print(f"Shortest tour length found by Simulated Annealing: {tour_length}")
        print(f"Number of evaluated tour lengths: {evaluated_lengths}")
        print(f"Computation time: {computation_time} seconds\n\n") 

    average_evaluated_lengths = sum(evaluated_lengths_array) / len(evaluated_lengths_array)
    average_computation_time  = sum(computation_times_array) / len(computation_times_array)

    print(f"Average evaluated tour lengths: {average_evaluated_lengths}")
    print(f"Average computation time: {average_computation_time} seconds")


#MAIN/////////////////////////////////////////////////////////////////////////
maximalNoOfCities=int(input("Enter the maximal number of cities: "))

(cities, distances) = load_distances()
#print(cities[:maximalNoOfCities])
#print(distances)

#random_walk()
#brute_force(maximalNoOfCities)
#compute_with_2opt(maximalNoOfCities)
compute_with_simulated_annealing(maximalNoOfCities)
