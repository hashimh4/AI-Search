import os
import sys
import time
import random

def read_file_into_string(input_file, ord_range):
    the_file = open(input_file, 'r') 
    current_char = the_file.read(1) 
    file_string = ""
    length = len(ord_range)
    while current_char != "":
        i = 0
        while i < length:
            if ord(current_char) >= ord_range[i][0] and ord(current_char) <= ord_range[i][1]:
                file_string = file_string + current_char
                i = length
            else:
                i = i + 1
        current_char = the_file.read(1)
    the_file.close()
    return file_string

def remove_all_spaces(the_string):
    length = len(the_string)
    new_string = ""
    for i in range(length):
        if the_string[i] != " ":
            new_string = new_string + the_string[i]
    return new_string

def integerize(the_string):
    length = len(the_string)
    stripped_string = "0"
    for i in range(0, length):
        if ord(the_string[i]) >= 48 and ord(the_string[i]) <= 57:
            stripped_string = stripped_string + the_string[i]
    resulting_int = int(stripped_string)
    return resulting_int

def convert_to_list_of_int(the_string):
    list_of_integers = []
    location = 0
    finished = False
    while finished == False:
        found_comma = the_string.find(',', location)
        if found_comma == -1:
            finished = True
        else:
            list_of_integers.append(integerize(the_string[location:found_comma]))
            location = found_comma + 1
            if the_string[location:location + 5] == "NOTE=":
                finished = True
    return list_of_integers

def build_distance_matrix(num_cities, distances, city_format):
    dist_matrix = []
    i = 0
    if city_format == "full":
        for j in range(num_cities):
            row = []
            for k in range(0, num_cities):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    elif city_format == "upper_tri":
        for j in range(0, num_cities):
            row = []
            for k in range(j):
                row.append(0)
            for k in range(num_cities - j):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    else:
        for j in range(0, num_cities):
            row = []
            for k in range(j + 1):
                row.append(0)
            for k in range(0, num_cities - (j + 1)):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    if city_format == "upper_tri" or city_format == "strict_upper_tri":
        for i in range(0, num_cities):
            for j in range(0, num_cities):
                if i > j:
                    dist_matrix[i][j] = dist_matrix[j][i]
    return dist_matrix

def read_in_algorithm_codes_and_tariffs(alg_codes_file):
    flag = "good"
    code_dictionary = {}   
    tariff_dictionary = {}  
    if not os.path.exists(alg_codes_file):
        flag = "not_exist"  
        return code_dictionary, tariff_dictionary, flag
    ord_range = [[32, 126]]
    file_string = read_file_into_string(alg_codes_file, ord_range)  
    location = 0
    EOF = False
    list_of_items = []  
    while EOF == False: 
        found_comma = file_string.find(",", location)
        if found_comma == -1:
            EOF = True
            sandwich = file_string[location:]
        else:
            sandwich = file_string[location:found_comma]
            location = found_comma + 1
        list_of_items.append(sandwich)
    third_length = int(len(list_of_items)/3)
    for i in range(third_length):
        code_dictionary[list_of_items[3 * i]] = list_of_items[3 * i + 1]
        tariff_dictionary[list_of_items[3 * i]] = int(list_of_items[3 * i + 2])
    return code_dictionary, tariff_dictionary, flag

input_file = "AISearchfile012.txt"

if len(sys.argv) > 1:
    input_file = sys.argv[1]

##### begin change 1 #####
the_particular_city_file_folder = "city-files"
path_for_city_files = "../" + the_particular_city_file_folder
##### end change 1   #####
    
if os.path.isfile(path_for_city_files + "/" + input_file):
    ord_range = [[32, 126]]
    file_string = read_file_into_string(path_for_city_files + "/" + input_file, ord_range)
    file_string = remove_all_spaces(file_string)
    print("I have found and read the input file " + input_file + ":")
else:
    print("*** error: The city file " + input_file + " does not exist in the folder '" + the_particular_city_file_folder + "'.")
    sys.exit()

location = file_string.find("SIZE=")
if location == -1:
    print("*** error: The city file " + input_file + " is incorrectly formatted.")
    sys.exit()
    
comma = file_string.find(",", location)
if comma == -1:
    print("*** error: The city file " + input_file + " is incorrectly formatted.")
    sys.exit()
    
num_cities_as_string = file_string[location + 5:comma]
num_cities = integerize(num_cities_as_string)
print("   the number of cities is stored in 'num_cities' and is " + str(num_cities))

comma = comma + 1
stripped_file_string = file_string[comma:]
distances = convert_to_list_of_int(stripped_file_string)

counted_distances = len(distances)
if counted_distances == num_cities * num_cities:
    city_format = "full"
elif counted_distances == (num_cities * (num_cities + 1))/2:
    city_format = "upper_tri"
elif counted_distances == (num_cities * (num_cities - 1))/2:
    city_format = "strict_upper_tri"
else:
    print("*** error: The city file " + input_file + " is incorrectly formatted.")
    sys.exit()

dist_matrix = build_distance_matrix(num_cities, distances, city_format)
print("   the distance matrix 'dist_matrix' has been built.")

##### begin change 2 #####
the_particular_alg_codes_and_tariffs = "alg_codes_and_tariffs.txt"
path_for_alg_codes_and_tariffs = "../" + the_particular_alg_codes_and_tariffs
##### end change 2   #####

code_dictionary, tariff_dictionary, flag = read_in_algorithm_codes_and_tariffs(path_for_alg_codes_and_tariffs)

if flag != "good":
    print("*** error: The text file 'alg_codes_and_tariffs.txt' does not exist.")
    sys.exit()

print("The codes and tariffs have been read from 'alg_codes_and_tariffs.txt':")

my_user_name = ""

my_first_name = ""
my_last_name = ""

algorithm_code = "US"

if not algorithm_code in code_dictionary:
    print("*** error: the algorithm code " + algorithm_code + " is illegal")
    sys.exit()
print("   your algorithm code is legal and is " + algorithm_code + " -" + code_dictionary[algorithm_code] + ".")

added_note = ""

############
############ NOW YOUR CODE SHOULD BEGIN.
############

# Depth first search (uniformed search)
# Goal: Find the shortest tour, whilst visiting all the cities

# Allows measuring the time passed, to ensure a tour is provided under a minute
import time

# Marks when the timer has started
start = time.time()

# We will be considering nodes in a search tree
# The state of a node
S = []
# The parent_id of the node
P = []
# The action which allowed us to go from our parent to the child node
tour = []
# The cumulative cost of the steps to the node
tour_length = []
# The depth of the node
D = []

# The node identifier (how many steps we have taken from our spot)
newID = 0
# Setting the initial state of the first node, which is simply our starting city (city 0)
S.append(0)
# Setting the root to have no parent, hence no action would have occurred
P.append(None)
# The action is the cities we have visited so far, at this node
tour.append([None])
# Setting the path-cost of the root node to zero. We will queue values from dist_matrix in the future
tour_length.append(0)
# Setting the depth of the root node to 0
D.append(0)

# An array to store our current best tour
current_tour_solution = []
# A variable to store the length of our best tour, currently holding an upper bound
current_tour_solution_length = 999999999999999999999999

# To tell us when to break from the loop
break_flag = False

# We are using stacks as we use the principle "last-in first-out" for depth first search
# I will use the word "list" interchangeably with "array"
# Our fringe is a queue of tuples, containing all our variables above, starting with only the root node
F = [(newID, S[0], P[0], tour[0], tour_length[0], D[0])]

# We define our goal state, which is a complete tour (a list) of all the cities
# Check whether the current state of the parent node is a goal state
if len(tour) == num_cities:
    tour = []
    tour_length = 0

# Continue with this code if our fringe is not empty
# It will not be empty when supplied data, since we have defined an empty start node
else:

    # Stop searching if our fringe is empty, as we would have visited the number of cities required
    while F:
        # print(F)

        # Break from the loop once the variable is set to true
        if break_flag == True:
            break

        # Creates an array to hold all the cities
        num_cities_array = []
        for i in range(1, num_cities + 1):
            num_cities_array.append(i)

        # The tour list at our node is taken away from the list containing all cities
        # This generates the children we are still able to visit
        if F[-1][3] != None:
            for i in F[-1][3]:
                if i in num_cities_array:
                    num_cities_array.remove(i)
        # The child nodes are the cities currently not in our tour
        child_city = num_cities_array

        # The new parent nodes are the previous children IDs
        new_parent_id = F[-1][1]
        # The current parent nodes
        parent_id = F[-1][2]
        # The length of the parent tour of the cities visited so far
        parent_tour_length = F[-1][4]
        # The depth of the parent node
        parent_depth = F[-1][5]

        # print(parent_id)

        # An array containing the tour of our parent node
        previous_tour = []
        if F[-1][3] != [None]:
            for i in F[-1][3]:
                previous_tour.append(i)

        # Removes the first tuple from our fringe tuple
        del F[-1]

        # Our successor state is simply seeking an unvisited city next or swapping our current city with another one
        for child in child_city:
            # Increase the unique identifier by one
            newID = newID + 1
            # Store each new child on the fringe
            S.append(child)
            # Store the new parent on the fringe
            P.append(new_parent_id)

            # Add the previous cities to the new tour list
            new_tour = []
            for i in previous_tour:
                new_tour.append(i)

            # If we have not visited a city yet, or we have only visited one city, simply add the child to the new tour
            if parent_id == None or parent_id == 0:
                new_tour.append(child)
            else:
                # If neither of the above, then add the city to the new tour
                # Kept as an if-else due to a previous possible alternative implementation (commented out)
                if parent_id != None:
                    # print(tour[parent_id])
                    # for i in tour[parent_id]:
                    #     new_tour_value = i
                    # new_tour.append(new_tour_value)
                    new_tour.append(child)
            # Add our new tour to our array of tours for each node
            tour.append(new_tour)

            # next_city = 0
            # This is set to false, since we have not encountered a tour with every city yet
            full_trip = False
            # The variable to calculate the length of our tour
            tour_length_calc = 0
            # The variable holding our current tour array
            tour_calc = tour[newID]

            # Evaluate the current tour to get the full length of the tour
            # If we have vistied one or no cities, then our tour length is 0
            if len(tour_calc) <= 1:
                tour_length_calc = 0
            else:
                # For a tour length that is greater than one and less than the total number of cities
                # Add the tour length of the parent and the distance from the parent to the new child
                if 1 < len(tour_calc) < num_cities:
                    tour_length_calc = parent_tour_length + dist_matrix[new_parent_id - 1][child - 1]
                # For a full round tour
                # Add the tour length of the parent and the distance from the parent to the new child
                # Also add the distance from the new child to the starting city
                if len(tour_calc) == num_cities:
                    full_trip = True
                    tour_length_calc = parent_tour_length + dist_matrix[new_parent_id - 1][child - 1]
                    original_city = new_tour[0]
                    tour_length_calc = tour_length_calc + dist_matrix[child - 1][original_city - 1]
                # Previous implementation which looped through every city in our current tour instead of the above
                # if 1 < len(tour_calc) < num_cities:
                #     for i in tour_calc:
                #         # To start on index 0
                #         i = i - 1
                #         # To find the city on the next index
                #         next_city = next_city + 1
                #         if next_city < len(tour_calc):
                #             tour_length_calc = tour_length_calc + dist_matrix[i][tour_calc[next_city]]
            # Add our calculated tour length to our tour length array for each node
            tour_length.append(tour_length_calc)

            # Evaluate the depth of the child node
            # Add one to the depth of the parent node
            D.append(parent_depth + 1)

            # If we have encountered a full tour, store the tour with the shortest distance
            if full_trip == True:
                if tour_length[newID] < current_tour_solution_length:
                    current_tour_solution = tour[newID]
                    current_tour_solution_length = tour_length[newID]
            # Break the loop and provide a tour if we go over 54 seconds of computation time
            if (time.time() - start) > 54:
                break_flag = True
                break

            # Otherwise, add the new node information to our fringe tuple if we have not met our goal
            # Add this if our current tour is nothing (for the very first node)
            # Or if our current tour includes one less than the complete number of cities
            if tour[newID] == None:
                F.append((newID, S[newID], P[newID], tour[newID], tour_length[newID], D[newID]))
            else:
                if len(tour[newID]) < num_cities:
                    F.append((newID, S[newID], P[newID], tour[newID], tour_length[newID], D[newID]))

    # Redefining tour as an empty list
    tour = []
    # Add our tour length to our tour_length variable
    tour_length = current_tour_solution_length
    # Add our calculated tour to our tour array
    for i in current_tour_solution:
        tour.append(i - 1)

# Testing our provided variables and arrays
# tour = [0,5,1,2,3,4,6,7,8,9,10,11]
# tour_length = 55
# print(num_cities) # Prints the number of cities
# print(dist_matrix[1][2]) # Prints the distance from city 1 to city 2
# print(tour) # Prints a list of integers, which has all the cities (as they must all be visited exactly once)

# An alternative implementation to calculate the tour_length, which was not used in the end
# # For each city, find the distance to the next one (if the next one exists)
# next_city = 0
# tour_length = 0
# for i in tour:
#     next_city = next_city + 1
#     if next_city < len(tour):
#         tour_length = tour_length + dist_matrix[i][tour[next_city]]
# # Ensure to add on the distance between the very last and first city, to get a full tour
# tour_length = tour_length + dist_matrix[tour[num_cities - 1]][tour[0]]

flag = "good"
length = len(tour)
for i in range(0, length):
    if isinstance(tour[i], int) == False:
        flag = "bad"
    else:
        tour[i] = int(tour[i])
if flag == "bad":
    print("*** error: Your tour contains non-integer values.")
    sys.exit()
if isinstance(tour_length, int) == False:
    print("*** error: The tour-length is a non-integer value.")
    sys.exit()
tour_length = int(tour_length)
if len(tour) != num_cities:
    print("*** error: The tour does not consist of " + str(num_cities) + " cities as there are, in fact, " + str(len(tour)) + ".")
    sys.exit()
flag = "good"
for i in range(0, num_cities):
    if not i in tour:
        flag = "bad"
if flag == "bad":
    print("*** error: Your tour has illegal or repeated city names.")
    sys.exit()
check_tour_length = 0
for i in range(0, num_cities - 1):
    check_tour_length = check_tour_length + dist_matrix[tour[i]][tour[i + 1]]
check_tour_length = check_tour_length + dist_matrix[tour[num_cities - 1]][tour[0]]
if tour_length != check_tour_length:
    flag = print("*** error: The length of your tour is not " + str(tour_length) + "; it is actually " + str(check_tour_length) + ".")
    sys.exit()
print("You, user " + my_user_name + ", have successfully built a tour of length " + str(tour_length) + "!")

local_time = time.asctime(time.localtime(time.time()))
output_file_time = local_time[4:7] + local_time[8:10] + local_time[11:13] + local_time[14:16] + local_time[17:19]
output_file_time = output_file_time.replace(" ", "0")
script_name = os.path.basename(sys.argv[0])
if len(sys.argv) > 2:
    output_file_time = sys.argv[2]
output_file_name = script_name[0:len(script_name) - 3] + "_" + input_file[0:len(input_file) - 4] + "_" + output_file_time + ".txt"

f = open(output_file_name,'w')
f.write("USER = " + my_user_name + " (" + my_first_name + " " + my_last_name + "),\n")
f.write("ALGORITHM CODE = " + algorithm_code + ", NAME OF CITY-FILE = " + input_file + ",\n")
f.write("SIZE = " + str(num_cities) + ", TOUR LENGTH = " + str(tour_length) + ",\n")
f.write(str(tour[0]))
for i in range(1,num_cities):
    f.write("," + str(tour[i]))
f.write(",\nNOTE = " + added_note)
f.close()
print("I have successfully written your tour to the tour file:\n   " + output_file_name + ".")