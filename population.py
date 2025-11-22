from cylinders import Cylinder, CylinderGroup, CYLINDER_SIDES
from config import CONTAINER_WIDTH, CONTAINER_HEIGHT
import random


class Population:
    """Manages a population of individuals and evolutionary operations inside a container."""

    def __init__(self, size: int, num_cylinders: int, mutation_rate: float, max_generations: int, cylinder_sides: int,
                 max_weight):
        self.__size = size
        self.__mutation_rate = mutation_rate
        self.__max_generations = max_generations

        self.__generations = 0
        self.__best_group: CylinderGroup | None = None

        # - Initialise cylinders - #
        # Get a random selection of different cylinder types and save them as objects
        self.__cylinders = [Cylinder(CYLINDER_SIDES, diameter / 2, weight) for weight, diameter in random.choices(CYLINDERS, k=num_cylinders)]

        # Sorts the cylinders in descending order based on size (radius)
        self.__cylinders = sorted(self.__cylinders, reverse=True, key=lambda x: x.weight)

        # Drop all large cylinders that already exceed the maximum weight
        while self.__cylinders and self.__cylinders[0].weight > max_weight:
            del self.__cylinders[0]
            num_cylinders -= 1

        if not self.__cylinders:
            raise Exception(f"\r\033[1m\033[31mCustom Exception: No cylinder can be packed with a maximum weight limit of: {max_weight}")

        # Sets the first cylinder's centre to the middle of the container.
        self.__cylinders[0].centre = (CONTAINER_WIDTH / 2, CONTAINER_HEIGHT / 2)

        print("+-----------\tInitialised cylinders\t-----------+")
        for i, cylinder in enumerate(self.__cylinders):
            print(f"Cylinder {i+1}:\t- Weight: {cylinder.weight}\t- Centre: {cylinder.centre}\t- Radius: {cylinder.radius}")

        # - Initialise population with random position strings - #
        self.__population = [CylinderGroup(self.__cylinders, num_cylinders, cylinder_sides, max_weight) for _ in range(size)]
        print(f"\nSample of population: {random.sample(self.__population, k=3)}\n")

    def tournament_selection(self, k: int = 3) -> CylinderGroup:
        """
        Select a cylinder group using tournament selection.
        :param int k: The size of the selection.
        :return: CylinderGroup
        """
        # Randomly select k cylinder groups and return the one with the highest fitness
        return max(random.sample(self.__population, k), key=lambda x: x.fitness())

    def evolve(self) -> None:
        """
        Run a single generation of the genetic algorithm.
        :return: None
        """
        # - Decode each position string in each group - #
        for i, cylinder_group in enumerate(self.__population):
            cylinder_group.decode(i == 0)

        # - Track the best packing - #
        self.__best_group = max(self.__population, key=lambda x: x.fitness())

        # - Create new population - #
        # Use the recycling method within existing cylinder groups to avoid creating many objects that will be unused.

