from typing import List
import random

random.seed(42)

# -- Initialise container types -- #
# Define unit container size
CONTAINER_SIZE = (20., 15.)

# Define the number of sides a cylinder will have
CYLINDER_SIDES = 8

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

    def __init__(self, size: int, num_cylinders: int, mutation_rate: float, max_generations: int, cylinder_sides: int):
        self.__size = size
        self.__num_cylinders = num_cylinders
        self.__mutation_rate = mutation_rate
        self.__max_generations = max_generations
        self.__cylinder_sides = cylinder_sides

        self.__generations = 0
        self.__population = []

    def create_random_positions(self) -> List[int]:
        """
        Creates a random list of positions for each circle, except the first circle as that starts at the centre of the
        container.
        :return: List[int], a list of position numbers.
        """
        return random.sample(range(self.__num_cylinders * self.__cylinder_sides), k=self.__num_cylinders - 1)


if __name__ == "__main__":
    cylinder_len = 5
    sample_cylinders = [Individual(CYLINDER_SIDES, diameter / 2, weight) for weight, diameter in random.choices(CYLINDERS, k=cylinder_len)]

    population = Population(50, cylinder_len, .1, 100, CYLINDER_SIDES)
    print(population.create_random_positions())
