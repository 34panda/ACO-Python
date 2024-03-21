from math import sqrt
from random import randint, choices, random
import matplotlib.pyplot as plt
import time

# Points and starting configuration
points = {
    'A': (0, 0),
}

starting_point = 'A'

# Generate random points
for i in range(15):
    points.update({str(i): (random(), random())})

alpha = 1
beta = 4

##########################

num_ants = len(points)
iterations = 250
evaporation_rate = 0.5
pheromone_deposit = 1

###########################

# initialize pheromone dictionary
pheromones = {(i, j): 1 for i in points for j in points if i != j}
time_start = time.time()

def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))

def calculate_parameter(point_a, point_b, alpha, beta):
    pheromone_level = pheromones[(point_a, point_b)]
    dist = distance(points[point_a], points[point_b])
    return (pheromone_level ** alpha) * ((1 / dist) ** beta)

def update_pheromones(ant_path):
    path_length = sum([distance(points[ant_path[i]], points[ant_path[i+1]]) for i in range(len(ant_path) - 1)])
    for i in range(len(ant_path) - 1):
        pheromones[(ant_path[i], ant_path[i+1])] += pheromone_deposit / path_length
        pheromones[(ant_path[i+1], ant_path[i])] += pheromone_deposit / path_length  # Assume symmetric paths

def evaporate_pheromones():
    for key in pheromones:
        pheromones[key] *= (1 - evaporation_rate)

def ant_colony(num_iterations, starting_point):
    for i in range(num_iterations):
        for j in range(num_ants):
            available_points = list(points.keys())
            current_point = choices(available_points)[0]  # Random starting point
            ant_path = [current_point]
            available_points.remove(current_point)

            while available_points:
                parameters = [calculate_parameter(current_point, point, alpha, beta) for point in available_points]
                next_point = choices(available_points, weights=parameters)[0]
                ant_path.append(next_point)
                available_points.remove(next_point)
                current_point = next_point

            ant_path.append(ant_path[0])  # Return to start
            update_pheromones(ant_path)

        evaporate_pheromones()

    return ant_path


##############################################################


def draw_graph(points, path):
    path_coords = [points[node] for node in path]

    # Extract x and y coordinates from the path
    path_x, path_y = zip(*path_coords)

    # Plot the connected points
    plt.plot(path_x + (path_x[0],), path_y + (path_y[0],), color='mediumpurple', marker='o', linestyle='-',
             markersize=10, label="Point")

    # Annotate the points with their labels and arrows
    for i in range(len(path) - 1):
        plt.annotate("", xy=path_coords[i + 1], xytext=path_coords[i],
                     arrowprops=dict(arrowstyle='->', color='blue', mutation_scale=30, linewidth=2))

    # Highlight the starting point in orange
    start_point = path_coords[0]
    plt.scatter(*start_point, color='orange', edgecolors='black', marker='o', s=300, label='Starting Point')

    for i in range(1, len(path_coords) - 1):
        plt.scatter(*path_coords[i], color='lavender', edgecolors='blue', marker='o', s=200)

    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Path taken by an Ant')

    plt.grid(True)
    plt.legend()
    plt.show()

##############################################################



if __name__ == "__main__":
    path = ant_colony(iterations, starting_point)
    print(path)
    time_end = time.time()
    print(time_end - time_start)
    draw_graph(points, path)
