from population import Population
from config import CYLINDER_SIDES
import matplotlib.pyplot as plt
from math import sqrt


def run_ga(*, population_size: int = 50, num_cylinders: int = 5, mutation_rate: float = .1, max_generations: int = 100,
           cylinder_sides: int = CYLINDER_SIDES, max_weight: int = 10_000):
    """
    Runs the genetic algorithm for the cargo loading problem provided.
    :return: None
    """
    # Init population and bin cylinders
    population = Population(population_size, num_cylinders, mutation_rate, cylinder_sides, max_weight)
    population.bin_cylinders()

    # Create square-sized subplot to store animations of different bins
    n_row_col = sqrt(population.bins.total)
    if int(n_row_col) != n_row_col:
        n_row_col += 1

    fig, ax = plt.subplots(int(n_row_col), int(n_row_col), figsize=(10, 10))
    fig.patch.set_facecolor("#01364C")

    population.create_containers(fig, ax)

    # For each bin generate its own initial population and evolve them.
    for i in range(population.bins.total):
        population.generate_groups(i)

        for generation in range(max_generations):
            population.evolve(i)

                # if generation % 10 == 0:
                #     population.best_cylinder_group.visualise(max_weight)

        population.create_evolution_anim(i)

    plt.show()


if __name__ == "__main__":
    run_ga(
        population_size=50,
        num_cylinders=5,
        mutation_rate=.1,
        max_generations=100,
        cylinder_sides=CYLINDER_SIDES,
        max_weight=10400
    )
