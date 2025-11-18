import random

random.seed(42)

# -- Initialise container types -- #
# Define unit container size
CONTAINER_SIZE = (20., 15.)

# Define cylinder containers
CYLINDERS = [
    (2500, 2.),  # Heavy tank
    (800, 1.5),  # Medium drum
    (300, 1.2)   # Light barrel
]


class Individual:
    """Represents a cylinder of a particular type in this problem."""

    def __init__(self, sides, radius, weight):
        self.__sides = sides
        self.__radius = radius
        self.__weight = weight

        self.__midpoint = (0., 0.)


class Population:
    """Manages a population of individuals and evolutionary operations."""

    def __init__(self, size: int, num_cylinders: int, mutation_rate: float, max_generations: int, cylinder_sides: int = 8):
        self.__size = size
        self.__num_cylinders = num_cylinders
        self.__mutation_rate = mutation_rate
        self.__max_generations = max_generations

        self.__generations = 0

        # Initialises population by selecting a random variety of different cylinders, and saving them into objects
        self.__population = [Individual(cylinder_sides, diameter / 2, weight) for weight, diameter in random.choices(CYLINDERS, k=size)]
        print(self.__population)


if __name__ == "__main__":
    Population(50, 10, .1, 100)
