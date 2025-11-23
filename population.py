from cylinders import Cylinder, CylinderGroup, CYLINDER_SIDES, CYLINDERS
from config import CONTAINER_WIDTH, CONTAINER_HEIGHT
from typing import List
import random


class Bin:
    def __init__(self, max_weight: int):
        self.__max_weight = max_weight
        self.__weight = 0
        self.__cylinders = []

    @property
    def cylinders(self) -> List[Cylinder]:
        return self.__cylinders

    def size(self) -> int:
        return len(self.__cylinders)

    def add(self, cylinder: Cylinder) -> bool:
        """
        Adds a cylinder to the bin
        :return: True, if cylinder can fit in the bin, False otherwise.
        """
        if self.__weight + cylinder.weight <= self.__max_weight:
            self.__cylinders.append(cylinder)
            self.__weight += cylinder.weight
            return True

        return False


class Bins:
    def __init__(self, max_weight):
        self.__max_weight = max_weight
        self.__bins = [Bin(max_weight)]

    @property
    def bins(self) -> List[Bin]:
        return self.__bins

    def pack_cylinder_ff(self, cylinder: Cylinder) -> None:
        """
        Packs the cylinder using the first-fit bin packing method
        :param Cylinder cylinder: The cylinder to pack.
        :return: None
        """
        if cylinder.weight > self.__max_weight:  # if the cylinder is heavier than the bins maximum capacity
            return  # just ignore it, thus letting it be discarded.

        for b in self.__bins:  # Iterate across each existing bin.
            if b.add(cylinder):  # checks whether the cylinder could fit at a particular bin
                return  # if it could fit, then return

        # when all the existing bins couldn't pack the new cylinder, create a new bin and add the cylinder in there.
        self.__bins.append(Bin(self.__max_weight))
        self.__bins[-1].add(cylinder)

class Population:
    """Manages a population of individuals and evolutionary operations inside a container."""

    def __init__(self, size: int, num_cylinders: int, mutation_rate: float, max_generations: int, cylinder_sides: int,
                 max_weight):
        self.__size = size
        self.__mutation_rate = mutation_rate
        self.__max_generations = max_generations
        self.__cylinder_sides = cylinder_sides
        self.__max_weight = max_weight
        self.__population = []
        self.__bins = Bins(max_weight)

        self.__generations = 0
        self.__best_group: CylinderGroup | None = None

        # - Initialise cylinders - #
        # Get a random selection of different cylinder types and save them as objects
        self.__cylinders = [Cylinder(CYLINDER_SIDES, diameter / 2, weight) for weight, diameter in random.choices(CYLINDERS, k=num_cylinders)]

        # Sorts the cylinders in descending order based on size (radius)
        self.__cylinders = sorted(self.__cylinders, reverse=True, key=lambda x: x.weight)

        # Sets the first cylinder's centre to the middle of the container.
        self.__cylinders[0].centre = (CONTAINER_WIDTH / 2, CONTAINER_HEIGHT / 2)

        print("+-----------\tInitialised cylinders\t-----------+")
        for i, cylinder in enumerate(self.__cylinders):
            print(f"Cylinder {i+1}:\t- Weight: {cylinder.weight}\t- Centre: {cylinder.centre}\t- Radius: {cylinder.radius}")

    def bin_cylinders(self) -> None:
        """
        Groups cylinders into different bins using first fit bin packing, based on their weight.
        :return: None
        """
        for cylinder in self.__cylinders:
            self.__bins.pack_cylinder_ff(cylinder)

        if not self.__bins.bins[0].cylinders:  # if no cylinders was able to be packed.
            raise Exception(f"\r\033[1m\033[31mCustom Exception: No cylinder can be packed with a maximum weight limit of: {self.__max_weight}")

    def generate_groups(self, bin_focus: int = 0) -> None:
        """
        Generates the initial groups, containing random position strings, for the population.
        :param int bin_focus: The bin to focus the packing onto.
        :return: None
        """
        focussed_bin = self.__bins.bins[bin_focus]

        self.__population = [
            CylinderGroup(focussed_bin.cylinders, focussed_bin.size(), self.__cylinder_sides) for _ in range(self.__size)
        ]
        print(f"\nSample of population: {random.sample(self.__population, k=3)}\n")

    def tournament_selection(self, k: int = 3) -> CylinderGroup:
        """
        Select a cylinder group using tournament selection.
        :param int k: The size of the selection.
        :return: CylinderGroup
        """
        # Randomly select k cylinder groups and return the one with the highest fitness
        return max(random.sample(self.__population, k), key=lambda x: x.fitness())

    @staticmethod
    def single_point_crossover(group1: List[int], group2: List[int]) -> List[int]:
        """
        Perform single-point crossover between two groups and randomly choose one of the offsprings.
        :param List[int] group1: A list of position numbers.
        :param List[int] group2: A list of position numbers.
        :return: List[int]
        """
        random_point = random.randrange(0, len(group1))

        return random.choice((
            group1[:random_point] + group2[random_point:],
            group2[:random_point] + group1[random_point:]
        ))

    def mutate(self, group: List[int]) -> List[int]:
        """
        Applies a replacement mutation to a position number with another number in the range (i + 1) * cylinder_sides
        that doesn't already exist within group ('i' is the index of a position num in the group of position numbers).
        :param List[int] group: The list of position numbers
        :return: List[int], a potentially mutated group.
        """
        existing_nums = set(group)

        for i in range(len(group)):  # Iterate across the length of the group
            if random.random() < self.__mutation_rate:  # if a mutation occurs
                # choose a new random position numbers from the possible range subtracted by any already used positions.
                group[i] = random.choice(list(set(range((i + 1) * CYLINDER_SIDES)).difference(existing_nums)))

        return group

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
        next_groups = [
            self.mutate(
                self.single_point_crossover(
                    self.tournament_selection().group,
                    self.tournament_selection().group
                )
            ) for _ in range(self.__size)
        ]

        # for group in self.__population:
        #     group.recycle(self.__)
