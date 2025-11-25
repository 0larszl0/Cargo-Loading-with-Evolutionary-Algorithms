from population import Population
from config import CYLINDER_SIDES


def run_ga(*, population_size: int = 50, num_cylinders: int = 5, mutation_rate: float = .1, max_generations: int = 100,
           cylinder_sides: int = CYLINDER_SIDES, max_weight: int = 10_000):
    """
    Runs the genetic algorithm for the cargo loading problem provided.
    :return: None
    """
    population = Population(population_size, num_cylinders, mutation_rate, cylinder_sides, max_weight)
    population.bin_cylinders()
    population.generate_groups()

    for generation in range(max_generations):
        population.evolve()

        # if generation % 10 == 0:
        #     population.best_cylinder_group.visualise(max_weight)

    population.show_evolution()


if __name__ == "__main__":
    run_ga(
        population_size=50,
        num_cylinders=5,
        mutation_rate=.1,
        max_generations=100,
        cylinder_sides=CYLINDER_SIDES,
        max_weight=10400
    )
