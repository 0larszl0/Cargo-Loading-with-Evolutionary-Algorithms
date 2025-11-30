from typing import Iterable
from random import random


def get_random_index(normalised_vals: Iterable[float]) -> int:
    """
    Gets a random index based on a random point within normalised_vals.
    :param Iterable[float] normalised_vals: Normalised values to use.
    :return: int, an index of the normalised value that was randomly chosen.
    """
    random_point = random()

    acc_values = 0  # accumulated values
    for i, fitness in enumerate(normalised_vals):
        acc_values += fitness
        if acc_values > random_point:
            print(acc_values)
            return i

    return -1

