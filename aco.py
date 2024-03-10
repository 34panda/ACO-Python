from math import sqrt
from random import randint, choices
import matplotlib.pyplot as plt

points = {
    'A': (1, 1),
    'B': (5, 8),
    'C': (7, 12),
    'D': (2, 9),
    'E': (7, 2),
    'F': (1, 12),
    'G': (4, 2),
}
starting_point = 'E'
alpha = 2
beta = 1



current_point = points[starting_point]
distances = []
parameters = []
probabilities = []
path = [current_point]


def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    length = sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
    return length


def get_distances(points, current_point):
    updated_points = {key: value for key, value in points.items() if value != current_point}

    distances.clear()
    for point in updated_points:
        distances.append(distance(current_point, updated_points[point]))

    return updated_points


def calculate_parameter(distance, alpha, beta):
    # generate a random int for A parameter (1-10)
    A = randint(1, 10)
    B = 1 / distance
    parameter = (A ** alpha) * (B ** beta)
    return parameter


def get_parameters(distances):
    parameters.clear()
    for distance in distances:
        parameters.append(calculate_parameter(distance, alpha, beta))


def get_probabilities(parameters):
    sum_of_parameters = sum(parameters)
    probabilities.clear()
    for parameter in parameters:
        probability = (parameter / sum_of_parameters) * 100
        probabilities.append(probability)


def next_point(probabilities):
    random_point = choices(list(points.keys()), weights=probabilities, k=1)[0]
    next_point = points[random_point]
    return next_point

def draw_graph(points, path):
  
    points_x, points_y = zip(*points.values())
    path_x, path_y = zip(*path)

    # Plot the connected points
    plt.plot(path_x + (path_x[0],), path_y + (path_y[0],), color='mediumpurple', marker='o', linestyle='-', markersize=10, label="Point")

    # Annotate the points with their labels and arrows
    for i in range(len(path) - 1):
        plt.annotate("", xy=path[i + 1], xytext=path[i],
                     arrowprops=dict(arrowstyle='->', color='blue', mutation_scale=30, linewidth=2))

    # Highlight the starting point in red with a red outline
    start_point = path[0]
    plt.scatter(*start_point, color='orange', edgecolors='black', marker='o', s=300, label='Starting Point')

    for i in range(1, len(path)-1):
        plt.scatter(*path[i], color='lavender', edgecolors='blue', marker='o', s=200)

    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Path taken by an Ant')

    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == "__main__":

    for _ in range(len(points)-1):

        points = get_distances(points, current_point)
        get_parameters(distances)
        get_probabilities(parameters)
        current_point = next_point(probabilities)
        path.append(current_point)

        print("Distances:", distances)
        print("Parameters:", parameters)
        print("Probabilities:", probabilities)
        print("Sum of probabilities:", sum(probabilities))
        print(points)
        print("Next point:", current_point)
        print("\n########\n")

    path.append(path[0])
    print(path)

    draw_graph(points, path)
