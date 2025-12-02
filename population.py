from cylinders import Cylinder, CylinderGroup, CYLINDER_SIDES, CYLINDERS
from canvas import AnimatedContainer
from utils import get_random_indices
from numpy import array, ndarray
from crossovers import *

from typing import List, Tuple, Union
from matplotlib.pyplot import Figure, Axes

import random


class Bin:
    def __init__(self, max_weight: int):
        self.__max_weight = max_weight
        self.__weight = 0
        self.__cylinders = []

    @property
    def cylinders(self) -> List[Cylinder]:
        return self.__cylinders

    @property
    def weight(self) -> int:
        return self.__weight

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
        self.__total_bins = 1

    @property
    def bins(self) -> List[Bin]:
        return self.__bins

    @property
    def total(self) -> int:
        return self.__total_bins

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
        self.__total_bins += 1


class Population:
    """Manages a population of individuals and evolutionary operations inside a container."""

    def __init__(self, size: int, num_cylinders: int, mutation_rate: float, cylinder_sides: int, max_weight):
        self.__size = size
        self.__mutation_rate = mutation_rate
        self.__cylinder_sides = cylinder_sides
        self.__max_weight = max_weight
        self.__population = []
        self.__bins = Bins(max_weight)

        self.__generations = 0
        self.__best_cylinder_group: CylinderGroup | None = None

        # - Initialise cylinders - #
        # Get a random selection of different cylinder types and save them as objects
        self.__cylinders = [Cylinder(CYLINDER_SIDES, diameter / 2, weight) for weight, diameter in random.choices(CYLINDERS, k=num_cylinders)]

        # Sorts the cylinders in descending order based on size (radius)
        self.__cylinders = sorted(self.__cylinders, reverse=True, key=lambda x: x.weight)

        print("+-----------\tInitialised cylinders\t-----------+")
        for i, cylinder in enumerate(self.__cylinders):
            print(f"Cylinder {i+1}:\t- Weight: {cylinder.weight}\t- Centre: {cylinder.centre}\t- Radius: {cylinder.radius}")

        self.__animated_containers: List[AnimatedContainer] = []

    @property
    def best_cylinder_group(self) -> CylinderGroup:
        return self.__best_cylinder_group

    @property
    def bins(self) -> Bins:
        return self.__bins

    def bin_cylinders(self) -> None:
        """
        Groups cylinders into different bins using first fit bin packing, based on their weight.
        :return: None
        """
        for cylinder in self.__cylinders:
            self.__bins.pack_cylinder_ff(cylinder)

        if not self.__bins.bins[0].cylinders:  # if no cylinders could be packed.
            raise Exception(f"\r\033[1m\033[31mCustom Exception: No cylinder can be packed with a maximum weight limit of: {self.__max_weight}")

    def create_containers(self, fig: Figure, ax: Union[Axes, List[Axes]], fpp: int = 30) -> None:
        """
        Create a container visualisation object for each possible bin.
        :param Figure fig: The figure the visualisation should be made onto.
        :param Union[Axes, List[Axes]] ax: The Axes, or List of Axes, of available plots to draw onto.
        :param int fpp: The frames per patch for the animation within each container.
        :return: None
        """
        if self.__bins.total == 1:
            self.__animated_containers.append(AnimatedContainer(fpp, fig, ax))
            return

        for i in range(self.__bins.total):
            self.__animated_containers.append(AnimatedContainer(fpp, fig, ax[i]))

    def generate_groups(self, bin_focus: int = 0) -> None:
        """
        Generates the initial groups, containing random position strings, for the population.
        :param int bin_focus: The bin of cylinders to focus on.
        :return: None
        """
        focussed_bin = self.__bins.bins[bin_focus]

        # Need to create clones of each Cylinder, instead of taking focussed_bin's cylinder as it will take a reference
        # of each class, thus essentially sharing the same cylinder's amongst each group, instead of having their own.
        self.__population = [
            CylinderGroup(
                [Cylinder(CYLINDER_SIDES, cylinder.radius, cylinder.weight) for cylinder in focussed_bin.cylinders],
                focussed_bin.size(), self.__cylinder_sides, focussed_bin.weight
            ) for _ in range(self.__size)
        ]
        print(f"\nSample of population: {random.sample(self.__population, k=3)}\n")

        self.__best_cylinder_group = CylinderGroup(
            [Cylinder(CYLINDER_SIDES, cylinder.radius, cylinder.weight) for cylinder in focussed_bin.cylinders],
            focussed_bin.size(), self.__cylinder_sides, focussed_bin.weight
        )

        self.__animated_containers[bin_focus].best_cylinder_group = self.__best_cylinder_group
        self.__animated_containers[bin_focus].add_cylinders()

    def tournament_selection(self, k: int = 3) -> CylinderGroup:
        """
        Select a cylinder group using tournament selection.
        :param int k: The size of the selection.
        :return: CylinderGroup
        """
        # Randomly select k cylinder groups and return the one with the highest fitness
        return max(random.sample(self.__population, k), key=lambda x: x.fitness())

    def get_normalised_fitness(self) -> ndarray:
        """
        Get an array of normalised fitnesses from the population
        :return: ndarray
        """
        fitnesses = array([group.fitness() for group in self.__population])
        return fitnesses / sum(fitnesses)

    def roulette_wheel_selection(self) -> CylinderGroup:
        """
        Perform roulette wheel selection to select a cylinder group.
        :return: CylinderGroup
        """
        return self.__population[
            get_random_indices(self.get_normalised_fitness())[0]
        ]

    def stochastic_universal_sampling(self) -> Tuple[CylinderGroup, CylinderGroup]:
        """
        Similar to Roulette Wheel Selection, but instead of one fixed point there's two.
        :return: Tuple[CylinderGroup, CylinderGroup]
        """
        child1_ind, child2_ind = get_random_indices(self.get_normalised_fitness(), 2)
        return (
            self.__population[child1_ind],
            self.__population[child2_ind]
        )

    def rank_based_selection(self) -> CylinderGroup:
        """
        Performs ranked based selection to select a cylinder group.
        :return: CylinderGroup
        """
        # - Sort the population in terms of fitness from smallest to largest - #
        sorted_population = sorted(self.__population, key=lambda group: group.fitness())

        total_ranks = sum(range(1, self.__size + 1))
        normalised_ranks = [i / total_ranks for i in range(1, self.__size + 1)]

        return sorted_population[get_random_indices(normalised_ranks)[0]]

    def elitist_selection(self, k: int = 5) -> CylinderGroup:
        """
        Gets one of the best k groups from the population.
        :return: CylinderGroup
        """
        return random.choice(sorted(self.__population, key=lambda group: group.fitness())[-k:])

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

    def evolve(self, bin_focus: int = 0) -> None:
        """
        Run a single generation of the genetic algorithm.
        :param int bin_focus: The bin of cylinders to focus on.
        :return: None
        """
        # - Decode each position string in each group - #
        for i, cylinder_group in enumerate(self.__population):
            cylinder_group.decode()

        # - Track the best packing - #
        # Get the best cylinder group in the current generation.
        best_cylinder_group_gen = max(self.__population, key=lambda x: x.fitness())

        # Check whether the best cylinder group in this generation group outperforms any previous ones.
        current_fitness, new_fitness = self.__best_cylinder_group.fitness(), best_cylinder_group_gen.fitness()
        if new_fitness > current_fitness:
            print(f"# {'-'*20} \033[1mNew Solution found at Generation {self.__generations}\033[0m {'-'*20} #\n"
                  f"{best_cylinder_group_gen}"
                  f"New fitness: \033[1m{new_fitness}\033[0m\t\033[32m+{new_fitness - current_fitness}\033[0m (from {current_fitness})\n"
                  f"{'='*80}\n")

            # Update the centre values of the Cylinders within the best cylinder group.
            for i, cylinder in enumerate(best_cylinder_group_gen.cylinders):
                self.__best_cylinder_group.cylinders[i].centre = cylinder.centre

            self.__animated_containers[bin_focus].save_state(self.__generations)

        # - Create new population - #
        # Use the recycling method within existing cylinder groups to avoid creating many objects that will be unused.
        next_groups = [
            self.mutate(
                single_point_crossover(
                    self.tournament_selection().group,
                    self.tournament_selection().group
                )
            ) for _ in range(self.__size)
        ]

        for i, group in enumerate(self.__population):
            group.recycle(
                [Cylinder(CYLINDER_SIDES, cylinder.radius, cylinder.weight) for cylinder in self.__bins.bins[bin_focus].cylinders],
                next_groups[i]
            )

        self.__generations += 1

    def create_evolution_anim(self, bin_focus: int = 0) -> None:
        """
        Uses the dynamic visualiser to illustrate the placement of cylinders between key generations.
        :return: None
        """
        current_container = self.__animated_containers[bin_focus]

        current_container.draw_acceptance_range()
        current_container.draw_centre()
        current_container.draw_patches()  # adds the cylinder patches at their initial positions onto the axes.
        current_container.draw_com_marker()

        print(f"# {'-'*26}\033[1m Recorded data for Bin {bin_focus}\033[0m {'-'*26} #")
        for cylinder_patch, save in current_container.save_states.items():
            print(f"{cylinder_patch}:\n"
                  f"\t- Centre history:\t{', '.join([str(centre) for centre in save[0]])}\n"
                  f"\t- Increments:\t\t{', '.join([str(centre) for centre in save[1]])}\n")

        current_container.choose_title(current_container.TRANSITION_TITLE)
        current_container.setup_axis()  # Saved penultimately to ensure all labels will be accounted for in the legend.
        current_container.ready_animation()  # Ready the animation for that container/axes.

