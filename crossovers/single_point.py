from random import randrange, choice
from typing import List


def single_point_crossover(group1: List[int], group2: List[int]) -> List[int]:
    """
    Perform single-point crossover between two groups and randomly choose one of the offsprings.
    :param List[int] group1: A list of position numbers.
    :param List[int] group2: A list of position numbers.
    :return: List[int]
    """
    random_point = randrange(len(group1))

    return choice((
        group1[:random_point] + group2[random_point:],
        group2[:random_point] + group1[random_point:]
    ))

