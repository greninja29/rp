import random
iteration = 1
target = 9

# 1. Generate a random solution for the problem and call it S
def generate_random_solution(array, length):
    indices = sorted(random.sample(range(len(array)), length))
    return [array[i] for i in indices]

# 2. ~~~Compute the neighborhood of S~~~ and choose S' as the best solution in the neighborhood
def get_neighborhood_1(array, subset):
    neighborhood = []
    # neighbours with one element less
    if len(subset) > 1:
        for index, item in enumerate(subset):
            neighborhood.append(subset[:index] + subset[index+1:])
    
    # neighbours with one element more
    if len(subset) < len(array):
        for item in array:
            if item not in subset:
                neighborhood.append(subset + [item])

    return neighborhood

def get_neighborhood_2(array, subset):
    neighborhood = []
    # replace every element in subset with one element from set
    for index, subset_item in enumerate(subset):
        for set_item in array:
            if set_item not in subset:
                neighborhood.append(subset[:index] + [set_item] + subset[index+1:])

    return neighborhood

# 2. Compute the neighborhood of S and ~~~choose S' as the best solution in the neighborhood~~~
def choose_best_sol_in_neighborhood(neighborhood):
    s_prime = []
    if neighborhood:
        s_prime = neighborhood[0]

        for item in neighborhood:
            if abs(sum(item)-target) < abs(sum(s_prime)-target):
            # if sum(item) <= sum(s_prime) and sum(item)>=target:
                s_prime = item
    return s_prime

# 3. If S' is better than S then go to step 4, else go to step 6
# returns True if S' is better, False otherwise
def compare_solutions(s, s_prime):
    if s_prime:
        return abs(sum(s_prime)-target) < abs(sum(s)-target)
        # return sum(s_prime) >= target
    else:
        return False

# Calls steps 2, 3 and does the rest:
# 4. S = S'
# 5. Go to step 2
# 6. Return S as the best solution encountered
def neighborhood_search(array, s):
    if sum(s) == target:
        return s

    global iteration
    print ("\n~~~Iteration: {}~~~".format(iteration))

    # Step 2
    s_neighborhood_1 = get_neighborhood_1(array, s)
    s_neighborhood_2 = get_neighborhood_2(array, s)
    s_neighborhood = s_neighborhood_1 + s_neighborhood_2
    print ("Neighborhood: ", s_neighborhood)
    s_prime = choose_best_sol_in_neighborhood(s_neighborhood)
    print ("Best solution in the neighborhood: \n", s_prime, sum(s_prime))

    # Step 3
    if compare_solutions(s, s_prime):
        # Step 4 and 5
        print( "S' is better than S")
        iteration += 1
        return neighborhood_search(array, s_prime)
    else:
        # Step 6
        return s

def neighbour_search(array,t):
    global target
    target = t
    s = generate_random_solution(array, random.randint(1, len(array)))
    # print ("Random solution: ", s, sum(s))
    s_final = neighborhood_search(array, s)
    print( "Final solution: ", s_final, sum(s_final))
    return s_final


if __name__ == "__main__":
    # Step 1
    # array = [-7, -3, -2, 5, 8, 3, 2, -1, 10, -6, 4, 7, 9, -8, 1, 6, -4, -5, -9, -10, 0, 11, -11, 12, -12, 13, -13, 14, -14, 15, -15, 16, -16, 17, -17, 18, -18, 19, -19, 20, -20]
    array = [3, 34, 4, 12, 5, 2] 
    s = generate_random_solution(array, random.randint(1, len(array)))
    
    print ("Random solution: ", s, sum(s))
    s_final = neighborhood_search(array, s)

    print( "Final solution: ", s_final, sum(s_final))
    
    
    