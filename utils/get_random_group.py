from typing import Iterable, List, Union
from numpy import array, ndarray
from random import random


def get_random_indices(normalised_vals: Union[List[float], ndarray], k: int = 1) -> List[int]:
    """
    Gets a list of random indices based on the k number of random points within normalised vals.
    :param Iterable[float] normalised_vals: Normalised values to use
    :param int k: The number of random points to use.
    :return: List[int], A list of indices
    """
    random_points = {random()}

    if k > 1:
        while len(random_points) != k:
            random_points.add(random())

    sorted_rps = sorted(random_points)

    i, acc_values, acc_inds = 0, 0, []
    while acc_values != 1 and sorted_rps:
        acc_values += normalised_vals[i]
        if acc_values >= sorted_rps[0]:  # if the accumulated value is greater than the smallest random point.
            acc_inds.append(i)
            sorted_rps.pop(0)

        i += 1

    return acc_inds


if __name__ == "__main__":
    values = array(range(100))
    normalised_values = values / sum(values)

    print(get_random_indices(normalised_values))
    print(get_random_indices(normalised_values, k=3))
