from typing import List
from utils import *
from math import radians, dist
import random

random.seed(42)

# -- Initialise container types -- #
# Define unit container size
CONTAINER_WIDTH, CONTAINER_HEIGHT = (20., 15.)

# Define the number of sides a cylinder will have
CYLINDER_SIDES = 8

# Define cylinder containers: [(Weight, Diameter)]
CYLINDERS = [
    (2500, 2.),  # Heavy tank
    (800, 1.5),  # Medium drum
    (300, 1.2)   # Light barrel
]


class Cylinder:
    """Represents a cylinder of a particular type."""

    def __init__(self, sides: int, radius: float, weight: int):
        self.__sides = sides
        self.__radius = radius
        self.__weight = weight

        self.__centre = (0., 0.)

    @property
    def centre(self) -> Tuple[float, float]:
        return self.__centre

    @centre.setter
    def centre(self, new_centre: Tuple[float, float]) -> None:
        self.__centre = new_centre

    @property
    def radius(self) -> float:
        return self.__radius

    @property
    def weight(self) -> int:
        return self.__weight

    def left(self) -> float:
        return self.__centre[0] - self.__radius

    def right(self) -> float:
        return self.__centre[0] + self.__radius

    def top(self) -> float:
        return self.__centre[1] + self.__radius

    def bottom(self) -> float:
        return self.__centre[1] - self.__radius


class CylinderGroup:
    """Contains cylinders in a particular grouping."""

    def __init__(self, cylinders: List[Cylinder], num_cylinders: int, cylinder_sides: int, max_weight: int):
        self.__cylinders = cylinders
        self.__num_cylinders = num_cylinders
        self.__cylinder_sides = cylinder_sides
        self.__max_weight = max_weight

        self.__weight = 0

        # A group will contain a list of random position numbers for each cylinder, apart from the first as that is
        # to be placed in the centre of the container.
        self.__group = random.sample(range(num_cylinders * cylinder_sides), k=num_cylinders - 1)

    def decode(self, debug: bool = False) -> None:
        """
        Decodes the position numbers within the group.
        :param bool debug: Whether to show debug messages or not.
        :return: None
        """
        cprint(debug, f"Outputting decoding process for: {self.__group}")

        for i in range(self.__num_cylinders - 1):
            # Check if the position number is greater than the maximum position number for the ith circle being seen.
            max_positions = (i + 1) * self.__cylinder_sides
            if self.__group[i] > max_positions:
                # if it is reset the position number to 0
                self.__group[i] = 0

            cprint(debug, f"+----\tWorking on cylinder: {i + 1}/{self.__num_cylinders - 1}\t----+")
            self.__group[i] = self.check_feasibility(self.__group[i], self.__cylinders[i + 1], max_positions, max_positions, debug)
            cprint(debug, f"Final position: {self.__group[i]}, with position: {self.__cylinders[i + 1].centre}\n")

        print(self.__group)

        # --- Filter any -1 positions --- #


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

        # -- Weight -- #
        if cylinder.weight + self.__weight > self.__max_weight:
            return -1

        # -- Geometric -- #
        # - Adjust centre of cylinder based on the position number - #

        # Get the cylinder corresponding to the position
        target_cylinder = self.__cylinders[position // self.__cylinder_sides]
        cprint(debug, f"Targeting Cylinder: \t{position // self.__cylinder_sides}\n\t- Weight: {target_cylinder.weight}\t- Radius: {target_cylinder.radius}\t- Centre: {target_cylinder.centre}")

        # Preset the point to the right position of the target cylinder such that both cylinders touch one another
        positioned_point = (target_cylinder.centre[0] + target_cylinder.radius + cylinder.radius, target_cylinder.centre[1])
        cprint(debug, f"Preset position is:\t{positioned_point}")

        # Rotate the positioned point by a radian amount defined by the side number multiplied by the distance between each side.
        cylinder.centre = rotate(
            target_cylinder.centre,
            positioned_point,
            radians((position % self.__cylinder_sides) * (360 / self.__cylinder_sides))
        )
        cprint(debug, f"Rotated position:\t({cylinder.centre[0]:.4f}, {cylinder.centre[1]:.4f})")

        # - Container-based - #
        # Check if cylinder fits within the container based on its current position.
        if (cylinder.left() < 0 or cylinder.right() > CONTAINER_WIDTH) or \
                (cylinder.bottom() < 0 or cylinder.top() > CONTAINER_HEIGHT):
            cprint(debug, "\033[31m\t---- Doesn't fit in container ----\033[0m")

            # in the case it's not fully in the container, move to the next position
            return self.check_feasibility((position + 1) % total_positions, cylinder, total_positions, positions_left - 1, debug)

        cprint(debug, f"\033[32m\t---- Fits inside the container! ----\033[0m")

        # - Neighbour-based - #
        # Check if the cylinder intersects in more than one place with another already placed cylinder.
        for i, individual in enumerate(self.__cylinders[:(total_positions // self.__cylinder_sides) + 1]):
            # checks whether the distance between the two cylinder centres is less than the sum of their radii.
            # allow a small tolerance (0.01) for any rotations.
            if (individual != cylinder) and (dist(individual.centre, cylinder.centre) < individual.radius + cylinder.radius -.01):
                cprint(debug, f"\033[31m\t---- Intersects with Cylinder {i} ----\033[0m", dist(individual.centre, cylinder.centre), individual.radius + cylinder.radius)

                # individual intersects! Therefore, another position needs to be used.
                return self.check_feasibility((position + 1) % total_positions, cylinder, total_positions, positions_left - 1, debug)

        cprint(debug, f"\033[32m\t---- No intersections detected! ----\033[0m")

        return position


class Population:
    """Manages a population of individuals and evolutionary operations inside a container."""

    def __init__(self, size: int, num_cylinders: int, mutation_rate: float, max_generations: int, cylinder_sides: int,
                 max_weight):
        self.__size = size
        self.__mutation_rate = mutation_rate
        self.__max_generations = max_generations

        self.__generations = 0

        # - Initialise cylinders - #
        # Get a random selection of different cylinder types and save them as objects
        self.__cylinders = [Cylinder(CYLINDER_SIDES, diameter / 2, weight) for weight, diameter in random.choices(CYLINDERS, k=num_cylinders)]

        # Sorts the cylinders in descending order based on size (radius)
        self.__cylinders = sorted(self.__cylinders, reverse=True, key=lambda x: x.weight)

        # Sets the first cylinder's centre to the middle of the container.
        self.__cylinders[0].centre = (CONTAINER_WIDTH / 2, CONTAINER_HEIGHT / 2)

        print("+-----------\tInitialised cylinders\t-----------+")
        for i, cylinder in enumerate(self.__cylinders):
            print(f"Cylinder {i+1}:\t- Weight: {cylinder.weight}\t- Centre: {cylinder.centre}\t- Radius: {cylinder.radius}")

        # - Initialise population with random position strings - #
        self.__population = [CylinderGroup(self.__cylinders, num_cylinders, cylinder_sides, max_weight) for _ in range(size)]
        print(f"\nSample of population: {random.sample(self.__population, k=3)}\n")

    def decode(self) -> None:
        """
        Decodes the population to ensure each group of cylinders is grouped feasibly.
        :return: None
        """
        for i, cylinder_group in enumerate(self.__population):
            cylinder_group.decode(i == 0)
            break

    def evolve(self):
        """Run a single generation of the genetic algorithm."""
        self.decode()



if __name__ == "__main__":
    population = Population(50, 5, .1, 100, CYLINDER_SIDES, 5000)
    population.evolve()
