from typing import List, Tuple
from math import dist
from utils import *
import random

random.seed(42)


class Cylinder:
    """Represents a cylinder of a particular type."""

    def __init__(self, sides: int, diameter: float, weight: float, *, id_: int = -1):
        self._id = id(self)
        if id_ != -1:
            self._id = id_

        self._sides = sides
        self._diameter = diameter
        self._radius = diameter / 2
        self._weight = weight

        self._centre = (0., 0.)

    def __str__(self):
        return (f"Cylinder (\033[4m{self.__repr__().split('at ')[1][:-1]}\033[0m):"
                f"\t- Centre: ({self._centre[0]:.3f}, {self._centre[1]:.3f})"
                f"\t- Radius: {self._radius}"
                f"\t- Weight: {self._weight}")

    @property
    def id(self) -> int:
        return self._id

    @property
    def centre(self) -> Tuple[float, float]:
        return self._centre

    @centre.setter
    def centre(self, new_centre: Tuple[float, float]) -> None:
        self._centre = new_centre

    @property
    def diameter(self) -> float:
        return self._diameter

    @property
    def radius(self) -> float:
        return self._radius

    @property
    def weight(self) -> float:
        return self._weight

    def left(self) -> float:
        return self._centre[0] - self._radius

    def right(self) -> float:
        return self._centre[0] + self._radius

    def top(self) -> float:
        return self._centre[1] + self._radius

    def bottom(self) -> float:
        return self._centre[1] - self._radius


class BasicGroup:
    """Contains a basic collection of Cylinder objects and their properties as a group."""

    def __init__(self, cylinders: List[Cylinder], num_cylinders: int, cylinder_sides: int, container_width: float, container_height: float):
        self._cylinders = cylinders
        self._cylinder_sides = cylinder_sides
        self._num_cylinders = num_cylinders

        self._weight = sum(cylinder.weight for cylinder in cylinders)

        self._container_width = container_width
        self._container_height = container_height

    @property
    def cylinders(self) -> List[Cylinder]:
        return self._cylinders

    @property
    def num_cylinders(self) -> int:
        return self._num_cylinders

    @property
    def weight(self) -> int:
        return self._weight

    def fitness(self) -> float:
        """
        The fitness is the inverse of the distance between the COM and the centre of the container.
        (shorter distance = higher fitness)
        :return: -> float
        """
        distance = dist(com(self._cylinders, self._weight), (self._container_width / 2, self._container_height / 2))

        if distance == 0:  # if the packed COM is at the centre of the container.
            return float("inf")

        return 1. / distance


class CylinderGroup(BasicGroup):
    """
    Inherited from BasicGroup, CylinderGroups is a more powerful object that can assort each cylinder to a particular
    position.
    """

    def __init__(self, cylinders: List[Cylinder], num_cylinders: int, cylinder_sides: int, container_width: float, container_height: float):
        super().__init__(cylinders, num_cylinders, cylinder_sides, container_width, container_height)
        self.__decoded_cylinders = cylinders[:1]

        # Sets the first cylinder's centre to the middle of the container.
        self._cylinders[0].centre = (container_width / 2, container_height / 2)

        # A group will contain a list of random position numbers for each cylinder, apart from the first as that is
        # to be placed in the centre of the container.
        self.__group = random.sample(range(num_cylinders * cylinder_sides), k=num_cylinders - 1)

    def __str__(self):
        return (f"CylinderGroup (\033[4m{self.__repr__().split('at ')[1][:-1]}\033[0m) contains:\n"
                f"\t- {'\n\t- '.join([str(cylinder) for cylinder in self._cylinders])}\n\n"
                f"{'='*80}\n")

    @property
    def decoded_cylinders(self) -> List[Cylinder]:
        return self.__decoded_cylinders

    @decoded_cylinders.setter
    def decoded_cylinders(self, updated_cylinders: List[Cylinder]) -> None:
        self.__decoded_cylinders = updated_cylinders

    @property
    def group(self) -> List[int]:
        return self.__group

    def recycle(self, grouping: List[int]) -> None:
        """
        Reuses the cylinder group by updating the group value and resetting the cylinders in the group.
        :param List[int] grouping: The new group this CylinderGroup will contain.
        :return: None
        """
        # - Reset centre of cylinders - #
        for cylinder in self._cylinders[1:]:  # reset all of them apart from the first which will always be at the centre
            cylinder.centre = (0., 0.)

        # - Reset decoded cylinders variable - #
        self.__decoded_cylinders = self._cylinders[:1]

        # - Reset the group - #
        self.__group = grouping

        # - Reset the weight of the group - #
        self._weight = sum(cylinder.weight for cylinder in self._cylinders)

    def decode(self, debug: bool = False) -> None:
        """
        Decodes the position numbers within the group.
        :param bool debug: Whether to show debug messages or not.
        :return: None
        """
        cprint(debug, f"Outputting decoding process for: {self.__group}")

        for i in range(self._num_cylinders - 1):
            # Check if the position number is greater than the maximum position number for the ith circle being seen.
            max_positions = (i + 1) * self._cylinder_sides
            if self.__group[i] > max_positions:
                # if it is reset the position number to 0
                self.__group[i] = 0

            cprint(debug, f"+----\tWorking on cylinder: {i + 1}\t----+")
            self.__group[i] = self.check_feasibility(self.__group[i], self._cylinders[i + 1], max_positions, max_positions, debug)
            cprint(debug, f"Final position: {self.__group[i]}, with position: {self._cylinders[i + 1].centre}\n")

            if self.__group[i] == -1:
                # reduce the number of cylinders if a position had failed.
                self._num_cylinders -= 1

        # --- Filter any -1 positions and any cylinders at those positions --- #
        # 1. Zip the group and all the cylinders (apart from the first) together
        # 2. Filter out any pair that has a -1 position number
        filtered_pairs = list(filter(lambda x: x[0] != -1, zip(self.__group, self._cylinders[1:])))

        self.__group = []  # set value in case there are no successful pairs
        if filtered_pairs:  # check if there are successful pairs
            # 2a. Unpair the results, convert them to lists, and assign appropriately
            self.__group, filtered_cylinders = map(lambda x: list(x), zip(*filtered_pairs))

            # 2b. Add the filtered cylinders after it.
            self.__decoded_cylinders += filtered_cylinders

            # 2c. Update the new weight of this group
            self._weight = sum(cylinder.weight for cylinder in self.__decoded_cylinders)

        cprint(debug, f"{'-'*40}\nDecoded group: {self.__group}\nRemaining cylinders: {self.__decoded_cylinders}")

    def check_feasibility(self, position: int, cylinder: Cylinder, total_positions: int, positions_left: int, debug: bool = False) -> int:
        """
        Checks whether a cylinder will be placed at a feasible position.
        :param int position: The position that is being checked.
        :param Individual cylinder: The cylinder that is being evaluated.
        :param int total_positions: The total number of possible positions at the position index.
        :param int positions_left: The number of positions left to check
        :param bool debug: Whether the function should output the decoding process.
        :return: int, A feasible position. This would be the passed argument if it succeeded, or -1 if the cylinder
        should be discarded.
        """
        cprint(debug, f"Evaluating Position:\t{position}")

        # - Recursion terminator - #
        if positions_left == 0:  # if we have looped through all possible positions and are back to the original position.
            return -1

        # -- Geometric -- #
        # - Adjust centre of cylinder based on the position number - #

        # Get the cylinder corresponding to the position
        target_cylinder = self._cylinders[position // self._cylinder_sides]
        cprint(debug, f"Targeting Cylinder: \t{position // self._cylinder_sides}\n\t- Weight: {target_cylinder.weight}\t- Radius: {target_cylinder.radius}\t- Centre: {target_cylinder.centre}")

        # Preset the point to the right position of the target cylinder such that both cylinders touch one another
        positioned_point = (target_cylinder.centre[0] + target_cylinder.radius + cylinder.radius, target_cylinder.centre[1])
        cprint(debug, f"Preset position is:\t{positioned_point}")

        # Rotate the positioned point by a radian amount defined by the side number multiplied by the distance between each side.
        cylinder.centre = rotate(
            target_cylinder.centre,
            positioned_point,
            (position % self._cylinder_sides) * (360 / self._cylinder_sides)
        )
        cprint(debug, f"Rotated position:\t({cylinder.centre[0]:.4f}, {cylinder.centre[1]:.4f})")

        # - Container-based - #
        # Check if cylinder fits within the container based on its current position.
        if (cylinder.left() < 0 or cylinder.right() > self._container_width) or \
                (cylinder.bottom() < 0 or cylinder.top() > self._container_height):
            cprint(debug, "\033[31m\t---- Doesn't fit in container ----\033[0m")

            # in the case it's not fully in the container, move to the next position
            return self.check_feasibility((position + 1) % total_positions, cylinder, total_positions, positions_left - 1, debug)

        cprint(debug, f"\033[32m\t---- Fits inside the container! ----\033[0m")

        # - Neighbour-based - #
        # Check if the cylinder intersects in more than one place with another already placed cylinder.
        for i, individual in enumerate(self._cylinders[:(total_positions // self._cylinder_sides) + 1]):
            # checks whether the distance between the two cylinder centres is less than the sum of their radii.
            # allow a small tolerance (0.01) for any rotations.
            if (individual != cylinder) and (dist(individual.centre, cylinder.centre) < individual.radius + cylinder.radius -.01):
                cprint(debug, f"\033[31m\t---- Intersects with Cylinder {i} ----\033[0m", dist(individual.centre, cylinder.centre), individual.radius + cylinder.radius)

                # individual intersects! Therefore, another position needs to be used.
                return self.check_feasibility((position + 1) % total_positions, cylinder, total_positions, positions_left - 1, debug)

        cprint(debug, f"\033[32m\t---- No intersections detected! ----\033[0m")

        return position

    def fitness(self) -> float:
        """
        The fitness is the inverse of the distance between the COM and the centre of the container.
        (shorter distance = higher fitness)
        AN OVERRIDE THAT USES THE DECODED CYLINDERS INSTEAD OF THE INITIAL CYLINDERS.
        :return: -> float
        """
        distance = dist(com(self.__decoded_cylinders, self._weight), (self._container_width / 2, self._container_height / 2))
        if distance == 0:  # if the packed COM is at the centre of the container.
            return float("inf")

        return 1. / distance
