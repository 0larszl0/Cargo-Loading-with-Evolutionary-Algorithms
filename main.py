from config import CYLINDER_SIDES, EXECUTE_TEST_CASE, CONTAINER_HEIGHT, CONTAINER_WIDTH, VISUALISE_EVOLUTION, RECORD_RESULTS
from event_manager import EventManager
from population import Population
from cylinders import Cylinder
import matplotlib.pyplot as plt
from numpy import ndarray
from typing import Tuple, List
from math import sqrt
from TEST import test_instances
from time import perf_counter
from json import dump


def create_subplots(population: Population) -> Tuple[plt.Figure, plt.Axes, EventManager]:
    """
    Creates subplots depending on the quantity of how many cylinders that were binned.
    :param Population population: Population obj.
    :return: Tuple[plt.Figure, plt.Axes, EventManager]
    """
    # Create square-sized subplot to store animations of different bins
    n_row_col = sqrt(population.bins.total)
    if int(n_row_col) != n_row_col:
        n_row_col += 1

    fig, ax = plt.subplots(int(n_row_col), int(n_row_col), figsize=(10, 10))
    fig.patch.set_facecolor("#01364C")

    if type(ax) is ndarray:  # if there are multiple bins to consider
        ax = ax.flatten()

        # Hide the Axes that will not be used.
        for axes in ax[population.bins.total:]:
            axes.set_visible(False)

        fig.tight_layout()

    return fig, ax, EventManager(fig)


def run_ga(cylinders: List[Cylinder],
           num_cylinders: int = 5,
           *,
           population_size: int = 50,
           mutation_rate: float = .1,
           max_generations: int = 100,
           max_weight: int = 10_000,
           cylinder_sides: int = CYLINDER_SIDES,
           container_width: float = CONTAINER_WIDTH,
           container_height: float = CONTAINER_HEIGHT,
           visualise: bool = VISUALISE_EVOLUTION) -> None:
    """
    Runs the genetic algorithm for the cargo loading problem provided.

    :param List[Cylinder] cylinders: A list of cylinders that will be grouped up. If [] is specified, a default range
    of cylinders based on num_cylinders will be created, with weights and diameter in accordance to the config file
    CYLINDER_TYPES.

    :param int num_cylinders: The number of cylinders provided or in the case of [] cylinders, the number of cylinders
    to generate.

    :param int population_size: The amount of groups to create with the given cylinders.
    :param float mutation_rate: The probability of a mutation to occur: a new position number to be randomly assigned.
    :param int max_generations: The number of generations to compute for.
    :param int max_weight: The maximum weight of the container.
    :param int cylinder_sides: How many sides of a cylinder to compute for.
    :param float container_width: The width of the given container.
    :param float container_height: The height of the given container.
    :param bool visualise: Whether to visualise the evolution of the population or not.

    :return: None
    """
    # Init population and bin cylinders
    population = Population(population_size, cylinders, num_cylinders, mutation_rate, cylinder_sides, max_weight)
    population.bin_cylinders()

    fig, ax, event_manager = create_subplots(population)
    population.create_containers(fig, ax, event_manager, container_width, container_height)

    # For each bin generate its own initial population and evolve them, whilst storing each animation and the key events
    animations, key_events = [], {}
    for i in range(population.bins.total):
        start_time = perf_counter()

        if not population.generate_groups(i):  # checks whether there's any need to evolve this bin
            continue  # Skip the evolving process when there's no need.

        for generation in range(max_generations):
            population.evolve(i)

        animations.append(population.create_evolution_anim(i))
        key_events |= population.get_summary(perf_counter() - start_time, i)

    if visualise: plt.show()

    if RECORD_RESULTS:
        with open(f"_TEST_RESULTS/instance[{EXECUTE_TEST_CASE}]-IPSUM.json", 'w') as json_file:
            dump(key_events, json_file)


if __name__ == "__main__":
    # Apply default values
    _num_cylinders, _max_weight, _container_width, _container_height = 5, 13_500, CONTAINER_WIDTH, CONTAINER_HEIGHT

    _test_instance = test_instances(EXECUTE_TEST_CASE)
    _cylinders = list(_test_instance[1])

    if any(_test_instance):  # if a valid test instance was retrieved.
        _num_cylinders = len(_cylinders)
        _container_width, _container_height, _max_weight = _test_instance[0]

    run_ga(
        _cylinders,
        _num_cylinders,  # How many cylinders should be generated
        population_size=50,
        mutation_rate=.1,
        max_generations=100,
        max_weight=_max_weight,
        container_width=_container_width,
        container_height=_container_height
    )
