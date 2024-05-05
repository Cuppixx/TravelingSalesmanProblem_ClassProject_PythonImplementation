from itertools import permutations
from random import shuffle
import random
import time

# load the distnace matrix from file
def loadDistances():
	distancesFile = open("citiesAndDistances.txt")
	cities = distancesFile.readline().split()
	del cities[16:]
	numCities = len(cities)
	
	# create an empty 2-dimensional matrix
	cityDistances = [[0.0] * numCities for i in range(numCities)]
	
	# for all cities:
	for i in range(numCities):
		distances = distancesFile.readline().split()
		del distances[0]
		del distances[16:]
		for j in range(len(distances)):
			cityDistances[i][j] = int(distances[j])
	return (cities,cityDistances)

# compute for a permutation of city names p the trip length
# compute first the distance form the last to the first city
# then add the distance from the first to the second city,...
# and finally, add the distance from the second last to the last city
#
def measurePath(p, distances):
	length = 0
	for i in range(len(p)):
		length += distances[p[i-1]][p[i]]
	return length

# example implementation of the random walk algorithm
# consider only cities from 0 to maximalNoOfCities
def random_walk(maximalNoOfCities, iterations = 1000000):
	
	# get the longest trip length for an upper bound
	# sum up all distances of a 2-dimensional list
	shortestTourLength = sum([sum(i) for i in distances])
	
	# for one million steps do: randomly sample a tour and compute the 
	# length. if better tour found, remember it
	for j in range(iterations):
		
		# sample random permutation
		p=list(range(maximalNoOfCities))
		shuffle(p)
		
		# measure path length
		tourLength = measurePath(p, distances)
		
		# if new path is shorter than the old best path, remember the new path
		if tourLength < shortestTourLength:
			shortestTourLength = tourLength
			shortestTour = p
			
			#print the new shortest path
			shortestTourCities = [cities[i] for i in shortestTour]
			print("iteration: {} tour: {} length: {}".format(j,shortestTourCities, shortestTourLength))
		
			# do some status printing from time to time
		elif j % 100000 == 0:
			print('iteration: {}'.format(j))	

def brute_force(maximalNoOfCities):
    time_start = time.perf_counter()
    num_cities = maximalNoOfCities
    shortest_tour_length = float('inf')
    shortest_tour = None
    
    # Generate all permutations of city indices
    for perm in permutations(range(num_cities)):
        tour_length = measurePath(perm, distances)
        #print("Tour found by brute force: {} with length: {}".format([cities[i] for i in perm], tour_length))
        # Update shortest tour if the current tour is shorter
        if tour_length < shortest_tour_length:
            shortest_tour_length = tour_length
            shortest_tour = perm
            
    shortest_tour_cities = [cities[i] for i in shortest_tour]
    print("Shortest tour found by brute force: {} with length: {}".format(shortest_tour_cities, shortest_tour_length))
    time_end = time.perf_counter()
    print("Got the optimal Tour for {} cities in {} seconds".format(maximalNoOfCities,time_end - time_start))	

def two_opt_xchg(tour, i, k):
    #print(tour)
    new_tour = tour[:i] + list(reversed(tour[i:k+1])) + tour[k+1:]
    #print(new_tour)
    return new_tour

def two_opt_step(tour, distances):
    num_cities = len(tour)
    shortest_length = measurePath(tour, distances)
    evaluated_lengths = 0
    
    improvement = True
    while improvement:
        improvement = False
        for i in range(num_cities - 2):
            for k in range(i + 2, num_cities):
                new_tour = two_opt_xchg(tour, i, k)
                new_length = measurePath(new_tour, distances)
                evaluated_lengths += 1
                if new_length < shortest_length:
                    shortest_length = new_length
                    tour = new_tour
                    improvement = True
                    break  # Start inner loop again with the updated tour
            if improvement:
                break  # Start outer loop again with the updated tour
    
    return tour, shortest_length, evaluated_lengths

def hill_climber(distances):
    random_tour = list(range(len(distances)))
    random.shuffle(random_tour)
    print("Random Tour: {}".format(random_tour))
    start_time = time.perf_counter()
    
    current_tour = random_tour
    current_length = measurePath(current_tour, distances)
    evaluated_lengths = 0
    
    while True:
        improved = False
        new_tour, new_length, evals = two_opt_step(current_tour, distances)
        evaluated_lengths += evals
        if new_length < current_length:
            current_tour = new_tour
            current_length = new_length
            improved = True
        if not improved:
            break
    
    end_time = time.perf_counter()
    computation_time = end_time - start_time
    
    return current_length, evaluated_lengths, computation_time

def compute_with_2opt(maximalNoOfCities):
    # Load the distance matrix and city names
    (cities, distances) = loadDistances()
    
    # Perform 2-opt hill climber for the given number of cities
    tour_length, evaluated_lengths, computation_time = hill_climber(distances)
    
    print(f"For {maximalNoOfCities} cities:")
    print(f"Shortest tour length found by 2-opt hill climber: {tour_length}")
    print(f"Number of evaluated tour lengths: {evaluated_lengths}")
    print(f"Computation time: {computation_time} seconds")
    

#MAIN/////////////////////////////////////////////////////////////////////////
maximalNoOfCities=int(input("Enter the maximal number of cities: "))

# load the distance matrix and city names
(cities, distances) = loadDistances()

# print city names
#print(cities[:maximalNoOfCities])

# print distance matrix
#print(distances)


#random_walk(maximalNoOfCities)
brute_force(maximalNoOfCities)
for n in range(1):
    compute_with_2opt(maximalNoOfCities)



