from random import sample, choice
from typing import List


def multi_point_crossover(group1: List[int], group2: List[int]) -> List[int]:
    """
    Perform multi-point crossover between two groups and randomly choose one of the offsprings.
    :param List[int] group1: A list of position numbers.
    :param List[int] group2: A list of position numbers.
    :return: List[int]
    """
    random_points = sample(range(len(group1)), 2)
    low_point, high_point = min(random_points), max(random_points)

    return choice((
        group1[:low_point] + group2[low_point:high_point] + group1[high_point:],
        group2[:low_point] + group1[low_point:high_point] + group2[high_point:]
    ))


def true_multi_point_crossover(group1: List[int], group2: List[int], crossovers: int):
    ...