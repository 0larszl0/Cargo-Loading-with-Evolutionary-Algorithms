from population import Population
from config import CYLINDER_SIDES


def run_ga():
    """
    Runs the genetic algorithm for the cargo loading problem provided.
    :return: None
    """
    population = Population(50, 5, .1, 100, CYLINDER_SIDES, 3400)

    population.evolve()
    # self.evolve()
    #
    # if self.__generations % 10 == 0:
    #     self.__best_group.visualise()


if __name__ == "__main__":
    run_ga()
