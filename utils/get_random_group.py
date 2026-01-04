from typing import Iterable, List, Union
from numpy import array, ndarray
from random import random


def get_random_indices(normalised_vals: Union[List[float], ndarray], k: int = 1) -> List[int]:
    """
    Gets a list of random indices based on the k number of random points within normalised vals.
    :param Iterable[float] normalised_vals: The normalised values of the fitnesses of a cylinder group.
    :param int k: The number of random points to use.
    :return: List[int], A list of indices
    """
    random_points = {random()}

    if k > 1:
        while len(random_points) != k:
            random_points.add(random())

    sorted_rps = sorted(random_points)  # sorts the random values that are in the floating range [0, 1] in ascending order.

    # - Get the index equivalent of a random point based on the normalised values given - #
    i = 0
    acc = 0  # accumulated values
    rand_indices = []  # a list containing indices of the cylinders at each random point.

    while acc != 1 and sorted_rps:  # loop until either all the normalised values have been visited (acc==1) or till all the random points have been reached.
        acc += normalised_vals[i]

        if acc >= sorted_rps[0]:  # if the accumulated value is greater or equal than the smallest random point.
            rand_indices.append(i)
            sorted_rps.pop(0)

        i += 1

    return rand_indices


if __name__ == "__main__":
    values = array(range(100))
    normalised_values = values / sum(values)

    print(get_random_indices(normalised_values))
    print(get_random_indices(normalised_values, k=3))
