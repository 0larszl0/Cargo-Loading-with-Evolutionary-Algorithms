from typing import Tuple, List


def com(cylinders: List, total_weight: int) -> Tuple[float, float]:
    """
    Calculate the centre of mass (COM), of a CylinderGroup, in each axis.
    :param List cylinders: Either a List of Cylinder or CustomCircle objects.
    :param int total_weight: The total weight of the objects in the cylinders parameter.
    :return: Tuple[float, float]
    """
    # Get a list of masses multiplied by their axis (MMA)
    mma_x, mma_y = zip(*[(cylinder.weight * cylinder.centre[0], cylinder.weight * cylinder.centre[1]) for cylinder in cylinders])

    return sum(mma_x) / total_weight, sum(mma_y) / total_weight

