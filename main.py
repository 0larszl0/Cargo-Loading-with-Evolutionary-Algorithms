from typing import List, Tuple
import random

random.seed(42)

# -- Initialise container types -- #
# Define unit container size
CONTAINER_WIDTH, CONTAINER_HEIGHT = (20., 15.)

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

    def __init__(self, sides: int, radius: float, weight: int):
        self.__sides = sides
        self.__radius = radius
        self.__weight = weight

        self.__centre = (0., 0.)

    @property
    def centre(self) -> Tuple[float, float]:
        return self.__centre

    @centre.setter
    def centre(self, new_centre: Tuple[float, float]) -> None:
        self.__centre = new_centre

    @property
    def radius(self) -> float:
        return self.__radius

    @property
    def weight(self) -> int:
        return self.__weight


class Population:
    """Manages a population of individuals and evolutionary operations inside a container."""

    def __init__(self, size: int, num_cylinders: int, mutation_rate: float, max_generations: int, cylinder_sides: int,
                 max_weight):
        # - Initialise passed arguments - #
        self.__size = size
        self.__num_cylinders = num_cylinders
        self.__mutation_rate = mutation_rate
        self.__max_generations = max_generations
        self.__cylinder_sides = cylinder_sides
        self.__max_weight = max_weight

        self.__generations = 0
        self.__weight = 0

        # - Initialise cylinders - #
        # Get a random selection of different cylinder types and save them as objects
        self.__cylinders = [Individual(CYLINDER_SIDES, diameter / 2, weight) for weight, diameter in random.choices(CYLINDERS, k=num_cylinders)]

        # Sorts the cylinders in descending order based on size (radius)
        self.__cylinders = sorted(self.__cylinders, reverse=True, key=lambda x: x.radius)

        # Sets the first cylinder's centre to the middle of the container.
        self.__cylinders[0].centre = (CONTAINER_WIDTH / 2, CONTAINER_HEIGHT / 2)

        print("+-----------\tInitialised cylinders\t-----------+")
        for i, cylinder in enumerate(self.__cylinders):
            print(f"Cylinder {i+1}:\t- Weight: {cylinder.weight}\t- Centre: {cylinder.centre}\t- Radius: {cylinder.radius}")

        # - Initialise population with random position strings - #
        self.__population = [self.create_random_positions() for _ in range(size)]
        print(f"\nSample of population: {random.sample(self.__population, k=5)}")

    def create_random_positions(self) -> List[int]:
        """
        Creates a random list of positions for each circle, except the first circle as that starts at the centre of the
        container.
        :return: List[int], a list of position numbers.
        """
        return random.sample(range(self.__num_cylinders * self.__cylinder_sides), k=self.__num_cylinders - 1)

    def decode_positions(self, positions):
        """
        Decodes the position values and determines
        :return:
        """

        for i, position in enumerate(positions):
            if position > i * 8:
                ...

    def check_feasibility(self, position: int, cylinder: Individual) -> int:
        """
        Checks whether a cylinder will be placed at a feasible position.
        :param int position: The position that is being checked.
        :param Individual cylinder: The cylinder that is being evaluated.
        :return: int, A feasible position. This would be the passed argument if it succeeded, or -1 if the cylinder
        should be discarded.
        """

        # -- Weight -- #
        if cylinder.weight + self.__weight > self.__max_weight:
            return -1

        # -- Geometric -- #
        # Adjust centre of cylinder based on the position number.

        # - Container-based - #


        # - Neighbour-based - #



        return 0



if __name__ == "__main__":
    population = Population(50, 5, .1, 100, CYLINDER_SIDES, 5000)
