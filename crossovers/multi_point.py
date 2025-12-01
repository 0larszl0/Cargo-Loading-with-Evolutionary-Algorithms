from .single_point import single_point_crossover
from random import sample, choice
from typing import List


def multi_point_crossover(group1: List[int], group2: List[int], *, crossovers: int) -> List[int]:
    """
    Performs multi-point crossover between two groups and randomly chooses one of the offsprings.
    :param List[int] group1: A list of position numbers.
    :param List[int] group2: A list of position numbers.
    :param int crossovers: The number of crossover points to use.
    :return: List[int]
    """
    if crossovers == 1:  # if the user selected their to be only one crossover point
        return single_point_crossover(group1, group2)

    # Get a list of 'crossover' amount of random points, in ascending order.
    random_points = sorted(sample(range(len(group1)), k=crossovers))

    for i, point in enumerate(random_points):
        if (i % 2 == 0) and (i == len(random_points) - 1):
            group1[point:], group2[point:] = group2[point:], group1[point:]

        elif i % 2 == 0:
            group1[point: random_points[i + 1]], group2[point: random_points[i + 1]] = group2[point: random_points[i + 1]], group1[point: random_points[i + 1]]

    return choice((group1, group2))


if __name__ == "__main__":
    # When running directly comment out the relative import at the top, and uncomment the below
    # from single_point import single_point_crossover

    print(multi_point_crossover(list(range(10)), list(range(10, 20)), crossovers=1))
    print(multi_point_crossover(list(range(10)), list(range(10, 20)), crossovers=4))
