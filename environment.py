import random
import math


class Environment:

    # init function
    def __init__(self, width, height, tile_size):
        self.width = width
        self.height = height
        self.grid = []
        self.tile_size = tile_size  # how many meters per tile
        # Building the grid
        for i in range(height):
            self.grid.append(['.' for i in range(width)])
        self.obstacles = []
        self.hubs = None
        self.packages = []
        self.destinations = []

    # Adding the obstacles to the grid
    def add_obstacle(self, x, y):
        self.grid[y][x] = '#'
        self.obstacles.append((x, y))

    # Adding the hub to the grid
    def add_hub(self, position, name):
        self.grid[position[1]][position[0]] = name
        self.hubs = position

    # Adding the drones to the grid
    # Method needed to create the visual movement of the drone
    def add_drones(self, position, previous, name):
        if (self.grid[position[1]][position[0]] == "."):
            self.grid[position[1]][position[0]] = name
        if (self.grid[previous[1]][previous[0]] == name):
            self.grid[previous[1]][previous[0]] = "."

    # Creating the packages
    def add_package(self, name, position):
        weight = round(random.uniform(0.1, 35), 1)
        destination = self.get_random_empty_position()
        status = "ready"
        self.packages.append({
            'name': name,
            'hub_position': position,
            'weight': weight,
            'destination': destination,
            'status': status
        })

    # Adding the packages names as destinations on the grid
    def add_destination(self, name, position):
        self.grid[position[1]][position[0]] = name

    # Function that gets an empty position
    # Used for adding features on empty positions, e.g.: packages destinations
    def get_random_empty_position(self):
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.grid[y][x] == ".":
                return x, y

    # Creates a grid on terminal
    def print_grid(self):
        for row in self.grid:
            print(" ".join(map(str, row)))

    # Verifies and returns the valid neighbors of a specific grid position
    def neighbors(self, position):
        x, y = position
        potential_neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        valid_neighbors = [neighbor for neighbor in potential_neighbors if self.is_valid_position(neighbor)]
        return valid_neighbors

    # Verifies which tiles are valid for a drone to run on
    def is_valid_position(self, position):
        x, y = position
        return 0 <= x < self.width and 0 <= y < self.height and self.grid[y][x] != '#' and self.grid[y][
            x] != 'X'  # Check for obstacles

    # Heuristic used to find the best path for a drone to deliver a package
    def heuristic(self, a, b):
        # Let's use the Euclidean distance
        # Same as sqrt((x2-x1)^2 + (y2-y1)^2)
        return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

    # Function that returns the path the drone has to follow from the hub to the delivery destination
    # It uses the A* algorithm for it
    def plan_path(self, start, goal):
        open_set = [start]
        came_from = {start: None}
        cost_so_far = {start: 0}

        while open_set:
            current_position = min(open_set, key=lambda pos: cost_so_far[pos] + self.heuristic(goal, pos))
            open_set.remove(current_position)

            if current_position == goal:
                path = [goal]
                while current_position in came_from:
                    current_position = came_from[current_position]
                    path.append(current_position)
                distance = (len(path) - 2) * self.tile_size  # Remove the first None and the last coords
                return path[::-1], distance

            for neighbor in self.neighbors(current_position):
                new_cost = cost_so_far[current_position] + 1  # Assuming uniform cost

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    open_set.append(neighbor)
                    came_from[neighbor] = current_position

        return None  # No path found

    # Function that allocates each package to the drones

    def allocate_packages_to_drones(self, drones, packages, hub_position, goals):
        i = 0
        for drone in drones:
            for package in packages:
                goal = goals[i]

                plan_path_result = self.plan_path(hub_position, goal)
                if plan_path_result is None:
                    # Handle the case where no path is found
                    continue

                (path_to_destination, distance) = plan_path_result
                round_trip_energy = 2 * distance

                # Necessary conditions before picking up a package:
                if (
                        drone.max_weight >= package['weight']
                        and drone.energy_capacity - round_trip_energy >= 25
                        and drone.dronerange >= distance
                ):
                    drone.current_package = package
                    packages.remove(package)
                    i += 1
