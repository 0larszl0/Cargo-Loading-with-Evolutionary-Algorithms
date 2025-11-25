from math import cos, sin, radians
from typing import Tuple


# The math was found at: https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python#34374437
def rotate(origin: Tuple[float, float], point: Tuple[float, float], angle: float) -> Tuple[float, float]:
    """
    Performs a (counterclockwise) rotation of a point by an angle around an origin.
    :param Tuple[float, float] origin: The origin to rotate around.
    :param Tuple[float, float] point: The point that needs moving.
    :param float angle: The angle, in degrees, to move the point by. (will be converted to radians)
    :return: Tuple[float, float], the rotated point.
    """

    x_diff, y_diff = (point[0] - origin[0]), (point[1] - origin[1])
    angle = radians(angle)

    return (
        origin[0] + (x_diff * cos(angle)) - (y_diff * sin(angle)),
        origin[1] + (x_diff * sin(angle)) - (y_diff * cos(angle))
    )


if __name__ == "__main__":
    print(rotate((0, 0), (5, 5), radians(90)))  # radians multiples pi/180 to the deg value.